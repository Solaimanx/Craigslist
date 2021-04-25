import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
import re


BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render (request,'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url =  BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')


    post_listings = soup.find_all('li',{'class':'result-row'})


    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_date = post.find(class_='result-date').text
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = "NA"


        if post.find(class_='result-image').get('data-ids'):
            post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            print(post_image)
        else:
            post_src = "https://img.republicworld.com/republic-prod/stories/promolarge/xxhdpi/c20gqydyxbbt0jo0_1593062345.jpeg?tr=w-758,h-433"
        
        post_src = BASE_IMAGE_URL.format(post_image)
        final_postings.append((post_title, post_url, post_date, post_price,post_src))

    




    

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
   
    }
    return render(request,'my_app/new_search.html', stuff_for_frontend)