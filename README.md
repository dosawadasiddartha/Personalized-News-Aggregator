# Personalized-News-Aggregator


Overview :  This News Aggregator project is designed to collect, categorize, and serve news articles from various sources using web scraping and RESTful APIs. It delivers personalized news to users based on categories like technology, sports, business, entertainment, etc. 


Setup Instructions: 

1) First Clone the Repository 

2) Install Dependencies which was there in requirements.txt file

3) Start the FastAPI Server : open main.py file and click on terminal and enter this Run coomand: uvicorn main:app --reload

4) Go to html file and click on Run and start debugging ------> Then Web page will open in a web browser to load the frontend interface.
   It will allow you to interact with the API, search articles by keyword or category, and view detailed articles.

-----------------------------------------------------------------------------------------------------------------------------------------------------------

Usage Instructions:
---> Endpoints :  GET /articles
   
1) Retrieve all articles with optional filters: by clicking on category wise like politics, technology etc.

2) Retrieve a specific article by ID
Example request: GET http://127.0.0.1:8000/articles/1

3) Search articles by keywords in title or summary
Example request: GET http://127.0.0.1:8000/search?query=Harris

-------------------------------------------------------------------------------------------------------------------------------------------------------------

Technologies Used:
----> Backend:
FastAPI: For creating the REST API.
pandas: For data processing and manipulation.
Uvicorn: ASGI server for running FastAPI.
------> Frontend:
HTML5, CSS3, Bootstrap: For the user interface.
JavaScript: To make API requests and dynamically render articles on the page.
-------->Scraping:
requests: For sending HTTP requests.
BeautifulSoup: For scraping the web pages and extracting article data.
dateparser: For parsing date strings.
spacy: For additional text processing and NLP tasks.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

Postman Collection:  To test the API using Postman, follow these steps:

Download and install Postman.
Import the Postman collection.
You can now run the different API requests to test the endpoints.

Postman Collection Link: 
