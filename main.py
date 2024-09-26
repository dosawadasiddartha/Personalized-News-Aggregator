from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from typing import List, Optional

#Load articles data from CSV
def load_articles():
    try:
        return pd.read_csv('news_articles_with_categories.csv')
    except FileNotFoundError:
        raise Exception("CSV file not found. Ensure the file path is correct.")

#Load the articles into a DataFrame
articles_df = load_articles()
app = FastAPI() #Initialize the FastAPI application


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class Article(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: str
    source: str
    url: str
    category: str

#Function to convert the DataFrame to a list of Article objects
def get_articles() -> List[Article]:
    return [
        Article(
            id=index,
            title=row['Title'],
            summary=row['Summary'],
            publication_date=row['Publication Date'],
            source=row['Source'],
            url=row['URL'],
            category=row['Category']
        )
        for index, row in articles_df.iterrows()
    ]

#Test endpoint to verify articles are loaded correctly
@app.get("/test-articles", response_model=List[Article])
def test_articles():
    articles = get_articles()
    return articles  

@app.get("/articles", response_model=List[Article])
def read_articles(category: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
    articles = get_articles()

    
    print("Initial articles count:", len(articles))
#Filter by category if provided
    if category:
        print(f"Filtering by category: {category}")
        articles = [article for article in articles if article.category.lower() == category.lower()]
        print("Articles count after category filter:", len(articles))  

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            articles = [
                article for article in articles 
                if start_date <= datetime.strptime(article.publication_date, "%Y-%m-%d %H:%M:%S") <= end_date
            ]
            print("Articles count after date filter:", len(articles)) 
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    return articles

#Retrieve a specific article by its ID.
@app.get("/articles/{id}", response_model=Article)
def read_article(id: int):
    articles = get_articles()
    for article in articles:
        if article.id == id:
            return article
    raise HTTPException(status_code=404, detail="Article not found")

@app.get("/search", response_model=List[Article])

#Search for articles by a keyword in the title or summary.
def search_articles(query: str):
    articles = get_articles()
    filtered_articles = [
        article for article in articles 
        if query.lower() in article.title.lower() or query.lower() in article.summary.lower()
    ]
    if not filtered_articles:
        raise HTTPException(status_code=404, detail="No articles found matching the query.")
    return filtered_articles

