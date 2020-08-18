#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib.request as ur
import lxml.etree as le
import socket
import ssl

#解决报错：certificate verify failed: unable to get local issuer certificate (_ssl.c:1045)>
ssl._create_default_https_context = ssl._create_unverified_context

request1 = ur.Request('https://mp.weixin.qq.com/s/oLwL5NOkVN3DQzy3QZs-Qg',
                     headers={
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'})
response1 = ur.urlopen(request1).read()
text1 = le.HTML(response1).xpath('//*[@id="img-content"]//p/span/text()')
DOI_list = list(filter(lambda x: re.match(r'^\d[0-9a-zA-Z\-_./]{15,100}',x) != None, text1))
print(DOI_list)

download_list = []
for i in DOI_list:

    request2 = ur.Request('https://sci-hub.st//'+i,
                          headers={
                              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'})
    response2 = ur.urlopen(request2).read().decode('utf-8')

    download_link = re.findall(r'<a.*?</a>', response2)
    # print(download_link)
    link = download_link[1]
    # print(link)
    Good_link = re.search(r'href=\'(.*?)\'\">', link)
    # Good_link = re.findall(r'',link)
    Last_dlink = Good_link.group(1)
    # print(Last_dlink)
    download_list.append(Last_dlink)
print(download_list)


#进行文件下载
for m in download_list:
    url = 'http:' + m
#解决文件下载不完成的error
    try:
        ur.urlretrieve(url,filename='./%s.pdf' %(x for x in DOI_list))
    except socket.timeout:
        count = 1
        while count <= 5:
            try:
                ur.urlretrieve(url,filename='./%s.pdf' %(x for x in DOI_list))
                break
            except socket.timeout:
                err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
                print(err_info)
                count += 1
        if count > 5:
            print("downloading file fialed!")


print("downloading complete!!")

# request3 = ur.Request(url,
#                       headers={
#                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'})
# response3 = ur.urlopen(request3,context=context).read()
# with open ('10.1126/science.aaz5626#','wb') as f:
#     f.write(response3)
