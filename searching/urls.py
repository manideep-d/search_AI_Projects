from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name ='search_projects' ),
    path('searchresults',views.searchResults,name ='search_results' ),
    path('about',views.about,name ='about' ),
]
