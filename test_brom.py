import pythoncom
import win32com.client


V83_CONN_STRING = 'File="D:\Documents\1C\Trade";Usr="Менеджер1";Pwd="";'
pythoncom.CoInitialize()
V83 = win32com.client.Dispatch("V83.COMConnector").Connect(V83_CONN_STRING) 