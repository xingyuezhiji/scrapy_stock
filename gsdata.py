import requests
from bs4 import BeautifulSoup as bs
headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
s = requests.Session()  # 可以在多次访问中保留cookie

cookie = {'Cookie':'acw_tc=AQAAACjPDG8L8QUATW9J32ip18u8+TEM; _csrf-frontend=e8984e72ae84dc81ac592102265449af469eea6618cf39edd1641bac4fa62245a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22cAFR19IVGgnZDprmj56ol3KAh3BnDVa9%22%3B%7D; bdshare_firstime=1528625461863; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1528625446,1528625555; _gsdataCL=WzEzNzE1MCwiMTU2MjI4OTAwNzkiLCIyMDE4MDYxMDE4MzIwOSIsIjVjOGRmOWFkNzEzZjhiZmE1ODEwNTI3OWZiMDNjZDEwIiwxMTU2Mzld; PHPSESSID=qnhdc713ltft57pvm26r6m9mb5; _identity-frontend=3734d755fd9d250ca9d6a8c081ad9a383bf8e0c41cda18c1946a3c538a18fecaa%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A27%3A%22%5B137150%2C%22test+key%22%2C2592000%5D%22%3B%7D; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1528627499'}
url = 'http://www.gsdata.cn/tool/ajaxwebpagecount'
url1 = 'http://www.gsdata.cn/oauth/getwxcachenotice'
a='http://www.gsdata.cn/member/login?url=http%3A%2F%2Fwww.gsdata.cn%2Ftool%2Fajaxwebpagecount'
payload = {'keyword': '马云'}
response = s.post(url1, {'username':'15622890079', 'password': '987456'}, headers=headers)
response1 = s.post(url, headers=headers,data=payload)
# try:
#     html_data = response.text.encode(response.encoding)
# except:
#     html_data = response.text

print(response1.text)
print(response1)
# soup = bs(html_data, 'lxml', from_encoding='utf-8')
# print(soup.get_text())