import json
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from fake_useragent import UserAgent
from linkedin_scraper import Person, actions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

ua = UserAgent()  # From here we generate a random user agent
proxies = []


def get_proxies():
    proxy = []
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        a = row.find_all('td')[0].string + row.find_all('td')[1].string

        proxy.append({'https': a})

        proxies.append({
            'ip': row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    return proxies


@csrf_exempt
def crawler(request):
    email = "g.rajukoushik@gmail.com"
    password = "rituraja"
    actions.login(driver, email, password)

    name_list = []

    print(request.GET)

    proxy_list = get_proxies()

    print(proxy_list)

    # making a request to a google custom search engine
    custom_search_engine_url = "https://www.googleapis.com/customsearch/v1"

    linkedin_url_list = set()

    for i in range(0, 6):
        print(str(i) + "loop info")
        PARAMS = {'key': 'AIzaSyByUxDR0YO701YOETlSJZn6bfFNWIjtQBM', 'cx': '009462381166450434430:ecyvn9zudgu',
                  'q': request.GET['query'], 'start': i * 10}

        # sending get request and saving the response as response object
        r = requests.get(url=custom_search_engine_url, params=PARAMS)

        # extracting data in json format
        custom_search_engine_data = r.json()

        for j in range(len(custom_search_engine_data['items'])):
            linkedin_url_list.add(custom_search_engine_data['items'][j]['link'])

            # linkedin_url_data = custom_search_engine_data['items']
            #
            # print(custom_search_engine_data['items'][0]['link'])

    for i in linkedin_url_list:

        try:
            # if email and password isnt given, it'll prompt in terminal
            person = Person(i, driver=driver)
            name_list.append(person)
        except:
            pass

    print(name_list)

    return HttpResponse(
        json.dumps(
            {
                'linkedin_url-list': str(linkedin_url_list),
                'post_name': 1,
                'post_content': 1,

            }
        )
    )
