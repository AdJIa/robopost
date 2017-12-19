'''
Created on 2017年10月13日

@author: LuJia
'''

import requests
from ProListUtil import ProListUtil
import random
import time
import pymysql

class Toutiao:

    proList = ProListUtil()
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    
    url = 'https://www.toutiao.com/api/pc/feed/?category=funny&utm_source=toutiao&tadrequire=true&max_behot_time='
    
    article_genre = 'article'

    tag = 'funny'

    ''' 递归查取数据 '''
    def recGetData(self, time, count, resData, proList):
        
        url = (self.url + '%s'%time)
        
        print(len(resData))
        
        response = requests.get(url, proxies={'http': random.choice(proList)}, headers=self.headers)
        
        status = response.status_code
        
        if status != 200:
            print(status)
            return resData
        
        res = response.json()
        
        if res['message'] == 'success':
            
            data = res['data']
            
            for obj in data:
                
                article_genre = obj.get('article_genre')
                source_url = obj.get('source_url')
                
                if source_url != None and article_genre != None and (article_genre == 'article'):
                    resData.append(source_url)
                    
            count = count - 1
            
            if count == 0:
                return resData
            
            time = res['next']['max_behot_time']

            return self.recGetData(time, count, resData, proList)
        else:
            return resData

    ''' 加载数据 '''
    def loadData(self):
        proList = self.proList.findIpsByRemote()
        resData = self.recGetData(0, 100, [], proList)
        setData = set(resData)
        ext = time.strftime('%Y%m%d', time.localtime())
        filePath = 'E:/jia/temp/db/urls/toutiao.' + ext

        urls = open(filePath, 'w')
        if setData != None:
            for url in setData:
                urls.write('https://www.toutiao.com' + url)
        urls.close()
        return setData

if __name__ == '__main__':
    toutiao = Toutiao()
    data = toutiao.loadData()

    db = pymysql.connect(host='qdm166276318.my3w.com', user='qdm166276318', db='qdm166276318_db', password='WOSHIlujia94', port=3306)
    cur = db.cursor()

    for o in data:

        sql = ("INSERT INTO funny (url) VALUES ('%s')" % ('https://www.toutiao.com' + o.replace('/group/', '/a')))
        print(sql)
        cur.execute(sql)
    db.commit()
    cur.close()
    db.close()
    pass
