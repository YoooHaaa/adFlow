
# 对传入的流量进行写文件等操作
import _stdout
import os
import datetime
import json
import main

class Flow(object):
    _PKG_PATH:str = ""


    def __init__(self):
        pass
    

    @classmethod
    def exec(cls, flow):
        """
        function:  用户调用此函数并传入流量，可完成流量的自动解析和写文件
        """
        pkgname, sdk, data, stack = cls._parse(flow)
        cls._save("./flow/" + pkgname + ".txt", sdk, data, stack)


    @classmethod
    def _parse(cls, flow):
        """
        function:  将拼接的流量解析成三段
        param:     flow -> 拼接的流量
        ret：      包名 + sdk + 流量 + 栈
        """
        try:
            return flow['pkgname'], flow['sdk'], flow['data'], flow['stack']
        except Exception as err:
            _stdout.Stdout.error("Flow", "_parse_data", str(err))
            _stdout.Stdout.warning(flow)
            return "", "", "", ""


    @classmethod
    def _save(cls, files:str, sdk:str, data:str, stack:str):
        """
        function:  将分段的流量数据保存文件
        param:     文件名 + sdk + 广告体 + 调用栈
        """
        try:
            #print("file = " + files)
            with open(files, "a", encoding='utf-8') as flows:
                flows.write("\n")
                flows.write("*****************************************" + sdk + "*****************************************")
                flows.write("\n")
                flows.write(str(datetime.datetime.now()))
                flows.write("\n")
                flows.write(data)  #json.loads:str-> json.  json.dumps:json -> str
                flows.write("\n")
                flows.write(stack)
                flows.write("\n")
                flows.write("***********************************************************************************************")
        except Exception as err:
            _stdout.Stdout.error("Flow", "_save", str(err))





