
SMART CITY AND AI PROJECTS INFORMATION SYSTEM:-

The primary goal of this project is to develop a system that collects and displays the docu- ments related to smart city projects and AI projects in various municipal websites across Canada according to the search query. The data is obtained by the scraping the municipal websites, each scraped page is fed into the Natural Language Processing(NLP) topic modeling algorithm Latent Dirichlet allocation (LDA) to retrieve the topics from particular document. If the topics from that particular document matches any word from the set of keywords then that document is saved to the database. Later on, document similarity is used to fetch from the documents database accord- ing to the query and the results are displayed on the web page.


System Architecture:-

<img src="Whole diagram.png">


This project is a UI application of "SMART CITY AI PROJECTS INFORMATION SYSTEM" which displays the information about AI projects in municipalities of North America.

The whole project consists of three parts

1)UI application to search the query and to view the results to links to AI projects.

2)To scrape the each municipality website and store the documents related to AI projects,smart city projects. The deciding factor to store the documents is done by performing LDA over the each document. (https://github.com/manideep-d/ScrapingMunicipalities)

3)The database to store the document is MongoDB Atlas.