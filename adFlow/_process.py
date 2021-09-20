import frida
import _stdout
import _flow
import main
import time


class Process(object):
    _pid = None
    _pkgname = None
    _session = None
    _script = None
    _device = None


    def __init__(self, device, pkgname=""):
        self._init(device, pkgname)
        pass


    @classmethod
    def _init(cls, device, pkgname):
        cls._pkgname = pkgname
        cls._device = device
        pass


    @classmethod
    def onload(cls):
        """
        function:  完成应用的重启，附加，JS脚本注入
        """
        try:
            cls.pid = cls._device.spawn(cls._pkgname)
            cls._device.resume(cls.pid)
            while True: # 每秒获取一次session 直至成功
                try:
                    time.sleep(0.5)
                    cls.session = cls._device.attach(cls.pid)
                except:
                    continue
                break
            
            with open("hook.js", "r", encoding='utf-8') as f:
                cls.script = cls.session.create_script(f.read())
            cls.script.on("message", main.on_message) 
            cls.script.load()
            cls.script.exports.initjs(cls._pkgname)
        except Exception as err:
            _stdout.Stdout.error("Process", "onload", str(err) )
            exit(2)

    @classmethod
    def unload(cls):
        """
        function:  释放script 和 session的资源
        """
        try:
            cls.script.unload()
            cls.session.detach()
        except:
            pass


    @classmethod
    def get_current_pkg(cls):
        """
        function:  获取当前正在运行的应用的包名
        param:     设备
        ret：      包名
        """
        try:
            target = cls._device.get_frontmost_application() #获取最前端Activity所在进程identifier
            return target.identifier
        except Exception as err:
            _stdout.Stdout.error("Process", "get_current_pkg", str(err))
            return ""







