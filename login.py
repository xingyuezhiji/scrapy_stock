from urllib import request
import urllib
from bs4 import BeautifulSoup as bs
import requests
url = 'http://10.248.98.2/srun_portal_pc?ac_id=1&srun_wait=1&theme=basic1'
# url1 = 'http://www.baidu.com'
postdata = {
'callback': 'jQuery1124034510276262504913_1538974917232',
'action': 'login',
'username': '33316S051067',
'password': '{MD5}0bb357831ad768ea707f2f4c4e703654',
'ac_id': '1',
'ip': '10.249.180.136',
'chksum': '1a744d25a8446a42fee07b5fb51fcbf4481ccd4c',
'info': '',
'n': '200',
'type': '1',
'os': '',
'name': '',
'double_stack': '0',
'_': '1538974917235'
}
session = requests.session()
postdata = urllib.parse.urlencode(postdata)
response = session.get(url,params=postdata)
print(response.text)

# print(postdata)
# response = request.Request(url=url,data=postdata)
# print(response)

openner = request.build_opener()
openner.open(response)
# try:
#     html_data = response.text.encode(response.encoding)
# except:
#     html_data = response.text
#
# # print(html_data)
# soup = bs(html_data, 'lxml', from_encoding='utf-8')
# print(soup)

