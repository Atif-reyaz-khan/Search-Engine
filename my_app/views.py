from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
from .import models 
# Create your views here.
BASE_CRAIGSLIST_URL="https://lucknow.craigslist.org/d/services/search/bbb?query={}"
BASE_IMAGE_URL="https://images.craigslist.org/{}_300x300.jpg"
def home(request):
    return render(request,'base.html')
def new_search(request):
    search=request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url=BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # print(quote_plus(search))
    # print(final_url)
    response=requests.get(final_url)
    data=response.text
    soup=BeautifulSoup(data,features='html.parser')
    final_postings=[]
    post_listing=soup.find_all('li',{'class':'result-row'})
    for post in post_listing:
        if(post.find(class_='result-title')):
            post_title=post.find(class_='result-title').text
        else:
            post_title='N/A'
        
        post_url=post.find('a').get('href')
        if(post.find(class_='result-image').get('data-ids')):
            post_image_id=post.find(class_="result-image").get('data-ids').split(',')[0].split(':')[1]
            
            post_image_url=BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.7k6XrvCq3pF-bH1nKh2LYQHaHa%26pid%3DApi&f=1"
        if(post.find(class_='result-price')):
            post_price=post.find(class_='result-price').text
        else:
            post_price='N/A' 
        final_postings.append((post_title,post_url,post_price,post_image_url))
        


    # print(post_price)



    
    # print(data)
    stuff_for_frontend={
        'final_postings':final_postings,
        'search':search,
    }
    return render(request,'my_app/new_search.html',stuff_for_frontend)