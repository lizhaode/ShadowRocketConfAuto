import parsePAC, addGFWtoADfile

if __name__ == '__main__':
    # 获取 GFWlist ，提取相关规则
    getPAC = parsePAC.parsePAC()
    getPAC.returnDomainList()
    getPAC.reutrnDomainSuffixList()
    # 将提取的规则与 ad 规则去重
    add = addGFWtoADfile.addToAD()
    add.delRulesFromFilebyKeyword()
    add.delRulesFromFilebySuffix()
    # 将 ad 读取到内存中，为下一步的拼接做准备
    f1 = open('tmp/sr_adb.conf')
    completeConf = f1.readlines()
    f1.close()
    # 提取规则注入的位置
    suffixAddIndex = completeConf.index('#Telegram\n')

    # 拼接从 GFWlist 获取到的规则
    domainSuffix = open('tmp/domainSuffixFile.txt')
    domain = open('tmp/domainFile.txt')
    middleConf = domain.readlines() + domainSuffix.readlines()
    domainSuffix.close()
    domain.close()
    # 拼接完整的规则
    for i in middleConf:
        completeConf.insert(suffixAddIndex, i)
    # 去掉原 ad 规则中，末尾的一些不会生效的规则
    completeConf.remove('DOMAIN-SUFFIX,cn,DIRECT\n')
    completeConf.remove('GEOIP,CN,DIRECT\n')
    completeConf.remove('[URL Rewrite]\n')
    completeConf.remove('^http://(www.)?google.cn https://www.google.com header\n')
    completeConf.remove('IP-CIDR,192.168.0.0/16,DIRECT\n')
    completeConf.remove('IP-CIDR,10.0.0.0/8,DIRECT\n')
    completeConf.remove('IP-CIDR,172.16.0.0/12,DIRECT\n')
    completeConf.remove('IP-CIDR,127.0.0.0/8,DIRECT\n')

    # 在规则 IP-CIDR 末尾添加 ,no-resolve 规则
    copyCompleteConf = completeConf
    for i in copyCompleteConf:
        if 'IP-CIDR' in i:
            replaceIndex = completeConf.index(i)
            i = i.strip('\n')
            i = i + ',no-resolve\n'
            completeConf[replaceIndex] = i




    # 将规则写入 myConf.conf 文件中
    with open('myConf.conf', 'w') as f:
        f.writelines(completeConf)
