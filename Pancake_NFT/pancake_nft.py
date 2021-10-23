
import json
import requests
import chardet
from web3 import Web3
from bs4 import BeautifulSoup as BS4

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BSC_API = "https://api.bscscan.com/api"
CONTRACT_ADDRESS = "0x0a8901b0E25DEb55A87524f0cC164E9644020EBA"
NFT_COOKIE_PATH = "./Pancake_NFT/nft_cookie.txt"

def get_Cookies(txt):
    f=open(txt,'r')
    cookies={}
    for line in f.read().split(';'):   
        name,value=line.strip().split('=',1)  
        cookies[name]=value  
    return cookies

def get_soup_new():
    url = "https://bscscan.com/address/0x17539cca21c7933df5c980172d22659b8c345c5a"
    headers = {
        "authority": "bscscan.com",
        "method": "GET",
        "path": "/address/0x17539cca21c7933df5c980172d22659b8c345c5a",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7,zh-TW;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://bscscan.com/token/0x0a8901b0e25deb55a87524f0cc164e9644020eba?a=0x17539cca21c7933df5c980172d22659b8c345c5a",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    cookies = requests.utils.cookiejar_from_dict(get_Cookies(NFT_COOKIE_PATH), cookiejar=None, overwrite=True)
    try:
        result = requests.get(url, cookies=cookies, verify=False, timeout=10, headers=headers)
        result = result.text
        print(result)
        soup=BS4(result,'html.parser')
        return soup
    except requests.exceptions.Timeout as e:
        result = "Timeout occurred"
        print(result)
    
def get_soup():
    url = "https://bscscan.com/token/generic-tokentxns2?"
    data_ = {"contractAddress":CONTRACT_ADDRESS, \
            "sid":"daf387e3f51056ccf7a78bb0efc8e151" \
           }
    headers = {
        "authority": "bscscan.com",
        "method": "GET",
        "path": "/address/0x17539cca21c7933df5c980172d22659b8c345c5a",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7,zh-TW;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://bscscan.com/token/0x0a8901b0e25deb55a87524f0cc164e9644020eba?a=0x17539cca21c7933df5c980172d22659b8c345c5a",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    cookies = requests.utils.cookiejar_from_dict(get_Cookies('cookie_old.txt'), cookiejar=None, overwrite=True)
    
    try:
        result = requests.get(url, cookies=cookies,params=data_, verify=False, timeout=10, headers=headers)
        result = result.text
        soup=BS4(result,'html.parser')
        return soup
    except requests.exceptions.Timeout as e:
        result = "Timeout Occurred."
        print(result)


def returnAskingPrice(Txn_hash,method_type):
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))

    url = "https://bscscan.com/tx/" + Txn_hash + "#eventlog"
    headers = {
        "authority": "bscscan.com",
        "method": "GET",
        "path": "/token/generic-tokentxns2?m=normal&contractAddress=0x0a8901b0E25DEb55A87524f0cC164E9644020EBA&a=&sid=daf387e3f51056ccf7a78bb0efc8e151&p=1",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7,zh-TW;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://bscscan.com/token/0x0a8901b0E25DEb55A87524f0cC164E9644020EBA",
        "sec-fetch-dest": "iframe",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    try: 
        result = requests.get(url, verify=False, timeout=10, headers=headers)
        result = result.text
        soup=BS4(result,'html.parser')
    except requests.exceptions.Timeout as e:
        result = "Timeout Occurred."
        print(result)
    
    
    if method_type == "Modify Ask Order":
        contract_address_ = soup.find("span",{"id":"chunk_decode_0_1"}).get_text()  
        if contract_address_ != CONTRACT_ADDRESS:
            return False
        token_id = soup.find("span",{"id":"chunk_decode_0_3"}).get_text() 
        price = int(soup.find("div",{"id":"event_dec_data_1"}).find_all("span")[1].get_text())
        formatPrice = round(float(web3.fromWei(price, "ether")), 2)
    elif method_type == "Create Ask Order":
        contract_address_ = soup.find("span",{"id":"chunk_decode_0_1"}).get_text()  
        if contract_address_ != CONTRACT_ADDRESS:
            return False
        token_id = soup.find("span",{"id":"chunk_decode_2_3"}).get_text() 
        price = int(soup.find("div",{"id":"event_dec_data_3"}).find_all("span")[1].get_text())
        formatPrice = round(float(web3.fromWei(price, "ether")), 2)
    
    return [formatPrice, token_id]

def returnTxInfoNew(buffer_Txn_hash):
    res = dict()
    order = 0
    soup = get_soup_new()
    body = soup.find("tbody").find_all("tr")
    for item in body:
        method_type = item.find_all("span")[0].get_text()
        if method_type == "Modify Ask Order" or method_type == "Create Ask Order":
            Txn_hash = item.find_all("a")[1].get_text()
            
            if Txn_hash == buffer_Txn_hash:
                return res
            else:
                temp = returnAskingPrice(Txn_hash, method_type)
                if  temp != False:
                    tdict = dict()
                    price, token_id = temp[0], temp[1]
                    tdict['token_id'] = token_id
                    tdict['price'] = price
                    tdict['Txn_hash'] = Txn_hash
                    tdict['method_type'] = method_type
                    res[order] = tdict
                    order = order + 1
    return res
if __name__ == '__main__':

    res = returnTxInfoNew("0x2258588b831cb49057052fff739288cfac919bbfdf52370b3e30ff856790cdb9")
    print(res)