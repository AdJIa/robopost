import requests
from bs4 import BeautifulSoup

class ProListUtil:

  #headers
  headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36'}

  #url
  url = 'http://www.xicidaili.com/nn/'

  # get proxy ips by html process
  def findIpsByRemote(self):

    request = requests.get(self.url, headers=self.headers)
    request.encoding = request.apparent_encoding

    soup = BeautifulSoup(request.text, "html5lib")
    ips = soup.findAll("tr")

    ipArr = []

    for x in range(1, len(ips)):
      ip = ips[x]
      tds = ip.findAll("td")
      ipArr.append("%s:%s" % (tds[1].contents[0], tds[2].contents[0]))

    return ipArr

if __name__ == '__main__':
  pro = ProListUtil()
  ips = pro.findIpsByRemote()
  print(ips)

