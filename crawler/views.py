import json
import time
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from fake_useragent import UserAgent
from linkedin_scraper import actions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from .models import Profile

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


def get_individual_result_from_linkedin(url, driver):
    individual_user_data = {}
    individual_user_data[url] = {}
    companies = []
    certifications = []

    driver.get(url)
    # Depends on how fast your server loads javascript and htmls
    # This code is to load entire html code, not only source code
    time.sleep(5)
    body = driver.find_element_by_tag_name("body")
    last_height = driver.execute_script(
        "return document.body.scrollHeight")
    while True:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(5)
        new_height = driver.execute_script(
            "return document.body.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height

    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')

    # Find all profile sections, It will find all headings like Experiences, Companies, Licenses etc
    all_divs = soup.findAll(class_="pv-profile-section-pager")

    for div in all_divs:
        headers = div.findAll('h2')
        for h in headers:
            if h.has_attr('class') and h['class'][0] == 'pv-profile-section__card-heading':
                # print(h.get_text().strip())
                extractedText = h.get_text().strip()
                if (extractedText == 'Experience'):
                    insideDivs = div.findAll('div')
                    for d in insideDivs:
                        # pv-entity_summary-info pv-entity_summary-info--background-section
                        if d.has_attr('class') and d['class'][0] == 'pv-entity__summary-info' and d['class'][
                            1] == 'pv-entity__summary-info--background-section':
                            pAll = d.findAll('p')

                            for p in pAll:
                                if p.get_text().strip() != 'Company Name':
                                    companies.append(p.get_text().strip())

                if (extractedText == 'Licenses & Certifications'):
                    # <h3 class="t-16 t-bold">Epic Beaker Anatomic Pathology</h3>
                    insideHeaders = div.findAll('h3')
                    for h3 in insideHeaders:
                        if h3.has_attr('class') and h3['class'][0] == 't-16' and h3['class'][1] == 't-bold':
                            # print(h3.get_text())
                            certifications.append(h3.get_text().strip())

    try:

        individual_user_data[url]['current_employer'] = companies[0]

    except:
        individual_user_data[url]['current_employer'] = 'None'

    individual_user_data[url]['companies'] = companies
    individual_user_data[url]['certifications'] = certifications
    # find name, current position,
    return individual_user_data


@csrf_exempt
def crawler(request, query):
    print("*************************************************************************************************************************************************************")
    print(query)
    email = "g.rajukoushik@gmail.com"
    password = "rituraja"
    actions.login(driver, email, password)

    name_list = []

    print(request.GET)

    # proxy_list = get_proxies()

    # print(proxy_list)

    # making a request to a google custom search engine
    custom_search_engine_url = "https://www.googleapis.com/customsearch/v1"

    linkedin_url_list = set()

    for i in range(0, 1):
        print(str(i) + "loop info")
        PARAMS = {'key': 'AIzaSyByUxDR0YO701YOETlSJZn6bfFNWIjtQBM', 'cx': '009462381166450434430:ecyvn9zudgu',
                  'q': query, 'start': i * 10}

        # sending get request and saving the response as response object
        r = requests.get(url=custom_search_engine_url, params=PARAMS)

        # extracting data in json format
        custom_search_engine_data = r.json()

        for j in range(len(custom_search_engine_data['items'])):
            linkedin_url_list.add(custom_search_engine_data['items'][j]['link'])

            # linkedin_url_data = custom_search_engine_data['items']
            #
            # print(custom_search_engine_data['items'][0]['link'])

    print(linkedin_url_list)

    dicty = {}

    for linkedin in linkedin_url_list:
        temp = get_individual_result_from_linkedin(linkedin, driver)
        dicty[linkedin] = get_individual_result_from_linkedin(linkedin, driver)
        print(temp)

        profile_model = Profile()

        URL = list(temp.keys())[0]
        profile_model.name = URL.split("/")[-1]
        profile_model.linkedin_url = URL
        profile_model.companies = json.dumps(temp[URL]['companies'])
        profile_model.current_job = temp[URL]['current_employer']
        profile_model.certifications = json.dumps(temp[URL]['certifications'])
        profile_model.is_updated = False
        profile_model.save()
    p = Profile()
    profile_all = p.objects.all()

    return 1

    # return HttpResponse(
    #     json.dumps(
    #         {
    #             'linkedin_url-list': str(linkedin_url_list),
    #             'post_name': str(name_list),
    #             'post_content': 1,
    #             'dict': dicty
    O

    #
    #         }
    #     )
    # )


def home(request):
    template_name = 'home.html'
    return render(request, template_name)


def result(request, query):
    template_name = 'index.html'
    query_set = Profile.objects.all()
    key = query
    if key:
        query_set =query_set.filter(certifications__icontains=key)

    return render(request, template_name, {'profiles': query_set, 'key': query})
