import tkinter.filedialog
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import threading
from ctypes import *
import time
import socket
import tkinter.messagebox

WIDGHT_WIDTH=600
WIDGHT_HEIGHT=400

#socket
size=1024
global_socket=None

#UDS
UDS_protocol="02fd"
UDS_type="8001"
UDS_src="0e80"
UDS_adderss="16e2"
secuity_level=0


def With_Thread(f):
    def Threads(*args):
        t = threading.Thread(target=f, args=(*args,))
        t.setDaemon(True)
        t.start()
    return Threads

#Diag
class Diag():
    def __init__(self):
        self.UDS_dll = windll.LoadLibrary("evg_sa_capldll.dll")
        pass

    @With_Thread
    def socket_disconect(self, socket_obj):
        try:
            socket_obj.shutdown(2)
            socket_obj.close()
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),":socket已关闭！")
            demo.socket_connect_button.configure(bg="blue", text="- -",command=lambda: demo.UDS.socket_conect())
        except:
            tkinter.messagebox.showwarning('警告', 'socket关闭失败！')
            demo.socket_connect_button.configure(bg="yellow", text="alm")

    @With_Thread
    def socket_conect(self):
        try:
            global global_socket
            global_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            global_socket.connect(("192.168.0.6",13400))
            demo.socket_connect_button.configure(bg="green", text="on",command=lambda: demo.UDS.socket_disconect(global_socket))
            self.socket_rx(global_socket)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," :socket已连接！")
        except :
            tkinter.messagebox.showwarning('警告', 'socket连接失败！')
            demo.socket_connect_button.configure(bg="yellow",text="alm")

    def socket_tx(self,socket_obj,imdata):
        length=(hex(int((len(imdata))/2)+4)).replace("0x","").zfill(8)
        data=UDS_protocol+UDS_type+length+UDS_src+UDS_adderss+imdata.lower().replace(" ","")
        socket_obj.send(bytes.fromhex(data))
        tx_data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" TX: "+data+"\n"
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " TX: " + data + "\n")
        demo.datadisplay.insert(INSERT, tx_data)

    def socket_tx_sec(self,socket_obj):
        imdata=demo.datainput_text.get("1.0",END)
        length=(hex(int((len(imdata))/2)+4)).replace("0x","").zfill(8)
        data=UDS_protocol+UDS_type+length+UDS_src+UDS_adderss+imdata
        ret=socket_obj.send(bytes.fromhex(data))
        tx_data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" TX: "+data+"\n"
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " TX: " + data + "\n")
        demo.datadisplay.insert(INSERT, tx_data)

    @With_Thread
    def socket_tx_baochi(self,socket_obj):
        while 1:
            time.sleep(3)
            length=(hex(6)).replace("0x","").zfill(8)
            data=UDS_protocol+UDS_type+length+UDS_src+UDS_adderss+'3e80'
            ret=socket_obj.send(bytes.fromhex(data))
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " TX: " + data + "\n")


    @With_Thread
    def socket_rx(self,socket_obj):
        try:
            while True:
                global secuity_level
                data = socket_obj.recv(size).hex()
                if data[24:28] == "6701":
                    secuity_level=data[28:]
                elif data[24:28] == "6703":
                    secuity_level = data[28:]
                elif data[24:28] == "6705":
                    secuity_level = data[28:]
                elif data[24:28] == "6707":
                    secuity_level = data[28:]
                elif data[24:28] == "6709":
                    secuity_level = data[28:]
                elif data[24:28] == "670B":
                    secuity_level = data[28:]
                else:
                    pass
                rx_data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" RX: " + data +"\n"
                if data == "02fd80020000000516e20e8000":
                    pass
                else:
                    demo.datadisplay.insert(INSERT, rx_data)
        except:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," :OSError: [WinError 10038]")

    @With_Thread
    def secuity_level_set(self):
        if demo.secuitylevel_Radiobutton_v.get() == 0:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," :1级解锁")
            self.socket_tx(global_socket,"2701")
            time.sleep(1)
            print(secuity_level)
            data=self.secuity_level_seed(secuity_level,0)
            self.socket_tx(global_socket, "2702"+data)
        elif demo.secuitylevel_Radiobutton_v.get() == 1:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," :3级解锁")
            self.socket_tx(global_socket, "2703")
            time.sleep(1)
            data = self.secuity_level_seed(secuity_level, 1)
            self.socket_tx(global_socket, "2704" + data)
        elif demo.secuitylevel_Radiobutton_v.get() == 2:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," :5级解锁")
            self.socket_tx(global_socket, "2705")
            time.sleep(1)
            data = self.secuity_level_seed(secuity_level, 2)
            self.socket_tx(global_socket, "2706" + data)
        elif demo.secuitylevel_Radiobutton_v.get() == 3:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," :7级解锁")
            self.socket_tx(global_socket, "2707")
            time.sleep(1)
            data = self.secuity_level_seed(secuity_level, 3)
            self.socket_tx(global_socket, "2708" + data)
        elif demo.secuitylevel_Radiobutton_v.get() == 4:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," :9级解锁")
            self.socket_tx(global_socket, "2709")
            time.sleep(1)
            data = self.secuity_level_seed(secuity_level, 4)
            self.socket_tx(global_socket, "270A" + data)
        elif demo.secuitylevel_Radiobutton_v.get() == 5:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," :B级解锁")
            self.socket_tx(global_socket, "270B")
            time.sleep(1)
            data = self.secuity_level_seed(secuity_level, 5)
            self.socket_tx(global_socket, "270C" + data)
        else:
            pass

    def secuity_level_seed(self,data,level):
        num1 = 4
        num2 = 16
        export1 = c_byte * num1
        export2 = c_byte * num2
        data_import = export1(int(data[0:2],16), int(data[2:4],16), int(data[4:6],16), int(data[6:8],16))
        data_export = export2()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," :",self.UDS_dll.UvDsmSaAlgorithm_Evg(data_import, level, data_export))
        list = []
        for i in range(len(data_export)):
            if data_export[i] >= 0:
                list.append(hex(data_export[i]).replace("0x", "").zfill(2))
            else:
                list.append(hex(data_export[i] % 256).replace("0x", "").zfill(2))
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," 秘钥:",''.join(list))
        return ''.join(list)

#GUI
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Doip诊断工具@yc")
        self.resizable(False, False)
        self.geometry(str(WIDGHT_WIDTH) + "x" + str(WIDGHT_HEIGHT) + '+200+25')
        self.WidgetsInit()
        self.UDS=Diag()

    def WidgetsInit(self):
        self._First_frame = tk.Frame(self)
        self._First_frame.grid(row=1, column=1, padx=2, pady=2, sticky=tk.NSEW)

        self._Second_datainput = tk.LabelFrame(self._First_frame, height=275, width=200, text="诊断命令")
        self._Second_datainput.grid_propagate(0)
        self._Second_datainput.grid(row=0, column=0, padx=2, pady=2, sticky=tk.NE)
        self._Third_datainput_WidgetsInit()

        self._Second_dataprint = tk.LabelFrame(self._First_frame, height=275, width=387.5, text="诊断结果")
        self._Second_dataprint.grid_propagate(0)
        self._Second_dataprint.grid(row=0, column=1, padx=2, pady=2, sticky=tk.NE)
        self._Third_dataprint_WidgetsInit()

        self._Second_dataflash = tk.LabelFrame(self._First_frame, height=110, width=590.5, text="诊断刷写-TBD")
        self._Second_dataflash.grid_propagate(0)
        self._Second_dataflash.grid(row=1, column=0,columnspan=2,padx=2, pady=2, sticky=tk.NW)
        self._Third_dataflash_WidgetsInit()

    def _Third_datainput_WidgetsInit(self):
        tk.Label(self._Second_datainput, text='192.168.0.6').grid(row=0, column=0, padx=20, pady=2.5)
        self.socket_connect_button=tk.Button(self._Second_datainput,bg="blue",width=4,text='- -',command=lambda: self.UDS.socket_conect())
        self.socket_connect_button.grid(row=0, column=1, padx=2, pady=2.5, sticky=tk.E + tk.W)

        self.Diag_set_Radiobutton_v = IntVar()
        self.Diag_set_Phy_button = tk.Radiobutton(self._Second_datainput, value=0,variable=self.Diag_set_Radiobutton_v,text="物理寻址",command=self.Diag_Set_Setting)
        self.Diag_set_Phy_button.grid(row=1, column=0, padx=2, pady=1, sticky=tk.NW)
        self.Diag_set_Fun_button = tk.Radiobutton(self._Second_datainput, value=1, variable=self.Diag_set_Radiobutton_v,text="功能寻址", command=self.Diag_Set_Setting)
        self.Diag_set_Fun_button.grid(row=1, column=1, padx=2, pady=1, sticky=tk.NW)

        self.datainput_text = tk.Text(self._Second_datainput, bd=3, height=3, width=10)
        self.datainput_text.grid(row=2, column=0, rowspan=2,padx=5)
        self.socket_trans_button = tk.Button(self._Second_datainput, width=6, text='发送',command=lambda :self.UDS.socket_tx_sec(global_socket))
        self.socket_trans_button.grid(row=2, column=1, padx=2, pady=1, sticky=tk.E + tk.W)
        self.socket_clear_button = tk.Button(self._Second_datainput, width=6, text='清空',command=self.data_delete)
        self.socket_clear_button.grid(row=3, column=1, padx=2, pady=1, sticky=tk.E + tk.W)

        tk.Label(self._Second_datainput, text='安全等级：').grid(row=4, column=0, padx=20, pady=2.5)
        self.secuitylevel_Radiobutton_v = IntVar()
        self.secuity1_button = tk.Radiobutton(self._Second_datainput, value=0, variable=self.secuitylevel_Radiobutton_v,
                                                  text="1级", command=lambda :self.UDS.secuity_level_set())
        self.secuity1_button.grid(row=4, column=1, padx=2, pady=1, sticky=tk.E + tk.W)
        self.secuity3_button = tk.Radiobutton(self._Second_datainput, value=1, variable=self.secuitylevel_Radiobutton_v,
                                                  text="3级", command=lambda :self.UDS.secuity_level_set())
        self.secuity3_button.grid(row=5, column=0, padx=2, pady=1, sticky=tk.E + tk.W)
        self.secuity5_button = tk.Radiobutton(self._Second_datainput, value=2, variable=self.secuitylevel_Radiobutton_v,
                                                  text="5级", command=lambda :self.UDS.secuity_level_set())
        self.secuity5_button.grid(row=5, column=1, padx=2, pady=1, sticky=tk.E + tk.W)

        self.secuity7_button = tk.Radiobutton(self._Second_datainput, value=3, variable=self.secuitylevel_Radiobutton_v,
                                              text="7级", command=lambda: self.UDS.secuity_level_set())
        self.secuity7_button.grid(row=6, column=0, padx=2, pady=1, sticky=tk.E + tk.W)
        self.secuity7_button = tk.Radiobutton(self._Second_datainput, value=4, variable=self.secuitylevel_Radiobutton_v,
                                              text="9级", command=lambda: self.UDS.secuity_level_set())
        self.secuity7_button.grid(row=6, column=1, padx=2, pady=1, sticky=tk.E + tk.W)
        self.secuity7_button = tk.Radiobutton(self._Second_datainput, value=5, variable=self.secuitylevel_Radiobutton_v,
                                              text="B级", command=lambda: self.UDS.secuity_level_set())
        self.secuity7_button.grid(row=7, column=0, padx=2, pady=1, sticky=tk.E + tk.W)


        self.socket_diag_con_button = tk.Button(self._Second_datainput, width=4, text='会话保持',
                                               command=lambda :self.UDS.socket_tx_baochi(global_socket))
        self.socket_diag_con_button.grid(row=7, column=1, padx=2, pady=2.5, sticky=tk.E + tk.W)

    def _Third_dataprint_WidgetsInit(self):
        self.datadisplay = tk.Text(self._Second_dataprint, bd=3, height=18, width=52)
        self.datadisplay.grid(row=0, column=0, padx=5)
        pass

    def _Third_dataflash_WidgetsInit(self):
        self.path = StringVar()
        tk.Label(self._Second_dataflash, text='镜像路径:').grid(row=0, column=0, padx=5, pady=2.5)
        self.file_path = tk.Entry(self._Second_dataflash, textvariable=self.path, width=34)
        self.file_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self._Second_dataflash, text='文件选择', command=self.data_file_path).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self._Second_dataflash, text='刷写进度:').grid(row=1, column=-0, padx=5, pady=2.5, sticky=tk.E + tk.W)
        self.process_display = ttk.Progressbar(self._Second_dataflash, maximum=100, value=0, length=245,
                                               mode='determinate')
        self.process_display.grid(row=1, column=1, padx=5, pady=2.5)
        pass


    def Diag_Set_Setting(self):
        global UDS_adderss
        if self.Diag_set_Radiobutton_v.get() == 0:
            UDS_adderss="16E2"
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),' 寻址设置：',UDS_adderss)
        elif self.Diag_set_Radiobutton_v.get() == 1:
            UDS_adderss = "E400"
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," 寻址设置：",UDS_adderss)
        else:
            pass

    def data_file_path(self):
        self.file_path.delete(0, END)
        path_ = tkinter.filedialog.askopenfilename()
        path_ = path_.replace("/", "\\\\")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " loginfo[data_file_path][1]：" + path_)
        self.path.set(path_)
        pass

    def data_delete(self):
        self.datainput_text.delete("1.0", END)
        self.datadisplay.delete("1.0", END)

if __name__=='__main__':
    try:
        demo = GUI()
        demo.mainloop()
    finally:
        demo.UDS.socket_disconect(global_socket)
