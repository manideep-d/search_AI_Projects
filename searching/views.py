from django.shortcuts import render

from utils import get_db_handle, get_collection_handle, filteringTheProjects

import re
import os


HOST_NAME = os.environ['HOST_NAME']
PORT = os.environ['PORT']
DATABASE_NAME = os.environ['DATABASE_NAME']
COLLECTION_NAME = os.environ['COLLECTION_NAME']

try:
    db_handle, mongo_client = get_db_handle(DATABASE_NAME,HOST_NAME,PORT)
    collection_handle = get_collection_handle(db_handle,COLLECTION_NAME)
except Exception as e:
    raise ("Not able to retrive the database properties.",e)


def home(request):
        """ This is home view where it returns html code of search box """

        municipalities = ['Richmond hill','Missisuaga','Winnipeg','Niagara falls','Vaughan','All Municipalities']
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

    municipality_name = municipality_name.replace(" ", "")

    all_projects = list(collection_handle.find())

    projects = filteringTheProjects(query,municipality_name.lower(),all_projects)
    context ={
                'projects':projects,
                'query':query,
                'municipality_name' : municipality_name
                } 

    if (len(projects) == 0):
        return render(request,'searching/noresults.html')
    else:
        return render(request,'searching/searchResults.html',context)