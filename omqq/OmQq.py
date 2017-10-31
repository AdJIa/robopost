import requests
import json
import hashlib
import mimetypes
import uuid
import os

class Omqq:

  session = requests.Session()

  headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36'}

  imagesPath = 'E:/jia/temp/images/'

  phone = '***'

  password = '***'

  #pro password
  #MD5(a.token + MD5(a.salt + d))
  def login(self):

    randomCode = self.getRandomCode()

    token = randomCode['token']
    salt = randomCode['salt']

    saltpwd = self.md5Encode(salt + self.password)

    pwd = self.md5Encode(token + saltpwd)

    loginData = {}
    loginData['phone'] = self.phone
    loginData['pwd'] = pwd
    loginData['token'] = token

    url = 'https://om.qq.com/userAuth/signInViaPhone?relogin=1'

    request = self.session.post(url, loginData)

    res = json.loads(request.text)['response']['code']

    if json.loads(request.text)['response']['code'] == 0:
      print('login success')
    else:
      print('login error')

  def getRandomCode(self):

    url = 'https://om.qq.com/userAuth/getPhoneRandomCode?phone=' + self.phone + '&relogin=1'

    request = self.session.get(url, headers=self.headers)

    jsonData = json.loads(request.text)

    if jsonData['response']['code'] == '0':
      print("getRandomCode success : %s "%jsonData['data'])
    else:
      print("getRandomCode error : %s"%jsonData['reponse']['msg'])

    return jsonData['data']

  def md5Encode(self, strs):
    m = hashlib.md5()
    m.update(strs.encode())
    return m.hexdigest()

  def downLoadImage(self, path):

    response = requests.get(path)
    exts = mimetypes.guess_all_extensions(response.headers['Content-Type'])

    ext = ''
    if len(exts) > 1:
      ext = exts[1]
    else:
      ext = exts[0]

    name = uuid.uuid4().hex

    filePath = 'E:/jia/temp/images/' + name + ext

    img = open(filePath, 'wb')
    img.write(response.content)
    img.close()

    return filePath

  def uploadImages(self, filePath):
    url = 'https://om.qq.com/image/archscaleupload?isRetImgAttr=1&relogin=1'
    files = {'Filedata': open(filePath, 'rb')}
    respone = self.session.post(url, files=files)
    res = respone.json()
    if res['response']['code'] != 0:
      print('文件上传失败！')
    return res['data']

  def imageInfoNoWater(self, urls):
    data = {'url': urls}
    url = 'https://om.qq.com/image/imageInfoNoWater?relogin=1'
    response = self.session.post(url, data)
    res = response.json()
    maxW = 240
    maxH = 160

    rurls = []
    for url in res['data']:
      urlObj = res['data'][url]
      if '1' != urlObj['isqrcode'] and '1' != urlObj['itype']:
        img10 = urlObj['img']['imgurl0'] or {}
        if img10['width'] >= maxW and img10['height'] >= maxH:
          rurls.append(urlObj['img']['imgurl640']['imgurl'])

    return rurls

  def exactupload(self, picUrl):
    url = 'https://om.qq.com/image/exactupload?relogin=1'
    data = {'url': picUrl, 'opCode': 151, 'isUpOrg': 1, 'subModule': 'normal_cover'}
    response = self.session.post(url, data)
    res = response.json()
    if res['response']['code'] != 0:
      print('获取失败')
    res['data']['src'] = picUrl

    return [res['data']]

  def publish(self, data):

    title = data['title']

    imgurl_ext = []
    content = ''

    imgUrls = ''
    for index, img in enumerate(data['imgs']):
      imgObj = img

      picUrl = imgObj['url']
      picDesc = imgObj['desc']

      filePath = self.downLoadImage(picUrl)
      uploadRes = self.uploadImages(filePath)
      picUrl = uploadRes['url']['size']['641']['imgurl']

      imgUrls += ',' + picUrl

      if index == 0:
        content += '<p class="">'
        content += ('<p style="margin-bottom:1px;padding-bottom:1px;" class="empty"><img src="%s" desc="%s"/></p><p type="om-image-desc" class="">%s</p>'%(picUrl, picDesc, picDesc))
        content += '</p>'
      else:
        content += ('<p style="margin-bottom:1px;padding-bottom:1px;" class="empty"><img src="%s" desc="%s"/></p><p type="om-image-desc" class="">%s</p>'%(picUrl, picDesc, picDesc))

    urls = self.imageInfoNoWater(imgUrls[1:])

    if len(urls) > 0:
      imgurl_ext = self.exactupload(urls[0])

    form_data = self.createFromData({'title': title, 'imgurl_ext': imgurl_ext, 'content': content})

    print(form_data)

    url = 'https://om.qq.com/article/publish?relogin=1'

    response = self.session.post(url, form_data)

    print(response.json())


  def createFromData(self, data):
    form_data = {}
    form_data['title'] = 'test111'
    form_data['title2'] = ''
    form_data['tag'] = ''
    form_data['video'] = ''
    form_data['cover_type'] = -1
    form_data['imgurl_ext'] = data['imgurl_ext']
    form_data['category_id'] = 82
    form_data['content'] = data['content']
    form_data['orignal'] = 0
    form_data['user_original'] = 0
    form_data['music'] = ''
    form_data['activity'] = ''
    form_data['apply_olympic_flag'] = 0
    form_data['apply_push_flag'] = 0
    form_data['apply_reward_flag'] = 0
    form_data['reward_flag'] = 0
    form_data['survey_id'] = ''
    form_data['survey_name'] = ''
    form_data['type'] = 0
    form_data['commodity'] = ''
    form_data['pushInfo'] = ''
    form_data['articleId'] = ''
    form_data['temp'] = ''
    form_data['video_source_data'] = ''
    return form_data

if '__main__' == __name__:
  data = {'title': '右边的小箭头，看到你了，想单独自拍的心思我已经看穿了', 'imgs': [{'url': 'http://inews.gtimg.com/newsapp_bt/0/2119796435/641', 'desc': '魔方达人'}, {'url': 'https://p3.pstatp.com/large/3e650000f06bae90047f', 'desc': '魔方达人'}, {'url': 'http://inews.gtimg.com/newsapp_bt/0/2134593674/641', 'desc': '魔方达人'}]}
  omqq = Omqq()
  omqq.login()
  # filePath = omqq.downLoadImage('https://p3.pstatp.com/origin/3e7a00120400bcb4ca29')
  # res = omqq.uploadImages(filePath)
  # imgurl = res['url']['size']['641']['imgurl']
  # exactuploadRes = omqq.exactupload(imgurl)
  # print(exactuploadRes)
  omqq.publish(data)

