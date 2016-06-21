import os
import base_sniffer
import frida_scripts.traffic.loader.tcp_traffic_loader as tcp_traffic_loader
import frida_scripts.traffic.unloader.tcp_traffic_unloader as tcp_traffic_unloader
import frida_scripts.traffic.sink.sink_dir as sink_dir

Sink = sink_dir.DirSink
TrafficLoader = tcp_traffic_loader.TrafficLoaderTCP
TrafficUnloader = tcp_traffic_unloader.TrafficUnloaderTCP


class SSLJavaSniffer(base_sniffer.Sniffer):
    def __init__(self, loaders, unloaders):
        super(SSLJavaSniffer, self).__init__(loaders, unloaders)

        self._outgoing_traffic_loader = self._loaders[0]
        self._incoming_traffic_loader = self._loaders[1]

    def get_sniffer_js(self):
        ssl = """
            Dalvik.perform(function () {
                    //var inputStream = Dalvik.use("com.android.org.conscrypt.OpenSSLSocketImpl$SSLInputStream");
                    //inputStream.read.overload().implementation = function () {
                    //    var byte = this.read();
                    //    var msg = {}
                    //    msg["msg"] = "SSLInputStream.read"
                    //    msg["src"] = "read"
                    //    msg["len"] = 1
                    //    msg["byteCount"] = 1
                    //    send(msg, byte)
                    //    return byte
                    //};                

                    //inputStream.read.overload("[B", "int", "int").implementation = function (buff, offset, byteCount) {
                    //    inputStream.read.overload("[B", "int", "int").call(this, buff, offset, byteCount);
                        
                        //return inputStream.read.overload("[B", "int", "int").call(this, buff, offset, byteCount);
                        //return inputStream.read.overload("[B", "int", "int").call(this, buff, offset, byteCount);
                        //return inputStream.read.overload("[B", "int", "int").call(this, buff, offset, byteCount);
                        //Integer bytesRead = inputStream.read.overload("[B", "int", "int").call(this, buff, offset, byteCount);                 
                    //    var msg = {}
                    //    msg["msg"] = "SSLInputStream.read"
                    //    msg["src"] = "read"
                    //    msg["len"] = byteCount
                    //    msg["offset"] = offset
                    //    send(msg, buff)
                    //    return bytesRead;
                    //};

                    var outputStream = Dalvik.use("com.android.org.conscrypt.OpenSSLSocketImpl$SSLOutputStream");

                    outputStream.write.overload("int").implementation = function (byte) {
                        this.write(byte);
                        var msg = {}
                        msg["msg"] = "SSLOutputStream.write"
                        msg["src"] = "write"
                        msg["len"] = 1
                        send(msg, byte)
                        return byte
                    };                

                    outputStream.write.overload("[B", "int", "int").implementation = function (buff, offset, byteCount) {
                        var msg = {}
                        msg["msg"] = "SSLOutputStream.write"
                        msg["src"] = "write"
                        msg["len"] = byteCount
                        msg["offset"] = offset
                        send(msg, buff)
                        this.write(buff, offset, byteCount);                 
                    };
            });
        """
        #import misc
        #ssl =misc.PRINT_INPUT_STREAM_READ_OVERLOADS
        return ssl

    def on_message(self, message, data):  
        try:
            if "src" in message["payload"]:
                if message["payload"]["src"] == "read":
                    if data:
                        length = message["payload"]["len"]
                        offset = message["payload"]["offset"]
                        self._incoming_traffic_loader.load(data[offset: offset+length])

                elif message["payload"]["src"] == "write":
                    if data:
                        length = message["payload"]["len"]
                        offset = message["payload"]["offset"]
                        self._outgoing_traffic_loader.load(data[offset: offset+length])
            else:
                print message, data

        except Exception as e:
            print message
            print e

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