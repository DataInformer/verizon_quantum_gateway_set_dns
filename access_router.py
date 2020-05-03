import json
import requests
import urllib3
import hashlib
from getpass import getpass
from http.cookies import SimpleCookie


class router_session:
    # establishes connection to router, can be used to view or change settings

    def __init__(self, host='https://myfiosgateway.com', verify=False, password=None):
        # if you want to set verify to True, you'll need to install the router's self-signed certificate
        # make sure the host really is your fios router
        self.verify = verify
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.host = host
        self.sess = requests.Session()
        r = self.sess.get(host + '/api', verify=verify)
        pwd_salt = r.json()['passwordSalt']
        if password is None:
            password = getpass()

        encoded_pwd = hashlib.sha512()
        encoded_pwd.update((password + pwd_salt).encode('ascii'))
        payload = json.dumps({'password': encoded_pwd.hexdigest()})
        print('Establishing connection...')
        res = self.sess.post(host + '/api/login', data=payload, verify=verify)
        print('Status: ', res)
        token = SimpleCookie(res.headers.get('set-cookie'))['XSRF-TOKEN'].value
        self.sess.headers.update({'X-XSRF-TOKEN': token})
        r = self.sess.get(host + '/api/devices', verify=verify)
        if r.status_code == 200:
            print('Connected')
        else:
            print(r)
        print('--------------------------------------------------------------------------')
    def remove_backup_dns(self):
        payload = json.dumps({"staticSecondaryDnsServer": "0.0.0.0"})  # invalid, so like removing
        r = self.sess.put(self.host + '/api/network/1', data=payload, verify=self.verify)
        return (r, r.json())

    def restore_backup_dns(self, dns_ip='1.1.1.1'): # default is cloudflare
        payload = json.dumps({"staticSecondaryDnsServer": dns_ip})
        r = self.sess.put(self.host + '/api/network/1', data=payload, verify=self.verify)
        return (r, r.json())