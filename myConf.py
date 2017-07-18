import parsePAC,addGFWtoADfile


if __name__ == '__main__':
    getPAC = parsePAC.parsePAC()
    getPAC.returnDomainList()
    getPAC.reutrnDomainSuffixList()

    add = addGFWtoADfile.addToAD()
    add.delRulesFromFilebyKeyword()
    add.delRulesFromFilebySuffix()

    f1 = open('tmp/sr_adb.conf')
    tmp = f1.readlines()
    f1.close()

    suffixStartIndex = tmp.index('## Proxy\n') + 1
    suffixEndIndex = tmp.index('#Telegram\n')

    startConf = tmp[:suffixStartIndex]
    endConf = tmp[suffixEndIndex:]

    domainSuffix = open('tmp/domainSuffixFile.txt')
    domain = open('tmp/domainFile.txt')
    middleConf = domainSuffix.readlines() + domain.readlines()
    domainSuffix.close()
    domain.close()

    completeConf = startConf + middleConf + endConf

    completeConf.remove('DOMAIN-SUFFIX,cn,DIRECT\n')
    completeConf.remove('GEOIP,CN,DIRECT\n')
    completeConf.remove('[URL Rewrite]\n')
    completeConf.remove('^http://(www.)?google.cn https://www.google.com header\n')

    with open('myConf.conf','w') as f:
        f.writelines(completeConf)