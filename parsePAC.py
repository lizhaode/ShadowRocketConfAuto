import requests
import base64
import io
import os
import shutil


class parsePAC():
    '''
    最终要生成一个文本文件，这个文件中包含所有代理规则，且规则的格式与ShadowRocket相符，即直接可以集成到最终的 ShadowRocket
    配置文件中
    '''

    def getPAC(self):
        '''
        在tmp目录下，生成一个干净的，只存在PAC规则地址的文件，为下一步处理做准备，文件名 allDomainFile.txt
        '''
        gfwUrl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
        pureGFWFile = 'tmp/GFW.txt'
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
            with open(pureGFWFile, 'a') as domain:
                # 去除空行
                if not str.isspace(i):
                    if self.wipeGoogle(i):
                        domain.write(self.wipeGoogle(i))
        # 复制一份，作为 DOMAIN 配置时使用
        shutil.copy(pureGFWFile, 'tmp/tmp.txt')

    def wipeGoogle(self, domainString):
        '''
        去除PAC文件中含有Google的规则
        '''
        if 'google' in domainString:
            return None
        return domainString

    def addGoogle(self, file):
        '''
        在最终规则文件的末尾，增加一条匹配所有Google网站的规则
        '''
        with open(file, 'a') as f:
            f.write('DOMAIN-KEYWORD,google,Proxy\n')

    def checkDuplicate(self, checkFile):
        '''
        去除文件中重复的内容
        '''
        f1 = open(checkFile)
        tmp = list(set(f1.readlines()))
        f1.close()
        with open(checkFile, 'w')as f:
            f.writelines(tmp)

    def reutrnDomainSuffixList(self, originalFile, domainSuffixFile):
        '''
        过滤PAC文件，生成 DOMAIN-SUFFIX 文件，文件名 domainSuffixFile.txt
        '''
        with open(originalFile) as f:
            for i in f.readlines():
                # 去掉末尾的换行符
                i = i.strip('\n')
                # 处理 || 开头的规则
                if i.startswith('||'):
                    domainSuffix = 'DOMAIN-SUFFIX,{url},PROXY\n'.format(url=i.strip('||'))
                    with open(domainSuffixFile, 'a') as file:
                        file.write(domainSuffix)
                # 处理 | 开头的规则
                elif i.startswith('|h'):
                    tmpDomain = i.split('/')[2]
                    # print(tmpDomain)
                    # 有的网址是www开头的，需要去掉 www
                    if 'www.' in tmpDomain:
                        tmp = tmpDomain.split('www.')[1]
                        domainSuffix = 'DOMAIN-SUFFIX,{url},PROXY\n'.format(url=tmp)
                        with open(domainSuffixFile, 'a') as file:
                            file.write(domainSuffix)
                    elif '*' in tmpDomain:
                        tmp = tmpDomain.split('*.')
                        if len(tmp) != 1:
                            domainSuffix = 'DOMAIN-SUFFIX,{url},PROXY\n'.format(url=tmp[1])
                            with open(domainSuffixFile, 'a') as file:
                                file.write(domainSuffix)
                # 处理 . 开头的规则
                elif i.startswith('.'):
                    tmp = i.split('/')[0].strip('.')
                    domainSuffix = 'DOMAIN-SUFFIX,{url},PROXY\n'.format(url=tmp)
                    with open(domainSuffixFile, 'a') as file:
                        file.write(domainSuffix)

        # 调用去重的方法，去除重复的数据
        self.checkDuplicate(domainSuffixFile)

    def returnDomainList(self, originalFile, domainFile):
        '''
        过滤PAC文件，生成 DOMAIN 文件，文件名 domain.txt
        在过滤规则之前，需要先去除 "||" , "|" , "." , "@" 开头的数据
        '''
        tmpFile = open(originalFile)
        tmpReadlines = tmpFile.readlines()
        tmpFile.close()
        allList = []
        for i in tmpReadlines:
            if i.startswith('||'):
                continue
            elif i.startswith('|h'):
                continue
            elif i.startswith('.'):
                continue
            elif i.startswith('@'):
                continue
            else:
                with open(originalFile, 'w')as f:
                    allList.append(i)
                    f.writelines(allList)
        # 开始创建 DOMAIN 规则文件
        with open(originalFile) as f:
            for i in f.readlines():
                i = i.strip('\n')
                domain = 'DOMAIN,{url},PROXY\n'.format(url=i)
                with open(domainFile, 'a') as file:
                    file.write(domain)
        # 去重
        self.checkDuplicate(domainFile)


if __name__ == '__main__':
    parsePAC().getPAC()
    parsePAC().reutrnDomainSuffixList('tmp/GFW.txt', 'tmp/domainSuffixFile.txt')
    parsePAC().returnDomainList('tmp/tmp.txt', 'tmp/domainFile.txt')
