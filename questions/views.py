from django_ratelimit.decorators import ratelimit
from django.shortcuts import render

import requests


# Imposing Search Limit of 5/m and 100/d
@ratelimit(key='ip', rate='5/m')
@ratelimit(key='ip', rate='100/d')
def index(request):
    return render(request, 'index.html')


def results(request, no):
    # The API endpoint
    url = "https://api.stackexchange.com/2.3/search/advanced"

    # Defining the payload
    payload = {
        "page": no,
        "pagesize": 10,
        "order": "desc",
        "sort": "activity",
        "title": request.GET['q'].strip(),
        "site": "stackoverflow"
    }
    
    # GET request to the API
    response = requests.get(url, params=payload)
    response_json = response.json()

    data = {}

    for q in response_json['items']:
        data[q['title']] = q['link']

    return render(request, 'list.html', {'data': data, 'curr': no, 'prev_pg': no - 1, 'next_pg': no + 1, 'q': payload['title']})

