import requests
from bs4 import BeautifulSoup
import pandas as pd
import dateparser
from datetime import datetime
import spacy #imported all required libraries


#List of CNN article URLs
urls = [
    'https://edition.cnn.com/world/live-news/israel-lebanon-war-hezbollah-09-25-24/index.html',
    'https://edition.cnn.com/2024/09/25/politics/cnn-poll-young-voters-harris-trump/index.html',
    'https://edition.cnn.com/2024/09/25/health/global-myopia-research-scli-intl-wellness/index.html',
    'https://edition.cnn.com/2024/09/25/europe/russia-ukraine-nuclear-zelensky-un-intl/index.html'
    
]

all_articles = []

for url in urls:
    try:
       
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1').get_text() if soup.find('h1') else 'No title found'
        summary = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'No summary found'

        time_element = soup.find('p', class_='update-time')  
        relative_time = time_element.get_text() if time_element else 'Unknown time'

       
        if relative_time and 'ago' in relative_time:
            publication_date = dateparser.parse(relative_time)
        else:
            publication_date = datetime.now()

        source = 'CNN'
        article_url = url

        
        all_articles.append({
            'Title': title,
            'Summary': summary,
            'Publication Date': publication_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Source': source,
            'URL': article_url
        })

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")


df = pd.DataFrame(all_articles)

df = df[['Title', 'Summary', 'Publication Date', 'Source', 'URL']]

csv_file_name = 'cnn_articles.csv'
df.to_csv(csv_file_name, index=False)

print(f"Article details saved to {csv_file_name} in a structured table format.")

#List of Times of India article URL's
urls = [
    'https://timesofindia.indiatimes.com/world/south-asia/yunus-reveals-brains-behind-well-organised-protest-that-ousted-hasina/articleshow/113675382.cms',  # Replace with your article URLs
    'https://timesofindia.indiatimes.com/india/police-foil-kashmir-residents-plan-to-cross-into-pakistan-through-kutch-border/articleshow/113675786.cms',
    'https://timesofindia.indiatimes.com/india/tirupati-laddu-row-jagan-reddy-calls-for-atonement-rituals-in-temples-on-sep-28-for-ap-cm-naidus-sin/articleshow/113667859.cms',
    'https://timesofindia.indiatimes.com/india/heavy-rains-in-mumbai-trains-flights-disrupted-2-killed-by-lightning/articleshow/113675770.cms'
    
]

all_articles = []

for url in urls:
    try:
        
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1').get_text() if soup.find('h1') else 'No title found'
        
        summary_tag = soup.find('meta', attrs={'name': 'description'})
        summary = summary_tag['content'] if summary_tag else 'No summary found'

        time_element = soup.find('span', class_='time_c')  
        relative_time = time_element.get_text() if time_element else 'Unknown time'

        if relative_time and 'ago' in relative_time:
            publication_date = dateparser.parse(relative_time)
        else:
            publication_date = datetime.now()

        source = 'Times of India'
        article_url = url

        all_articles.append({
            'Title': title,
            'Summary': summary,
            'Publication Date': publication_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Source': source,
            'URL': article_url
        })

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")


df = pd.DataFrame(all_articles)

df = df[['Title', 'Summary', 'Publication Date', 'Source', 'URL']]

csv_file_name = 'toi_articles.csv'
df.to_csv(csv_file_name, index=False)

print(f"Article details saved to {csv_file_name} in a structured table format.")

nlp = spacy.load('en_core_web_sm')

# Categories
categories = {
    'Politics': ['politics', 'government', 'election', 'vote', 'policy', 'senate', 'congress', 'protest', 'demonstration'],
    'Technology': ['technology', 'AI', 'artificial intelligence', 'software', 'hardware', 'computer', 'internet'],
    'Sports': ['sports', 'football', 'soccer', 'basketball', 'cricket', 'game', 'tournament', 'athlete'],
    'Health': ['health', 'medicine', 'disease', 'hospital', 'vaccine', 'treatment', 'nutrition', 'research', 'study'],
    'Finance': ['finance', 'economy', 'stock', 'investment', 'market', 'money', 'bank'],
    'Entertainment': ['entertainment', 'movie', 'music', 'celebrity', 'television', 'show'],
    'Science': ['science', 'research', 'study', 'experiment', 'biology', 'chemistry', 'physics'],
    'Education': ['education', 'school', 'college', 'university', 'student', 'learning', 'teacher'],
    'International Relations': ['conflict', 'war', 'attack', 'foreign policy', 'diplomacy', 'tensions'],
    'Weather/Disaster': ['weather', 'storm', 'flood', 'rain', 'disaster', 'alert', 'evacuation'],
   
}
#Function to categorize an article based on keywords
def categorize_article(text):
    
    doc = nlp(text.lower())
    
    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category
    
    return 'Other' 
# Load CNN articles from a CSV file into a DataFrame
cnn_df = pd.read_csv('cnn_articles.csv')

toi_df = pd.read_csv('toi_articles.csv')  
#Apply the categorize_article function to the 'Summary' column of CNN articles
cnn_df['Category'] = cnn_df['Summary'].apply(categorize_article)

toi_df['Category'] = toi_df['Summary'].apply(categorize_article)

combined_df = pd.concat([cnn_df, toi_df], ignore_index=True)

updated_csv_file_name = 'news_articles_with_categories.csv'
combined_df.to_csv(updated_csv_file_name, index=False)

print(f"articles saved to {updated_csv_file_name} with a new 'Category' column.")
