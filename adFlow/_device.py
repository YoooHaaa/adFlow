import frida
import os
import _stdout



class Device(object):
    
    def __init__(self):
        """
        function:  初始化获取设备对象和端口转发
        """
        self.session = None
        try:
            self.device = self.connect_device()
            if not self.device:
                raise Exception("Unable to connect.")
        except:
            self.forward_frida()
            self.device = self.connect_device()

        if not self.device:
            _stdout.Stdout.error("Device", "get_device",  "连接设备失败")
            exit()
        pass


    @classmethod
    def connect_device(cls, timeout=15):
        """
        function:  获取远程USB连接的设备对象
        """
        try:
            device = frida.get_usb_device(timeout=timeout)
        except Exception as err:
            _stdout.Stdout.error("Device", "connect_device", err)
        return device


    @classmethod
    def forward_frida(cls):
        """
        function:  自动完成端口转发
        """
        os.system("adb forward tcp:27042 tcp:27042")
        os.system("adb forward tcp:27043 tcp:27043")  


    def get_device(self):
        """
        function:  获取设备对象
        """
        return self.device

    