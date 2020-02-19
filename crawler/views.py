import json

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


@csrf_exempt
def crawler(request):
    print(request.GET)

    # making a request to a google custom search engine
    custom_search_engine_url = "https://www.googleapis.com/customsearch/v1"

    PARAMS = {'key': 'AIzaSyByUxDR0YO701YOETlSJZn6bfFNWIjtQBM', 'cx': '009462381166450434430:ecyvn9zudgu',
              'q': request.GET['query']}

    # sending get request and saving the response as response object
    r = requests.get(url=custom_search_engine_url, params=PARAMS)

    # extracting data in json format
    custom_search_engine_data = r.json()

    print(custom_search_engine_data)

    return HttpResponse(
        json.dumps(
            {
                'current_user': 1,
                'post_name': 1,
                'post_content': 1,

            }
        )
    )
