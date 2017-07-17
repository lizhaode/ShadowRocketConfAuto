import requests
import base64
import io
import os


class parsePAC():
    '''
    最终要生成一个文本文件，这个文件中包含所有代理规则，且规则的格式与ShadowRocket相符，即直接
    '''
    def getPAC(self):
        '''
        在tmp目录下，生成一个干净的，只存在PAC规则地址的文件，为下一步处理做准备
        '''
        gfwUrl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
        domainFile = 'tmp/allDomainFile.txt'
        if not os.path.exists('tmp'):
            os.mkdir('tmp')

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
                # 去除空行
                if not str.isspace(i):
                    domain.write(i)

    def wipeGoogle(self, domainString):
        '''
        去除PAC文件中含有Google的规则
        '''
        if 'google' in domainString:
            return None
        return domainString

    def addGoogle(self,file):
        '''
        在最终规则文件的末尾，增加一条匹配所有Google网站的规则
        '''
        with open(file,'a') as f:
            f.write('DOMAIN-KEYWORD,google,Proxy')

    def reutrnDomainList(self, file):
        with open(file) as f:
            for i in f.readlines():
                domainString = self.wipeGoogle(i)
                if not domainString:
                    pass


if __name__ == '__main__':
    parsePAC().getPAC()
