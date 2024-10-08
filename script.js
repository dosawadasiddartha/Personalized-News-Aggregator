const articlesContainer = document.getElementById('articles');
const searchInput = document.getElementById('search');
const categorySelect = document.getElementById('category');
const searchButton = document.getElementById('search-button');

// Function to fetch articles
async function fetchArticles() {
    const category = categorySelect.value;
    const searchQuery = searchInput.value;

    let url;

// If there's a search query, use the `/search` endpoint
    if (searchQuery) {
        url = `http://127.0.0.1:8000/search?query=${encodeURIComponent(searchQuery)}`;
    } else {
        
        url = 'http://127.0.0.1:8000/articles';
        if (category) {
            url += `?category=${category}`;
        }
    }

    console.log(`Fetching URL: ${url}`);

    const response = await fetch(url);
    if (!response.ok) {
        console.error(`HTTP error! status: ${response.status}`);
        return;
    }
    const articles = await response.json();
    displayArticles(articles);
}

// Function to display articles and make them clickable
function displayArticles(articles) {
    articlesContainer.innerHTML = '';
    if (articles.length === 0) {
        articlesContainer.innerHTML = '<div class="list-group-item">No articles found.</div>';
        return;
    }
    articles.forEach(article => {
        const articleItem = document.createElement('a');
        articleItem.className = 'list-group-item list-group-item-action';
        articleItem.href = article.url; 
        articleItem.target = "_blank"; 
        articleItem.innerHTML = `<h5>${article.title}</h5><p>${article.summary}</p><small>${article.publication_date} | ${article.source}</small>`;
        articlesContainer.appendChild(articleItem);
    });
}

// Event listener for search button click
searchButton.addEventListener('click', fetchArticles);

// Event listeners for filtering
searchInput.addEventListener('input', fetchArticles);
categorySelect.addEventListener('change', fetchArticles);

fetchArticles();
