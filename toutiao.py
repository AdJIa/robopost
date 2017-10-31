'''
Created on 2017年10月13日

@author: LuJia
'''

import requests
from ProListUtil import ProListUtil
import random

class Toutiao:

    proList = ProListUtil()
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    
    url = 'https://www.toutiao.com/api/pc/feed/?category=funny&utm_source=toutiao&tadrequire=true&max_behot_time='
    
    article_genre = 'article'

    tag = 'funny'

    ''' 获取组图数据 '''
    def getZutu(self, time, count, resData, proList):
        
        url = (self.url + '%s'%time)
        
        #print(url)


        
        response = requests.get(url, proxies={'http': random.choice(proList)}, headers=self.headers)
        
        status = response.status_code
        
        if status != 200:
            return resData
        
        res = response.json()
        
        if res['message'] == 'success':
            
            data = res['data']
            
            for obj in data:
                
                article_genre = obj.get('article_genre')
                tag = obj.get('tag')
                source_url = obj.get('source_url')
                
                if source_url != None and article_genre != None and (article_genre == self.article_genre or article_genre == 'article'):
                    resData[source_url] = obj
                    
            count = count - 1
            
            if count == 0:
                return resData
            
            time = res['next']['max_behot_time']
            
            return self.getZutu(time, count, resData, proList)
    
if __name__ == '__main__':
    toutiao = Toutiao()
    proList = toutiao.proList.findIpsByRemote()
    resData = toutiao.getZutu(0, 10, {}, proList)
    print(resData)
    pass