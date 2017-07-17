import requests
import base64
import io


class parsePAC():


    def getPAC(self):
        gfwUrl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
        gfwFile = 'gfwlist.txt'
        domainFile = 'domainFile.txt'

        gfwBase = requests.get(gfwUrl).text
        gfwList = base64.b64decode(gfwBase).decode('UTF-8')

        # io库可以将字符串加载成 File 类型，便于处理
        originalGFW = io.StringIO(gfwList)

        # 清除掉PAC文件中头部和尾部无用的内容
        for i in originalGFW.readlines():
            # 以 "!" 开头的是注释，文件开头的 "[]"
            if i.startswith('!') or i.startswith('['):
                continue
            with open(domainFile, 'a') as domain:
                if not str.isspace(i):
                    domain.write(i)




if __name__ == '__main__':
    parsePAC().getPAC()