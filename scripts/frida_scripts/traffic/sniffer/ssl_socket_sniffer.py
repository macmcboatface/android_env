from subprocess import Popen
import frida
import sys
import os
import base_sniffer
import frida_scripts.traffic.loader.tcp_traffic_loader as tcp_traffic_loader
import frida_scripts.traffic.unloader.tcp_traffic_unloader as tcp_traffic_unloader
import frida_scripts.traffic.sink.sink_file as sink_file
import frida_scripts.traffic.sink.sink_dir as sink_dir

Sink = sink_dir.DirSink
TrafficLoader = tcp_traffic_loader.TrafficLoaderTCP
TrafficUnloader = tcp_traffic_unloader.TrafficUnloaderTCP

class SocketInTheMiddle(object):
    _generic_outgoing_traffic_loader = None
    _generic_incoming_traffic_loader = None
    def __init__(self, outgoing_loader, incoming_loader):
        self._outgoing_traffic_loader = outgoing_loader
        self._incoming_traffic_loader = incoming_loader

    def write(self, data):
        self._outgoing_traffic_loader.load(data)

    def read(self, data):
        self._incoming_traffic_loader.load(data)

    def new(self):
        pass

    def free(self):
        pass

    def do_handshake(self):
        pass

    def shutdown(self):
        pass

    def set_fd(self):
        pass

    def renegotiate(self):
        pass

    @staticmethod
    def generic_write(data):
        SocketInTheMiddle._generic_outgoing_traffic_loader.load(data)

    @staticmethod
    def generic_read(data):
        SocketInTheMiddle._generic_incoming_traffic_loader.load(data)

    @staticmethod
    def generic_do_handshake(*args, **kwargs):
        pass

    @staticmethod
    def generic_new(*args, **kwargs):
        pass

    @staticmethod
    def generic_free(*args, **kwargs):
        pass

    @staticmethod
    def generic_set_fd(*args, **kwargs):
        pass

    @staticmethod
    def generic_renegotiate(*args, **kwargs):
        pass

    @staticmethod
    def generic_shutdown(*args, **kwargs):
        #SocketInTheMiddle._generic_incoming_traffic_loader.load()
        pass

    @staticmethod
    def set_generics(_generic_outgoing_traffic_loader, _generic_incoming_traffic_loader):
        SocketInTheMiddle._generic_outgoing_traffic_loader = _generic_outgoing_traffic_loader
        SocketInTheMiddle._generic_incoming_traffic_loader = _generic_incoming_traffic_loader

class SocketSniffer(base_sniffer.Sniffer):
    def __init__(self, loaders, unloaders):
        super(SocketSniffer, self).__init__(loaders, unloaders)
        self._outgoing_traffic_loader = self._loaders[0]
        self._incoming_traffic_loader = self._loaders[1]
        self.sockets = {}
        self.counter = 0
        SocketInTheMiddle.set_generics(self._outgoing_traffic_loader,
            self._incoming_traffic_loader
            )

    SSL_WRITE_SCRIPT = """
Interceptor.attach(Module.findExportByName(null, "SSL_write"), {
    onEnter: function(args) {
        this.sslNativePointer = args[0]
        this.fd = args[1];
        this.SSLHandshakeCallbacks = args[2]
        this.buff = args[3];
        this.offset = args[4];
        this.byteCount = args[5];
        this.writeTimeoutMs = args[6];

        this.buff = args[1];
        this.byteCount = args[2];
        this.writeTimeoutMs = args[3];
        this.offset = args[4];
    }
    , onLeave: function(retval) {
        if(retval.toInt32()<= 0) {
            msg = {}
            msg["type"] = "meta"
            msg["sslNativePointer"] = this.sslNativePointer
            msg["origin"] = "SSL_write"
            msg["error"] = "eof"
            send(msg);
        }
        if(retval.toInt32() > 0) {
            msg = {}
            msg["type"] = "data"
            msg["sslNativePointer"] = this.sslNativePointer
            msg["origin"] = "SSL_write"
            buff = Memory.readByteArray(ptr(this.buff.toInt32()+this.offset.toInt32()), retval.toInt32())
            send(msg, buff);
        }
    }
});
"""


    SSL_READ_SCRIPT = """
Interceptor.attach(Module.findExportByName(null, "SSL_read"), {
    onEnter: function(args) {
        this.sslNativePointer = args[0]
        this.fd = args[1];
        this.SSLHandshakeCallbacks = args[2]
        this.buff = args[3];
        this.offset = args[4];
        this.byteCount = args[5];
        this.writeTimeoutMs = args[6];


        this.buff = args[1];
        this.byteCount = args[2];
        this.writeTimeoutMs = args[3];
        this.offset = args[4];
    }
    , onLeave: function(retval) {

        if(retval.toInt32()<= 0) {
            msg = {}
            msg["type"] = "meta"
            msg["sslNativePointer"] = this.sslNativePointer
            msg["origin"] = "SSL_read"
            msg["error"] = "eof"
            send(msg);
        }
        if(retval.toInt32() > 0) {
            msg = {}
            msg["type"] = "data"
            msg["sslNativePointer"] = this.sslNativePointer
            msg["origin"] = "SSL_read"
            buff = Memory.readByteArray(ptr(this.buff.toInt32()+this.offset.toInt32()), retval.toInt32())
            send(msg, buff);
        }

    }
});
"""
    SSL_NEW_SCRIPT = """
Interceptor.attach(Module.findExportByName(null, "SSL_new"), {
    onEnter: function(args) {
        this.sslNativePointer = args[0]
    }
    , onLeave: function(retval) {
        msg = {}
        msg["type"] = "meta"
        msg["sslNativePointer"] = retval
        msg["origin"] = "SSL_new"
        send(msg);
    }
});
"""
    SSL_FREE_SCRIPT = """
Interceptor.attach(Module.findExportByName(null, "SSL_free"), {
    onEnter: function(args) {
        this.sslNativePointer = args[0]
        //for(var i =0; i < 3; i++) {
        //    send("args[" + i + "]=" + args[i])
        //}
    }
    , onLeave: function(retval) {
        msg = {}
        msg["type"] = "meta"
        msg["sslNativePointer"] = this.sslNativePointer
        msg["origin"] = "SSL_free"
        send(msg);
    }
});
"""
    SSL_DO_HANDSHAKE_SCRIPT = """
Interceptor.attach(Module.findExportByName(null, "SSL_do_handshake"), {
    onEnter: function(args) {
        this.sslNativePointer = args[0]
    }
    , onLeave: function(retval) {
        msg = {}
        msg["type"] = "meta"
        msg["sslNativePointer"] = this.sslNativePointer
        msg["origin"] = "SSL_do_handshake"
        send(msg);
    }
});
"""
    SSL_SET_FD_SCRIPT = """
Interceptor.attach(Module.findExportByName(null, "SSL_set_fd"), {
    onEnter: function(args) {
        this.sslNativePointer = args[0]
    }
    , onLeave: function(retval) {
        msg = {}
        msg["type"] = "meta"
        msg["sslNativePointer"] = this.sslNativePointer
        msg["origin"] = "SSL_set_fd"
        send(msg);
    }
});
"""
    SSL_SHUTDOWN_SCRIPT = """
Interceptor.attach(Module.findExportByName(null, "SSL_shutdown"), {
    onEnter: function(args) {
        this.sslNativePointer = args[0]
    }
    , onLeave: function(retval) {
        msg = {}
        msg["type"] = "meta"
        msg["sslNativePointer"] = this.sslNativePointer
        msg["origin"] = "SSL_shutdown"
        send(msg);
    }
});
"""
    SSL_RENEGOTIATE_SCRIPT = """
Interceptor.attach(Module.findExportByName(null, "SSL_renegotiate"), {
    onEnter: function(args) {
        this.sslNativePointer = args[0]
    }
    , onLeave: function(retval) {
        msg = {}
        msg["type"] = "meta"
        msg["sslNativePointer"] = this.sslNativePointer
        msg["origin"] = "SSL_renegotiate"
        send(msg);
    }
});
"""
    def new(self, sslNativePointer):
        if str(sslNativePointer) not in self.sockets:
            outgoing_loader = self._outgoing_traffic_loader.create_subloader("sock.%s.%s" % (self.counter, sslNativePointer))
            incoming_loader = self._incoming_traffic_loader.create_subloader("sock.%s.%s" % (self.counter, sslNativePointer))
            self.sockets[str(sslNativePointer)] = SocketInTheMiddle(outgoing_loader, incoming_loader)
            self.sockets[str(sslNativePointer)].new()
            self.counter += 1
        else:
            self.sockets[str(sslNativePointer)].generic_new()

    def free(self, sslNativePointer):
        if str(sslNativePointer) in self.sockets:
            self.sockets[str(sslNativePointer)].free()
            del self.sockets[str(sslNativePointer)]
        else:
            SocketInTheMiddle.generic_free()

    def shutdown(self, sslNativePointer):
        if str(sslNativePointer) in self.sockets:
            self.sockets[str(sslNativePointer)].shutdown()
        else:
            SocketInTheMiddle.generic_shutdown()

    def renegotiate(self, sslNativePointer):
        if str(sslNativePointer) in self.sockets:
            self.sockets[str(sslNativePointer)].renegotiate()
        else:
            SocketInTheMiddle.generic_renegotiate()

    def write(self, sslNativePointer, data):
        if str(sslNativePointer) in self.sockets:
            self.sockets[str(sslNativePointer)].write(data)
        else:
            SocketInTheMiddle.generic_write(data)

    def read(self, sslNativePointer, data):
        if str(sslNativePointer) in self.sockets:
            self.sockets[str(sslNativePointer)].read(data)
        else:
            SocketInTheMiddle.generic_read(data)

    def set_fd(self, sslNativePointer):
        if str(sslNativePointer) in self.sockets:
            self.sockets[str(sslNativePointer)].set_fd()
        else:
            SocketInTheMiddle.generic_set_fd()

    def do_handshake(self, sslNativePointer):
        if str(sslNativePointer) in self.sockets:
            self.sockets[str(sslNativePointer)].do_handshake()
        else:
            SocketInTheMiddle.generic_do_handshake()

    def on_message(self, message, data):
        if message['type'] == 'error':
            print("[!] " + message['stack'])
        elif message['type'] == 'send':
            msg = message['payload']
            if not isinstance(msg, dict):
                print msg
            else: #elif isinstance(msg, dict):
                if msg["type"] == "data":
                    if data is not None:
                        if msg["origin"] == "SSL_read":
                            self.read(msg["sslNativePointer"], data)
                        elif msg["origin"] == "SSL_write":
                            self.write(msg["sslNativePointer"], data)
                    else:
                        print(message)
                elif msg["type"] == "meta":
                    if  msg["origin"] == "SSL_new":
                        self.new(msg["sslNativePointer"])
                    elif msg["origin"] == "SSL_shutdown":
                        self.shutdown(msg["sslNativePointer"])
                    elif msg["origin"] == "SSL_do_handshake":
                        self.do_handshake(msg["sslNativePointer"])
                    elif msg["origin"] == "SSL_set_fd":
                        self.set_fd(msg["sslNativePointer"])
                    elif msg["origin"] == "SSL_free":
                        self.free(msg["sslNativePointer"])
                    elif msg["origin"] == "SSL_renegotiate":
                        self.renegotiate(msg["sslNativePointer"])
                elif msg["type"] == "log":
                    print msg
        else:
            print(message)

    def get_sniffer_js(self):
        js = ""
        js += SocketSniffer.SSL_NEW_SCRIPT
        js += SocketSniffer.SSL_FREE_SCRIPT
        js += SocketSniffer.SSL_DO_HANDSHAKE_SCRIPT
        js += SocketSniffer.SSL_RENEGOTIATE_SCRIPT
        js += SocketSniffer.SSL_SET_FD_SCRIPT
        js += SocketSniffer.SSL_SHUTDOWN_SCRIPT
        js += SocketSniffer.SSL_READ_SCRIPT
        js += SocketSniffer.SSL_WRITE_SCRIPT
        return js

    @staticmethod
    def _create_loaders(base_port):
        outgoing_loader = TrafficLoader.create_loader(TrafficLoader, base_port)
        incoming_loader = TrafficLoader.create_loader(TrafficLoader, base_port+1)
        loaders = [outgoing_loader, incoming_loader]
        for loader in loaders:
            loader.daemon = True
            loader.start()
        return loaders

    @staticmethod
    def _create_unloaders(base_port, output_dir):
        outgoing_path = os.path.join(output_dir, "outgoing")
        incoming_path = os.path.join(output_dir, "incoming")

        outgoing_sink = Sink(outgoing_path)
        incoming_sink = Sink(incoming_path)

        unloaders_defs = [(base_port, outgoing_sink),
                            (base_port+1, incoming_sink)]

        unloaders = TrafficUnloader.create_unloaders(TrafficUnloader, unloaders_defs)
        for unloader in unloaders:
            unloader.daemon=True
            unloader.start()

        return unloaders
