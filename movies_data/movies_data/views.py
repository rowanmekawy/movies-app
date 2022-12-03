from django.shortcuts import render
import requests
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.templatetags.static import static
from django.template import loader
from .models import movies
from .serializers import moviesSerializer

    
import csv
import xlrd

def index(request):
    
    mymembers = movies.objects.all().values()
    template = loader.get_template('views.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))  

def load_movies(request):
    data=movies.objects.all().delete()
    url = "https://api.themoviedb.org/3/movie/top_rated?api_key=a3acf5c7c3141f721f08a7d4cace4ac2&language=en-US&page=1"
 
    payload = {}
    headers= {}
    
    response = requests.request("GET", url, headers=headers, data = payload)
    
    data = response.json()

    movies_list = data.get('results')
    movies_list_dic = []
    for movie in movies_list:
        rec = {
            "title" : movie.get('title'),
            "rating" : movie.get('vote_average'),
            "overview": movie.get('overview'),
            "data_sources" : 'The Movie Database: Top Rated Movies',
        }
        movies_list_dic.append(rec)
    top_250_tvs = "https://imdb-api.com/en/API/Top250TVs/k_szfihoma"
    top_250_movies = "https://imdb-api.com/en/API/Top250Movies/k_szfihoma"
    response_tvs = requests.request("GET", top_250_tvs, headers=headers, data = payload)
    response_movies = requests.request("GET", top_250_movies, headers=headers, data = payload)

    data_tvs = response_tvs.json()
    data_movies = response_movies.json()

    tv_list = data_tvs.get('items')
    for tv in tv_list:
        rec = {
            "title" : tv.get('title'),
            "rating" : tv.get('imDbRating'),
            "overview": '',
            "data_sources" : 'imDb top 250 tv',
        }
        if not list(filter(lambda movies_list_dic: movies_list_dic['title'] == rec["title"], movies_list_dic)) :

            movies_list_dic.append(rec)    
    movie_list = data_movies.get('items')  
    for movie in movie_list:

        rec = {
            "title" : movie.get('title'),
            "rating" : movie.get('imDbRating'),
            "overview": '',
            "data_sources" : 'imDb top 250 movies',
        }
        if not list(filter(lambda movies_list_dic: movies_list_dic['title'] == rec["title"], movies_list_dic)) :

            movies_list_dic.append(rec)       

    filename = open('static\datasets\movie-dataset-latest.csv', 'r', encoding='UTF-8')
    file = csv.DictReader(filename)
    for col in file:
        rec = {
            "title" : col['title'],
            "rating" : col['vote_average'],
            "overview": col['overview'],
            "data_sources" : 'movie-dataset-latest',
        }
        if not list(filter(lambda movies_list_dic: movies_list_dic['title'] == rec["title"], movies_list_dic)) :
            print("erfrrfr")
            movies_list_dic.append(rec)   

    dataframe = xlrd.open_workbook("static\datasets\\NetflixDataset.xlsx")

    sheet = dataframe.sheets()[0]
    header = sheet.row_values(0)
    ro = 1
    for r in range(ro, sheet.nrows):
        rec = {
            "title" : sheet.cell(r, header.index("title")).value,
            "rating" : sheet.cell(r, header.index("tmdb_score")).value,
            "overview": sheet.cell(r, header.index("description")).value,
            "data_sources" : 'NetflixDataset',
        }        
        if not list(filter(lambda movies_list_dic: movies_list_dic['title'] == rec["title"], movies_list_dic)) :
            movies_list_dic.append(rec)

    for movie in movies_list_dic: 
        data = movies.objects.create(title= movie['title'],overview=movie['overview'],rate=movie['rating'] ,data_sources=movie['data_sources'])
        data.save()

    return HttpResponse("""<html><script>window.location.replace('/movies');</script></html>""")

def movies_list(request):
    movies_oj =  movies.objects.all()
    serialize = moviesSerializer(movies_oj,many=True)
    return JsonResponse({"movies":serialize.data}, safe=False)