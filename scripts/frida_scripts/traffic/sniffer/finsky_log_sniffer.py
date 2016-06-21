import os
import base_sniffer
import frida_scripts.traffic.loader.tcp_traffic_loader as tcp_traffic_loader
import frida_scripts.traffic.unloader.tcp_traffic_unloader as tcp_traffic_unloader
import frida_scripts.traffic.sink.sink_file as sink_file

Sink = sink_file.FileSink
TrafficLoader = tcp_traffic_loader.TrafficLoaderTCP
TrafficUnloader = tcp_traffic_unloader.TrafficUnloaderTCP



class FinskyLogSniffer(base_sniffer.Sniffer):
    def __init__(self, loaders, unloaders):
        super(FinskyLogSniffer, self).__init__(loaders, unloaders)
        self._log_loader = self._loaders[0]

                    # FinskyLog.a.overload("java.lang.Throwable", "java.lang.String", "[Ljava.lang.Object").implementation = function (ex, s, objs) {
                    #     var msg = {}
                    #     msg["msg"] = "FinskyLog.a"
                    #     msg["src"] = "a"
                    #     send(msg, s)
                    #     this.a(ex, s, objs);
                    # };
    def get_sniffer_js(self):
        ssl = """
            Dalvik.perform(function () {
                    var FinskyLog = Dalvik.use("com.google.android.finsky.utils.FinskyLog");
                    var String = Dalvik.use("java.lang.String")

                    FinskyLog.a.overload("java.lang.String").implementation = function (s) {
                        var msg = {}
                        msg["msg"] = "FinskyLog.a"
                        msg["src"] = "a"
                        msg["s"] = s
                        send(msg)
                        return this.a(s);                 
                    };

                    FinskyLog.a.overload("java.lang.String", "[Ljava.lang.Object;").implementation = function (s, objs) {
                        var msg = {}
                        msg["msg"] = "FinskyLog.a"
                        msg["src"] = "a"
                        msg["s"] = s
                        msg["objs"] = objs
                        send(msg)
                        return this.a(s, objs);                 
                    };
                    

            });
        """
        #import frida_scripts.traffic.misc as misc
        #ssl =misc.PRINT_FINSKY_LOG_A_OVERLOADS
        return ssl

    def on_message(self, message, data): 
        try:
            if "src" in message["payload"]:
                if message["payload"]["src"] == "a":
                    if "s" in message["payload"]:
                        if "objs" in message["payload"] and len(tuple(message["payload"]["objs"])) > 0:
                            # args = tuple(message["payload"]["objs"])
                            # norm_args = []
                            # for arg in args:
                            #     if not isinstance(arg, dict):
                            #         norm_args.append(arg)
                            #     else:
                            #         norm_args.append(str(arg))
                            # msg = message["payload"]["s"] % tuple(norm_args)
                            # msg += "\n"
                            msg = message["payload"]["s"] + "\n"

                        else:
                            msg = message["payload"]["s"] + "\n"

                        self._log_loader.load(msg)
                    else:
                        print message, data
                else:
                    print message, data    
            else:
                print message, data

        except Exception as e:
            print message
            print e

    @staticmethod
    def _create_loaders(base_port):
        loader = TrafficLoader.create_loader(TrafficLoader, base_port)       
        loader.daemon=True
        loader.start()
        return [loader]


    @staticmethod
    def _create_unloaders(base_port, output_dir):
        output_dir = os.path.join(output_dir, "finsky")
        logging_sink = Sink(output_dir)

        unloaders_defs = [(base_port, logging_sink)]

        unloaders = TrafficUnloader.create_unloaders(TrafficUnloader, unloaders_defs)
        for unloader in unloaders:
            unloader.daemon=True
            unloader.start()

        return unloaders