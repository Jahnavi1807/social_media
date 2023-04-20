from django.shortcuts import render
import requests
API_KEY = 'ab547a533c5c41659e5e03d2132abdc3'
# Create your views here.

def news(request):
	url = f'https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey={API_KEY}'
	response = requests.get(url)
	data = response.json()
	articles = data['articles']

	context = {
	'articles' : articles }

	return render(request,'news_api/news_home.html',context)


