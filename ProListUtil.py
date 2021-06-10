import requests
from bs4 import BeautifulSoup
import json

class ProListUtil:

  #headers
  headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36'}

  #url
  url = 'https://ip.jiangxianli.com/api/proxy_ips'

  # get proxy ips by html process
  def findIpsByRemote(self):

    response = requests.get(self.url, headers=self.headers)
    response.encoding = response.apparent_encoding

    resData = json.loads(response.text)

    ips = resData.get("data").get("data");
    ipArr = []

    for x in range(1, len(ips)):
      ip = ips[x]
      ipArr.append(ip.get("ip"))

    return ipArr

if __name__ == '__main__':
  pro = ProListUtil()
  ips = pro.findIpsByRemote()
  print(ips)
#   https://github.com/jiangxianli/ProxyIpLib#%E5%85%8D%E8%B4%B9%E4%BB%A3%E7%90%86ip%E5%BA%93

