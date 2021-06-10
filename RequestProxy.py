import requests
import random
import json
from ProListUtil import ProListUtil
from bs4 import BeautifulSoup

import urllib.parse as urlparse



if __name__ == '__main__':

  proUtil = ProListUtil()

  print('start.......')

  # pro = proUtil.findIpsByRemote()

  # print('proxy ip list : %s' % pro)

  headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36'}

  print('request heads : %s' %headers)

  url = 'https://m.ke.com/cq/xiaoqu/c3611099972231/?sug=%E8%9E%8D%E5%9F%8E%E5%8D%8E%E5%BA%9C'

  print('request url : %s'%url)

  # request = requests.get(url, proxies={'http': random.choice(pro)}, headers=headers)
  request = requests.get(url, headers=headers)

  request.encoding = request.apparent_encoding

  soup = BeautifulSoup(request.text, "html.parser")
  taga = soup.select("li.pictext a")

  for x in range(1, len(taga)):
    a = taga[x]
    href = a.get("href")
    dataaction = a.get("data-action")
    querys = urlparse.parse_qs(dataaction)




