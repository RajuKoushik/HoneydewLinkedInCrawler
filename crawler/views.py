import json

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = response.text
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


@csrf_exempt
def crawler(request):
    print(request.GET)

    # making a request to a google custom search engine
    custom_search_engine_url = "https://www.googleapis.com/customsearch/v1"

    linkedin_url_list = []

    for i in range(0, 6):
        print(str(i) + "loop info")
        PARAMS = {'key': 'AIzaSyByUxDR0YO701YOETlSJZn6bfFNWIjtQBM', 'cx': '009462381166450434430:ecyvn9zudgu',
                  'q': request.GET['query'], 'start': i * 10}

        # sending get request and saving the response as response object
        r = requests.get(url=custom_search_engine_url, params=PARAMS)

        # extracting data in json format
        custom_search_engine_data = r.json()

        for j in range(len(custom_search_engine_data['items'])):
            linkedin_url_list.append(custom_search_engine_data['items'][j]['link'])

            # linkedin_url_data = custom_search_engine_data['items']
            #
            # print(custom_search_engine_data['items'][0]['link'])

    return HttpResponse(
        json.dumps(
            {
                'linkedin_url-list': linkedin_url_list,
                'post_name': 1,
                'post_content': 1,

            }
        )
    )
