import requests
import random
import json
from ProListUtil import ProListUtil



if __name__ == '__main__':

  proUtil = ProListUtil()

  print('start.......')

  pro = proUtil.findIpsByRemote()

  print('proxy ip list : %s' % pro)

  headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36'}

  print('request heads : %s' %headers)

  url = 'https://m.toutiao.com/list/?tag=news_story&ac=wap&count=20&format=json_raw&as=A1A599CCDF74D90&cp=59CFF4FD59D04E1&min_behot_time=1506758030'

  print('request url : %s'%url)

  request = requests.get(url, proxies={'http': random.choice(pro)}, headers=headers)

  request.encoding = request.apparent_encoding

  res = request.text

  if res != "":
    print('request data : %s'%res)
    print(json.loads(request.text)['return_count'])




