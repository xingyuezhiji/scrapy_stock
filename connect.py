from urllib import request
import urllib
from bs4 import BeautifulSoup as bs
import requests

class Loginer():
    def __init__(self, username, password):
        self.loginUrl = 'http://10.248.98.2/srun_portal_pc?ac_id=1&srun_wait=1&theme=basic1'
        self.username = username
        self.password = password
        self.openner = request.build_opener()

    def login(self):
        postdata = {
            'username': self.username,
            'password': self.password,
            'action': 'login',
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
        postdata = urllib.parse.urlencode(postdata)
        myRequest = request.Request(url=self.loginUrl, data=postdata)

        result = self.openner.open(myRequest).read()
        resStr=str(result)
        ind=resStr.find('font-weight:bold;color:orange')
        if(ind!=-1):
            print ('connected successfully' )
        else:
            print ('connected faild!! Maybe your username or password is wrong!')

def main():
    username=input('Enter your username:')
    password=input('Enter your password:')
    file=open('temp_username.dat','w')
    file.write(username)
    file.close()
    l = Loginer(username,password)
    l.login()

if __name__ == '__main__':
    main()
    print ('done')

