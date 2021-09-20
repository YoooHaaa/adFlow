import colorama
from colorama import init,Fore,Back,Style
init(autoreset=True)


class Stdout(object):
    _label_info_start:str = "\033[32m"
    _label_end:str = "\033[0m"
    _label_error_start:str = "\033[31m"
    _label_warn_start:str = "\033[33m"

    @classmethod
    def info(cls, info):
        print(cls._label_info_start + "[+++++++++] -->> " + info + cls._label_end)
        pass
        
    @classmethod #调试版
    def error(cls, clas:str, func:str, err:str):
        print(cls._label_error_start + "[---------] -->> " + "[ " + clas + " -> " + func + " ] " + err + cls._label_end)
        pass

    @classmethod
    def warning(cls, warn):
        print(cls._label_warn_start + "[---------] -->> " + warn + cls._label_end)
        pass
"""
    @classmethod #发布版
    def error(cls, clas, func, err):
        print(cls._label_error_start + "[---------] -->> " + "[ " + err + " ]" + cls._label_end)
        pass
"""