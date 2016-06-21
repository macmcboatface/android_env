
PRINT_OBJECT_METHOD_OVERLOADS = """
	Dalvik.perform(function () {
        var cls = Dalvik.use("%s");
        group = cls.%s.overloads;
        method = null;
        s="";
        f = function (t) {return t.className;};
        i=0;
        for (i = 0; i !== group.length; i++) {
        	method = group[i];
        	s = method.argumentTypes.map(f).join(":");
        	send(s);
        }
    });
"""
PRINT_INPUT_STREAM_READ_OVERLOADS = PRINT_OBJECT_METHOD_OVERLOADS % ("com.android.org.conscrypt.OpenSSLSocketImpl$SSLInputStream",
	"read",
	)

PRINT_VERIFIER_A_OVERLOADS = PRINT_OBJECT_METHOD_OVERLOADS % ("com.google.android.gms.common.kv",
    "a",
    )

PRINT_FINSKY_LOG_A_OVERLOADS = PRINT_OBJECT_METHOD_OVERLOADS % ("com.google.android.finsky.utils.FinskyLog",
    "a",
    )

PRINT_STRING_GETBYTES_OVERLOADS = PRINT_OBJECT_METHOD_OVERLOADS % ("java.lang.String",
    "getBytes",
    )