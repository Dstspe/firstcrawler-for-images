# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:45:10 2017

@author: Fan
"""
"""
一个翻页抓图并保存的小爬虫，连续命名保存图片。
"""

from bs4 import BeautifulSoup
import os
import requests
import re
import datetime

def downloadImg(url, m, n):    #m为起始页，n为末页

    os.chdir(r'E:\****')   #保持在当前目录
    t = 1  # 记录图片张数
    headers = {'User-Agent':  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}    
        
    for i in range(n-m+1):  #自动翻页,i的起始值是0
        html_doc = requests.get(url + '/page/' + str(m+i), headers = headers)   # m+i为起始页
        soup = BeautifulSoup(html_doc.text, "lxml")     #转换成bs，记得带.text
        
        for myimg in soup.find_all('div', class_="featured-image"): #find_all返回list，遍历时是单个元素，用find返回dict，然后查找['src']
            pic_name = str(m+i)+ '-' + str(t) + '.jpg'              #按顺序命名图片，从1开始                                                                       
            try:                                
                img_src = myimg.find('img')['src']     #定位，用find_all输出带标签的list.
                                         #遍历list元素后为dict，找出'img'标签下的class_='src',也可用find('img').get('src')
                img_st = re.split('-\d{3}x\d{3}', img_src)  #将图片改为原图的格式,即切除-400x300的小图片部分
                img_src_o = img_st[0] + img_st[1]    #重新将切开原图与其后缀如'.jpg','.png'连接起来
            except IndexError:
                img_src_o = img_src             #部分图片无400x300格式，无法切割时弹IndexError，遇到该情况时跳过切割直接下载图片
            except TypeError:
                pass                            #部分src输出为空，跳过
            
            get_img = requests.get(img_src_o, headers = headers)         #打开，用requests.get来打开定位的图片            
            with open(pic_name, 'wb') as pic:       #保存图片，'wb'模式打开再保存
                pic.write(get_img.content)            
                print("Success!" + pic_name)
                t += 1                                  #保存完一张后t+1
        print("Next is page: " + str(m+i+1) + '!')

starttime = datetime.datetime.now()

if __name__ == '__main__':    #仅在本文件中进行
    downloadImg(url, 1, 110)
    endtime = datetime.datetime.now()
    total_time = endtime - starttime
    print('用时： ' + str(total_time))  #计时
