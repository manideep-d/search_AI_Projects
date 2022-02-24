from django.shortcuts import render

from utils import filteringTheProjects

import re


def home(request):
        """ This is home view where it returns html code of search box """

        municipalities = ['Richmond Hill','Missisuaga','Winnipeg','Niagara Falls','All Municipalities']
                                                                    
        return render(request,'searching/home.html',{'municipalities':municipalities})

def about(request):
     """ Returns html code about page """

     return render(request,'searching/about.html')


def searchResults(request):
    """ This method is returning the search results according to the search query """
    try:
        query = request.POST['query']
        municipality_name = request.POST['municipality_name']
    except Exception as e:
        raise ("Error recieving in query or municipality name from post.",e)

    municipality_name = municipality_name.replace(" ", "").lower()

    projects = filteringTheProjects(query,municipality_name)
    context ={
                'projects':projects,
                'query':query,
                'municipality_name' : municipality_name
                } 

    if (len(projects) == 0):
        return render(request,'searching/noresults.html')
    else:
        return render(request,'searching/searchResults.html',context)