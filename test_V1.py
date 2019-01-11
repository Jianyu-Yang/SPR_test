from selenium import webdriver
from lxml import etree
import requests
import time
import os
from tqdm import tqdm,trange
import datetime
from bs4 import BeautifulSoup


time_start = time.time()
global root_path
root_path=os.path.dirname(os.path.realpath(__file__))
#root_path=root_path[0]
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
root_url='https://www.mgstage.com/search/search.php?monthly_limit=0&is_monthly=0&sort=popular'

def get_movie_ulrs(root_url):
    global browser
    browser = webdriver.Chrome()
    browser.get(root_url)
    botton = browser.find_element_by_id('AC')
    botton.click()
    # print(browser.page_source)
    html = etree.HTML(browser.page_source)
    # html=etree.tostring(html)
    # print(result.decode('utf-8'))

    movie_urls = html.xpath('//*[@id="center_column"]/div[2]/div/ul/li/a/@href')
    only_movie_urls=[]
    for n in range(len(movie_urls)):
        movie_urls[n] = movie_urls[n][24:-1]
        if os.path.exists(os.path.join(root_path,movie_urls[n])):
            print('文件%s已存在！'%movie_urls[n])
        else:
            only_movie_urls.append( 'https://www.mgstage.com/product/product_detail/' + movie_urls[n] + '/')

    print(only_movie_urls)
        #movie_urls[n]='https://www.mgstage.com'+movie_urls[n]
    return only_movie_urls

def get_img_urls(movie_url):
    # global browser
    # browser=webdriver.Chrome()
    # browser.get(movie_url)
    # botton=browser.find_element_by_id('AC')
    # botton.click()
    # #print(browser.page_source)
    # html=etree.HTML(browser.page_source)
    #html=etree.tostring(html)
    #print(result.decode('utf-8'))

    #browser.execute_script('windows.open()')
    #browser.switch_to.window(browser.window_handles[1])
    browser.get(movie_url)
    html = etree.HTML(browser.page_source)
    movie_id=html.xpath('//*[@id="center_column"]/div[1]/div[1]/div/table[2]/tbody//th[text()="品番："]/following-sibling::td[1]/text()')
    print(movie_id)
    movie_id=movie_id[0]

    os.mkdir(root_path+'\\'+movie_id)
    os.chdir(root_path+'\\'+movie_id)
    cover_img_url=html.xpath('//*[@id="EnlargeImage"]/@href')
    #print(cover_img_url)
    sample_img_urls=html.xpath('//*[@id="sample-photo"]//a/@href')
    sample_img_urls=cover_img_url+sample_img_urls
    #print(sample_img_urls)
    sample_img_urls = tqdm(sample_img_urls,mininterval=0.01,unit_scale=1,ncols=60)
    #browser.close()
    #browser.switch_to.window(browser.window_handles[0])
    return movie_id,sample_img_urls

def download_sample_imgs(sample_img_urls,headers,i=0):
    time_download_imgs_start=time.time()
    for sample_img_url in sample_img_urls:
        i=str(i)
        sample_img_urls.set_description("正在下载第%s张图片"%i)
        img=requests.get(sample_img_url,headers=headers)
        f=open(i+'.jpg','ab')
        f.write(img.content)
        f.close()
        i=int(i)
        i=i+1
    return i,datetime.timedelta(seconds=time.time() - time_download_imgs_start)

def log_output(movie_id,img_num,time_download_imgs):
    log_infor = ['movie_id:', '', 'img_num:', '', 'time:', '', '#' * 20]
    log_infor[1] = movie_id
    log_infor[3] = str(img_num)
    log_infor[5] = str(time_download_imgs)
    print(log_infor)
    os.chdir(root_path)
    fh = open('download_log.txt', 'a+', encoding='utf-8')
    fh.write(log_infor[6] + '\n' + log_infor[0] + log_infor[1] + '\n' + log_infor[2] + log_infor[3] + '\n' + log_infor[4] + log_infor[5] + '\n')
    fh.close()

movie_urls=get_movie_ulrs(root_url)
#global browser
#browser.execute_script('windows.open()')
#browser.switch_to.window(browser.window_handles[1])
for movie_url in movie_urls:
    movie_id,sample_img_urls=get_img_urls(movie_url)
    img_num,time_download_imgs=download_sample_imgs(sample_img_urls,headers)
    log_output(movie_id,img_num,time_download_imgs)
print('程序运行时间：',datetime.timedelta(seconds=time.time() - time_start))

browser.close()