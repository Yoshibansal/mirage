import requests, json
from bs4 import BeautifulSoup
import time

def scrap(url):
    headers = {
        'authority': 'hub.sovy.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'cache-control': 'max-age=0',
        'referer': 'https://www.sovy.com/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    params = (
        ('domain', url),
        ('utm_source', 'gdprreadinessscan'),
        ('utm_medium', 'sovy.com'),
        ('utm_campaign', 'sovy.com'),
    )

    session = requests.Session()
    response = session.get('https://hub.sovy.com/gdpr-scan/', headers=headers, params=params)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        script = soup.find('script', attrs={'id': 'pricetable-script-js-extra'})
        json_encry_uid = script.text.strip().split('=')[1].rstrip(';')
        
        encry_uid = json.loads(json_encry_uid)['encry_uid']
        
        print(encry_uid)
        
        print(response.status_code)
        
        headers = {
            'authority': 'hub.sovy.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://hub.sovy.com',
            'referer': 'https://hub.sovy.com/gdpr-scan/?domain=https://www.facebook.com&utm_source=gdprreadinessscan&utm_medium=sovy.com&utm_campaign=sovy.com',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
        'action': 'checklink_t2',
        'path': url,
        'encry_uid': encry_uid
        }

        
        for retry in range(2):
            response = session.post('https://hub.sovy.com/wp-admin/admin-ajax.php', headers=headers, data=data)
            if retry == 1:
                if response.status_code == 200:
                    main_url = json.loads(response.content)

    print(main_url['scan_url'])

    url = main_url['scan_url']
    headers = {
    'authority': 'hub.sovy.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63',
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        time.sleep(60)
        soup = BeautifulSoup(response.content, 'lxml')
        whatyouneed = []
        #section 1
        div = soup.find('div', attrs={'class': 'whatyouneed'})
        
        if div:
            headings = div.findAll('h4')
            descriptions = div.findAll('h5')
            
            for heading, description in zip(headings, descriptions):
                inner = {
                    'head': heading.text.strip(),
                    'description': description.text.strip()
                }
                
                whatyouneed.append(inner)
                        
        divs = soup.findAll('div', attrs={'class': 'mod_desc'})
        
        missing = {}
        whatyouhave = {}

        for i in range(len(divs)):
            divs2 = divs[i].findAll('div')
            if divs2 and len(divs2):
                for div2 in divs2:
                    headings = div2.findAll('h4')
                    for heading in headings:
                        heads = div2.findAll('h5')
                        descriptions = div2.findAll('h6')
                        
                        lists = []
                        
                        for head, description in zip(heads, descriptions):
                            inner = {
                                'head': head.text.strip(),
                                'description': description.text.strip()
                            }
                            
                            lists.append(inner)
                        
                        if i == 0:
                            missing[heading.text.strip()] = lists
                        else:
                            whatyouhave[heading.text.strip()] = lists

        data = {
            'whatyouneed': whatyouneed,
            'missing': missing,
            'whatyouhave': whatyouhave
        }
        
        return data