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
import os

WIDGHT_WIDTH=600
WIDGHT_HEIGHT=400

#socket
size=1024
global_socket = None

#UDS
UDS_protocol="02fd"
UDS_type="8001"
UDS_src="0e80"
UDS_adderss="16e2"
secuity_level=0
Flag = True
flash_file_path = None



def With_Thread(f):
    def Threads(*args):
        t = threading.Thread(target=f, args=(*args,))
        t.setDaemon(True)
        t.start()
    return Threads

#Diag
class Diag():
    def __init__(self):
        self.UDS_dll = windll.LoadLibrary(".\evg_sa_capldll.dll")
        pass

    @With_Thread
    def socket_disconect(self, socket_obj):
        try:
            socket_obj.shutdown(2)
            socket_obj.close()
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ":socket已关闭！")
            demo.socket_connect_button.configure(bg="blue", text="- -", command=lambda: demo.UDS.socket_conect())
        except:
            tkinter.messagebox.showwarning('警告', 'socket关闭失败！')
            demo.socket_connect_button.configure(bg="yellow", text="alm")

    @With_Thread
    def socket_conect(self):
        try:
            global global_socket
            global_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            global_socket.connect(("192.168.0.6",13400))
            demo.socket_connect_button.configure(bg="green", text="on", command=lambda: demo.UDS.socket_disconect(global_socket))
            self.socket_rx(global_socket)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " :socket已连接！")
        except :
            tkinter.messagebox.showwarning('警告', 'socket连接失败！')
            demo.socket_connect_button.configure(bg="yellow",text="alm")

    def socket_rx_flash(self, socket_obj):
        try:
            data = socket_obj.recv(size).hex()
            global secuity_level
            if data[24:28] == "6701":
                secuity_level = data[28:]
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
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " RX :" + str(data))
            if data == "02fd80030000000516e20e8000":
                return 'Null'
            else:
                return data
        except Exception as e:
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + f" : {e}")
            return str(e)

    def socket_tx_flash(self, socket_obj, UDS_addr, imdata, flash_data=None):
        if flash_data== None:
            length = (hex(int((len(imdata)) / 2) + 4)).replace("0x", "").zfill(8)
            data = UDS_protocol + UDS_type + length + UDS_src + UDS_addr + imdata.lower().replace(" ", "")
            socket_obj.send(bytes.fromhex(data))
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " TX: ", str(data))
        else:
            length = (hex(int((len(imdata)) / 2) + 4+ len(flash_data))).replace("0x", "").zfill(8)
            data = UDS_protocol + UDS_type + length + UDS_src + UDS_addr + imdata.lower().replace(" ", "")
            socket_obj.send(bytes.fromhex(data) + flash_data)
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " TX: ", str(data))
        return data

    def secuity_level_set_flash(self, socket_obj, UDS_src, level):
        if level == 0:
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " :1级解锁")
            self.socket_tx_flash(socket_obj, UDS_src, "2701")
            self.socket_rx_flash(socket_obj)
            self.socket_rx_flash(socket_obj)
            time.sleep(1)
            data = self.secuity_level_seed_flash(secuity_level, 0)
            self.socket_tx_flash(socket_obj, UDS_src, "2702" + data)
        elif level == 1:
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " :3级解锁")
            self.socket_tx_flash(socket_obj, UDS_src, "2703")
            self.socket_rx_flash(socket_obj)
            self.socket_rx_flash(socket_obj)
            time.sleep(1)
            data = self.secuity_level_seed_flash(secuity_level, 1)
            self.socket_tx_flash(socket_obj, UDS_src, "2704" + data)
        elif level == 2:
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " :5级解锁")
            self.socket_tx_flash(socket_obj, UDS_src, "2705")
            self.socket_rx_flash(socket_obj)
            self.socket_rx_flash(socket_obj)
            time.sleep(1)
            data = self.secuity_level_seed_flash(secuity_level, 2)
            self.socket_tx_flash(socket_obj, UDS_src, "2706" + data)
        elif level == 3:
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " :7级解锁")
            self.socket_tx_flash(socket_obj, UDS_src, "2707")
            self.socket_rx_flash(socket_obj)
            self.socket_rx_flash(socket_obj)
            time.sleep(1)
            data = self.secuity_level_seed_flash(secuity_level, 3)
            self.socket_tx_flash(socket_obj, UDS_src, "2708" + data)
        elif level == 4:
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " :9级解锁")
            self.socket_tx_flash(socket_obj, UDS_src, "2709")
            self.socket_rx_flash(socket_obj)
            self.socket_rx_flash(socket_obj)
            time.sleep(1)
            data = self.secuity_level_seed_flash(secuity_level, 4)
            self.socket_tx_flash(socket_obj, UDS_src, "270A" + data)
        elif level == 5:
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " :B级解锁")
            self.socket_tx_flash(socket_obj, UDS_src, "270B")
            self.socket_rx_flash(socket_obj)
            self.socket_rx_flash(socket_obj)
            time.sleep(1)
            data = self.secuity_level_seed_flash(secuity_level, 5)
            self.socket_tx_flash(socket_obj, UDS_src, "270C" + data)
        else:
            pass

    def secuity_level_seed_flash(self, data, level):
        # zcanpro.write_log("开始计算秘钥")
        num1 = 4
        num2 = 16
        export1 = c_byte * num1
        export2 = c_byte * num2
        data_import = export1(int(data[0:2], 16), int(data[2:4], 16), int(data[4:6], 16), int(data[6:8], 16))
        data_export = export2()
        self.UDS_dll.UvDsmSaAlgorithm_Evg(data_import, level, data_export)
        list = []
        for i in range(len(data_export)):
            if data_export[i] >= 0:
                list.append(hex(data_export[i]).replace("0x", "").zfill(2))
            else:
                list.append(hex(data_export[i] % 256).replace("0x", "").zfill(2))
        # zcanpro.write_log(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+ " 秘钥 : "+ ''.join(list))
        return ''.join(list)


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
        try :
            while 1:
                if Flag:
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
                else:
                    break
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" : {e}")


    @With_Thread
    def secuity_level_set(self):
        if demo.secuitylevel_Radiobutton_v.get() == 0:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," :1级解锁")
            self.socket_tx(global_socket,"2701")
            time.sleep(1)
            data= self.secuity_level_seed(secuity_level,0)
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

    def resp_deal_flash(self, socket_obj, rsp_head, rsp_tail, req, rsp_40p, rsp_78, pro=None, seqnum=None, size=None):
        while True:
            ret = self.socket_rx_flash(socket_obj)
            if ret[rsp_head:rsp_tail] == rsp_40p:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {req} step RX: {ret}，成功！")
                demo.process_display['value'] = pro
                return 1
            elif ret == "02fd80020000000516e20e8000":
                continue
            elif ret == "timed out":
                return 255
            elif ret[-6:] == rsp_78:
                continue
            elif ret == "OSError: [WinError 10038]" or 'Null':
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {req} step RX: 返回值错误,刷写退出！")
                return 0
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {req} step RX: {ret}，失败！")
                return 0

    def resp_deal_flash_36(self, socket_obj, rsp_head, rsp_tail, req, rsp_40p, rsp_78, pro=None, seqnum=None, size=None):
        while True:
            ret = self.socket_rx_flash(socket_obj)
            if ret[rsp_head:rsp_tail] == rsp_40p:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {req} step RX: {ret}，序号{seqnum}成功,剩余大小：{size}！")
                demo.process_display['value'] = pro
                return 1
            elif ret == "02fd80020000000516e20e8000":
                continue
            elif ret == "timed out":
                return 255
            elif ret[-6:] == rsp_78:
                continue
            elif ret == "OSError: [WinError 10038]" or 'Null':
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {req} step RX: 返回值错误,刷写退出！")
                return 0
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {req} step RX: {ret}，失败！")
                return 0

    def flash_36(self, flash_socket, f, size=None):
        file_szie = size
        while True:
            for seq in range(0, 256):
                x = f.read(8192)
                file_szie -= 8192
                if file_szie < -8192:
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 36 step RX: 软件上传完成,序号：{seq}！")
                    demo.process_display['value'] = 30
                    return 1
                else:
                    while 1:
                        self.socket_tx_flash(flash_socket, "16E2", "36" + hex(seq).replace("0x", "").zfill(2), x)
                        ret = self.resp_deal_flash_36(flash_socket, -4, -2, "36", "76", "7f3678", seqnum=seq, size=file_szie)
                        if ret == 0:
                            return 0
                        elif ret == 255:
                            continue
                        elif ret == 1:
                            break
                        else:
                            pass

    def flash_F15C(self, socket_obj):
        while True:
            ret = self.socket_rx_flash(socket_obj)
            if ret[-8:-2] == "62f15c":
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 22F15C step RX: {ret}，成功！")
                if ret[30:32] == "64":
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 22F15C step RX: {ret}，升级进度100%！")
                    demo.process_display['value'] = 96
                    return 1
                else:
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 22F15C step RX: {ret}，升级进度{int(ret[30:32], 16)}%！")
                    demo.process_display['value'] = 30 + 0.6 * int(ret[30:32], 16)
                    return 2
            elif ret[-6:] == "7f2278":
                continue
            elif ret == "02fd80020000000516e20e8000":
                continue
            elif ret == "OSError: [WinError 10038]" or 'Null':
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " 22F15C step RX: 返回值错误,刷写退出！")
                return 0
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 22F15C step RX: {ret}，失败！")
                return 0

    @With_Thread
    def doip_falsh(self, file_path):
        self.socket_disconect(global_socket)
        time.sleep(2)
        flash_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        flash_socket.connect(("192.168.0.6", 13400))
        flash_socket.settimeout(2)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : socket已连接！")
        tkinter.messagebox.showwarning('警告', '刷写期间禁止使用“诊断命令面板按钮、选项”！')
        time.sleep(2)

        # 1001
        self.socket_tx_flash(flash_socket, "16E2", "1001")
        ret = self.resp_deal_flash(flash_socket, -12, -8, "1001", "5001", "7f1078", 1)
        if ret == 0:
            return None

        # 1003
        self.socket_tx_flash(flash_socket, "16E2", "1003")
        ret = self.resp_deal_flash(flash_socket, -12, -8, "1003", "5003", "7f1078", 2)
        if ret == 0:
            return None

        # 8502
        self.socket_tx_flash(flash_socket, "16E2", "8502")
        ret = self.resp_deal_flash(flash_socket, -4, None, "8502", "c502", "7f8578", 3)
        if ret == 0:
            return None

        # 280303
        self.socket_tx_flash(flash_socket, "16E2", "280303")
        ret = self.resp_deal_flash(flash_socket, -4, None, "280303", "6803", "7f2878", 4)
        if ret == 0:
            return None

        # 1002
        self.socket_tx_flash(flash_socket, "16E2", "1002")
        ret = self.resp_deal_flash(flash_socket, -12, -8, "1002", "5002", "7f1078", 5)
        if ret == 0:
            return None

        # 1级解锁
        self.secuity_level_set_flash(flash_socket, '16e2', 0)
        ret = self.resp_deal_flash(flash_socket, -4, None, "1级解锁", "6702", "7f2778")
        if ret == 0:
            return None

        # 2EF199
        self.socket_tx_flash(flash_socket, "16E2", "2EF19920220112")
        self.socket_rx_flash(flash_socket)
        ret = self.resp_deal_flash(flash_socket, -6, None, "2EF199", "6ef199", "7f2e78", 7)
        if ret == 0:
            return None

        # 2EF198
        self.socket_tx_flash(flash_socket, "16E2", "2EF1983131313131313131313131313131313131313131")
        ret = self.resp_deal_flash(flash_socket, -6, None, "2EF198", "6ef198", "7f2e78", 9)
        if ret == 0:
            return None

        # 22F100
        self.socket_tx_flash(flash_socket, "16E2", "22F100")
        ret = self.resp_deal_flash(flash_socket, -14, -8, "22F100", "62f100", "7f2278", 10)
        if ret == 0:
            return None

        with open(str(flash_file_path), "rb") as f:
            file_size = os.path.getsize(str(flash_file_path))
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 36 step : 文件大小为{os.path.getsize(str(flash_file_path))}！")

        # 3803
            self.socket_tx_flash(flash_socket, "16E2", "3803001E443A5C6D6170646174615C6575726F70655C6765726D616E79312E79787A1104"+(hex(file_size).replace("0x", "").zfill(8))*2)
            ret = self.resp_deal_flash(flash_socket, -16, -12, "3803", "7803", "7f3878", 12)
            if ret == 0:
                return None

        # 36
            for seq in range(1, 256):
                x = f.read(8192)
                file_size -= 8192
                while 1:
                    self.socket_tx_flash(flash_socket, "16E2", "36"+hex(seq).replace("0x", "").zfill(2), x)
                    ret = self.resp_deal_flash_36(flash_socket, -4, -2, "36", "76", "7f3678", seqnum=seq, size=file_size)
                    if ret == 0:
                        return None
                    elif ret == 255:
                        continue
                    elif ret == 1:
                        break
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 36 step RX: 块1传输完毕！")
            ret = self.flash_36(flash_socket, f, size=file_size)
            if ret == 0:
                return None

        # 37
        self.socket_tx_flash(flash_socket, "16E2", "37")
        ret = self.resp_deal_flash(flash_socket, -2, None, "37", "77", "7f3778", 37)
        if ret == 0:
            return None

        # 31010203
        self.socket_tx_flash(flash_socket, "16E2", "31010203")
        ret = self.resp_deal_flash(flash_socket, -10, -8, "31", "71", "7f3178", 31)
        if ret == 0:
            return None

        # 3101FF01
        self.socket_tx_flash(flash_socket, "16E2", "3101FF01")
        ret = self.resp_deal_flash(flash_socket, -10, -8, "31", "71", "7f3178", 33)
        if ret == 0:
            return None

        # 31010205
        self.socket_tx_flash(flash_socket, "16E2", "31010205")
        ret = self.resp_deal_flash(flash_socket, -10, -8, "31", "71", "7f3178", 33)
        if ret == 0:
            return None

        # 22F15C
        while True:
            time.sleep(5)
            self.socket_tx_flash(flash_socket, "16E2", "22F15C")
            ret = self.flash_F15C(flash_socket)
            if ret == 0:
                return None
            elif ret == 2:
                continue
            elif ret == 1:
                break
            else:
                pass

        # 1101
        self.socket_tx_flash(flash_socket, "16E2", "1101")
        ret = self.resp_deal_flash(flash_socket, -4, None, "1101", "5101", "7f1178", 100)
        if ret == 0:
            return None

        tkinter.messagebox.showwarning('警告', '刷写完成，请等待10mins，之后手动检查版本！！！')


#GUI
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Doip诊断工具@yc")
        self.resizable(False, False)
        self.geometry(str(WIDGHT_WIDTH) + "x" + str(WIDGHT_HEIGHT) + '+200+25')
        self.WidgetsInit()
        self.UDS = Diag()

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

        self._Second_dataflash = tk.LabelFrame(self._First_frame, height=110, width=590.5, text="诊断刷写-TBC")
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
        self.secuity9_button = tk.Radiobutton(self._Second_datainput, value=4, variable=self.secuitylevel_Radiobutton_v,
                                              text="9级", command=lambda: self.UDS.secuity_level_set())
        self.secuity9_button.grid(row=6, column=1, padx=2, pady=1, sticky=tk.E + tk.W)
        self.secuityB_button = tk.Radiobutton(self._Second_datainput, value=5, variable=self.secuitylevel_Radiobutton_v,
                                              text="B级", command=lambda: self.UDS.secuity_level_set())
        self.secuityB_button.grid(row=7, column=0, padx=2, pady=1, sticky=tk.E + tk.W)


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
        tk.Label(self._Second_dataflash, text='刷写进度:').grid(row=1, column=0, padx=5, pady=2.5, sticky=tk.E + tk.W)
        self.process_display = ttk.Progressbar(self._Second_dataflash, maximum=100, value=0, length=245, mode='determinate')
        self.process_display.grid(row=1, column=1, padx=5, pady=2.5)
        tk.Button(self._Second_dataflash, text='开始刷写', command=lambda: self.UDS.doip_falsh(self.path)).grid(row=1, column=2, padx=5, pady=5)
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
        global flash_file_path
        self.file_path.delete(0, END)
        path_ = tkinter.filedialog.askopenfilename()
        path_ = path_.replace("/", "\\\\")
        flash_file_path = path_
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " loginfo[data_file_path][1]：" + path_)
        self.path.set(path_)

    def data_delete(self):
        self.datainput_text.delete("1.0", END)
        self.datadisplay.delete("1.0", END)

if __name__=='__main__':
    demo = GUI()
    try:
        demo.mainloop()
    except Exception as e:
        demo.UDS.socket_disconect(global_socket)
        exit(0)
    finally:
        demo.UDS.socket_disconect(global_socket)
        exit(0)
