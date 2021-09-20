import os
import frida
import _thread
import _device
import getopt 
import sys
import _process
import _flow
import time
import _stdout
import json



def on_message(message, data):
    """
    function:  消息回调，用于接收并处理JS中发送的流量信息
    """
    if message['type'] == 'send':
        #print("获取到流量")
        if message['payload'][:7] == 'flow:::':
            jsonpacket = json.loads(message['payload'][7:])
            _flow.Flow().exec(jsonpacket)
    else:
        #print("*****[frida hook]***** : " + str(message))
        pass


def show_banner():
    print("   *********************************************************************")
    print("   ***************             FRIDA   RUN            ******************")
    print("   *********************************************************************")
    pass

def show_help():
    tips = "\n*******************************************************************************\n" \
           "    本工具为自动抓取应用中广告流量明文的工具，用户开启后，根据消息提示选择相应\n" \
           "的包名进行hook即可，获取的流量会自动保存在flow文件夹下对应的以包名命名的txt文\n" \
           "件中\n" \
           "*******************************************************************************\n"
    print("\033[32m" + tips + "\033[0m")
    pass

def get_system() -> list:
    """
    function:  返回系统应用包名，用于排除hook
    """
    list_system = ["com.miui.home", "com.lbe.security.miui", "com.miui.securitycenter"]
    return list_system

def choose_hook(oldpkg, pkgname):
    """
    function:  返回系统应用包名，用于排除hook
    param:     oldpkg -> 正处于hook的包名  pkgname -> 可hook的包名
    """
    if pkgname in get_system():
        return False
    while True:
        if oldpkg == "":
            choose = input('确定要hook -> ' + pkgname + "  y / n")
        else:
            choose = input('确定要hook -> ' + pkgname + "  y / n  该操作将丢失对 [" + oldpkg + "] 的hook")

        sys.stdout.flush()
        if  choose == 'n':
            return False
        elif choose == 'y':
            return True


def entry():
    """
    function:  主功能函数
    """
    _pgkname_ = ""
    process = None
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h")
        for arg, value in opts:
            if arg == '-h':
                show_help()
                exit(0)
    except getopt.GetoptError:
        show_help()
        exit(2)

    device = _device.Device().get_device()
    process = _process.Process(device=device, pkgname=_pgkname_)

    if not os.path.exists("./flow"):
        os.mkdir("./flow")

    show_banner()

    while True:
        print("running......")
        time.sleep(1)
        cpkgname = process.get_current_pkg()
        if cpkgname == "" :
            continue

        if _pgkname_ == "": #第一次hook
            if not choose_hook(_pgkname_, cpkgname):
                continue
            _pgkname_ = cpkgname
            process = _process.Process(device=device, pkgname=_pgkname_)
            process.onload()
            _stdout.Stdout.info("hooking -> [ " + cpkgname + " ]")
        else:
            if _pgkname_ != cpkgname: #已切换应用
                if not choose_hook(_pgkname_, cpkgname):
                    continue
                _pgkname_ = cpkgname
                process.unload()
                process = _process.Process(device=device, pkgname=_pgkname_)
                process.onload()
                _stdout.Stdout.info("hooking -> [ " + cpkgname + " ]")
 

if __name__ == "__main__":
    entry()


