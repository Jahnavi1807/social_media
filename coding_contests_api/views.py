# f# views.py
# import requests
# from django.shortcuts import render

# def contests(request):
#     # Set up the Codeforces API endpoint and parameters
#     url = 'https://codeforces.com/api/contest.list'
#     params = {
#         'gym': 'false',
#         'apiKey': 'bf104ad75d6303f266f5d0a86ea7ea870226e7ec', # Replace with your Codeforces API key
#     }

#     # Make the API request and handle any errors
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()['result']
#     except requests.exceptions.RequestException as e:
#         data = []
#         error_message = str(e)

#     # Render the template with the contest data
#     context = {
#         'contests': data,
#         'error_message': error_message if 'error_message' in locals() else None,
#     }
#     return render(request, 'coding_contests/contests.html', context)


import requests
from django.shortcuts import render

def contests(request):
    # Set up the Codeforces API endpoint and parameters
    url = 'https://codeforces.com/api/contest.list'
    params = {
    'gym': 'fasle',
    'apikey': '89727854b4a8c1b4d4c2cfadfa39f88cbc85db58',}

    # Make the API request and handle any errors
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()['result']
    except requests.exceptions.RequestException as e:
        data = []
        error_message = str(e)
    
	
	


    # Render the template with the contest data
    context = {
        'contests': data,
        'error_message': error_message if 'error_message' in locals() else None,
    }
    return render(request, 'coding_contests_api/contests.html', context)
