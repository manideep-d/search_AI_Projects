from pymongo import MongoClient

import pandas as pd
from tqdm import tqdm
tqdm.pandas(desc="progress-bar")

import nltk
nltk.data.path.append('viewprojects/nltk_data')
nltk.download('omw-1.4')

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from itertools import chain
from nltk.tag import pos_tag

import os

import gensim

HOST_NAME = os.environ['HOST_NAME']
PORT = os.environ['PORT']
DATABASE_NAME = os.environ['DATABASE_NAME']
COLLECTION_NAME = os.environ['COLLECTION_NAME']

#https://www.analyticsvidhya.com/blog/2021/06/how-to-connect-mongodb-database-with-django/
def get_db_handle(host, port,db_name,collection_name):
    """To use Mongodb client """
    try:

        client = MongoClient(host,port=int(port))
        db_handle = client[db_name]
        collection_handle = db_handle[collection_name]
    
    except Exception as e:
        raise ("Not able to retrive the database properties.",e)
    
    return collection_handle


def filteringTheProjects(query,municipality_name):
    """ Filters the projects from database according to the muncipality name and accordint to search query """
    
    collection_handle = get_db_handle(HOST_NAME, PORT,DATABASE_NAME,COLLECTION_NAME)

    if(municipality_name == 'allmunicipalities'):
        all_projects = list(collection_handle.find())
        docs,filteredProjects = appending_docs(all_projects)

    elif(municipality_name == 'richmondhill'):
        projects = list(collection_handle.find({ "municipality_name": "richmondhill"}))
        docs,filteredProjects = appending_docs(projects)

    elif(municipality_name == 'missisuaga'):
        projects = list(collection_handle.find({ "municipality_name": "missisuaga"}))
        docs,filteredProjects = appending_docs(projects)

    elif(municipality_name == 'winnipeg'):
        projects = list(collection_handle.find({ "municipality_name": "winnipeg"}))
        docs,filteredProjects = appending_docs(projects)

    else: #niagarafalls
        projects = list(collection_handle.find({ "municipality_name": "niagarafalls"}))
        docs,filteredProjects = appending_docs(projects)

    if(len(docs)>0):
        sim_array = findingtfid(docs,query)
        new_projects = findingSimilarProjects(sim_array,filteredProjects)

    else:
        new_projects=[]

    return new_projects

def appending_docs(projects):
    """appending text,matched words and topics  """
    docs = []
    filteredProjects = []

    for project in projects:
                doc = project['topics'] + project['matched_words'] + project['topics'] + project['text']
                docs.append(doc)
                filteredProjects.append(project)
    
    return docs,filteredProjects

    
def findingtfid(docs,query):
    """ Returns the tfid matrix with query and documents returned from the database. This does the preprocessing of query and documents"""
    #https://github.com/thepylot/Resemblance/blob/master/sim/views.py

    data = pd.DataFrame(list(docs),columns =[ 'texts'])
    lemmatizer = WordNetLemmatizer()

    data['sentences'] = data['texts'].progress_map(sent_tokenize)

    data['tokens_sentences'] = data['sentences'].progress_map(lambda sentences: [word_tokenize(sentence) for sentence in sentences])

    data['tokens_sentences_lemmatized'] = data['tokens_sentences'].progress_map(
        lambda list_tokens_POS: [
            [
                lemmatizer.lemmatize(tokens) for tokens in tokens_POS
            ] 
            for tokens_POS in list_tokens_POS
        ]
    )

    my_stopwords = stopwords.words('english') 

    data['tokens'] = data['tokens_sentences_lemmatized'].map(lambda sentences: list(chain.from_iterable(sentences)))

    data['tokens'] = data['tokens_sentences_lemmatized'].map(lambda tokens_lits: [token.lower() for tokens in tokens_lits for token in tokens if token.isalpha() 
                                                        and token.lower() not in my_stopwords and len(token)>1])

    tokens = data['tokens'].tolist()

    dictionary = gensim.corpora.Dictionary(tokens)

    corpus = [dictionary.doc2bow(token) for token in tokens]
    tf_idf = gensim.models.TfidfModel(corpus)
    
    root_dir = os.path.abspath(os.path.dirname(__name__))
    working_dir = os.path.join(root_dir, 'workdir/')
    sims = gensim.similarities.Similarity(working_dir,tf_idf[corpus],num_features=len(dictionary))


    query_doc = [w.lower() for w in word_tokenize(query)]
    query_doc = [ word for word  in query_doc if word not in my_stopwords]
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]

    return sims[query_doc_tf_idf]

def findingSimilarProjects(sim_array,docs):
    """ Returning the projects which are having tfid greater than 0 """

    sim_projects = []
    for index,sim_score in enumerate(sim_array):
        if sim_score > 0:
            sim_projects.append(docs[index])
    
    return sim_projects
