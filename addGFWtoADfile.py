import requests

class addToAD():
    '''
    从 Shadowrocket-ADBlock-Rules 中提取广告过滤的规则，以合并到 ShadowRocket 规则中
    '''

    def __init__(self):
        '''
        获取最新的 sr_adb.conf
        '''
        sr_ad = 'https://raw.githubusercontent.com/h2y/Shadowrocket-ADBlock-Rules/master/sr_adb.conf'
        adFile = 'tmp/sr_adb.conf'
        adContent = requests.get(sr_ad).text
        with open(adFile,'w') as f:
            f.write(adContent)

    def delDuplicate(self,keyword,file):
        '''
        根据给定的关键字，去除文件中相同的内容
        '''
        f1 = open(file)
        compareTmp = f1.readlines()
        f1.close()
        with open(file,'w+') as f:
            writeList = []
            for i in compareTmp:
                if keyword in i:
                    continue
                else:
                    writeList.append(i)
            f.writelines(writeList)

    def delRulesFromFilebyKeyword(self):
        '''
        根据获取到的 DOMAIN-KEYWORD 过滤 domainFile.txt domainSuffixFile.txt
        '''
        keywordList = []
        with open('tmp/sr_adb.conf') as f:
            tmpFileContent = f.readlines()
            startIndex = tmpFileContent.index('#KEYWORD\n')
            endIndex = tmpFileContent.index('## END Proxy\n')
            content = tmpFileContent[startIndex + 1:endIndex]
            # 先获取 DOMAIN-KEYWORD 的列表
            for i in content:
                i = i.strip('\n')
                keywordList.append(i.split(',')[1])

        # 过滤 domainFile.txt 和 domainSuffixFile.txt
        for i in keywordList:
            self.delDuplicate(i,'tmp/domainFile.txt')
            self.delDuplicate(i,'tmp/domainSuffixFile.txt')

    def delRulesFromFilebySuffix(self):
        '''
        根据获取到的 DOMAIN-SUFFIX 过滤 domainFile.txt domainSuffixFile.txt
        '''
        keywordList = []
        with open('tmp/sr_adb.conf') as f:
            tmpFileContent = f.readlines()
            startIndex = tmpFileContent.index('## Proxy\n')
            endIndex = tmpFileContent.index('#Telegram\n')
            content = tmpFileContent[startIndex + 1:endIndex]
            # 先获取 DOMAIN-KEYWORD 的列表
            for i in content:
                i = i.strip('\n')
                keywordList.append(i.split(',')[1])

        # 过滤 domainFile.txt 和 domainSuffixFile.txt
        for i in keywordList:
            self.delDuplicate(i,'tmp/domainFile.txt')
            self.delDuplicate(i,'tmp/domainSuffixFile.txt')

if __name__ == '__main__':
    addToAD().delRulesFromFilebyKeyword()
    addToAD().delRulesFromFilebySuffix()