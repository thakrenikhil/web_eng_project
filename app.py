from flask import Flask, request, render_template, redirect, url_for, session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Selenium setup for web scraping
def get_search_results(query):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless for faster execution
    service = Service('chromedriver.exe')  # Ensure correct path to ChromeDriver

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    driver.get(url)

    # Extract page content
    try:
        title = driver.find_element(By.ID, "firstHeading").text
        content = driver.find_element(By.CLASS_NAME, "mw-parser-output").text
        result = {"title": title, "content": content[:1000] + "..."}  # Limit content size
    except Exception:
        result = {"title": "No Results", "content": "No relevant information found."}

    driver.quit()
    return result

# Home route (Landing Page)
@app.route('/')
def index():
    return render_template('index.html')

# 🔹 LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # When the form is submitted
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple hardcoded credentials (Modify for database use)
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('search'))  # Redirect to search page after login
        else:
            return render_template('login.html', error="Invalid credentials. Try again!")

    return render_template('login.html')  # Display login page for GET requests

# 🔹 SEARCH PAGE (After Login)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'logged_in' in session:  # Check if user is logged in
        if request.method == 'POST':  # If user submits a search query
            query = request.form.get('query')
            if query:
                result = get_search_results(query)
                return render_template('results.html', result=result, query=query)
            return render_template('search.html', error="Please enter a valid query.")

        return render_template('search.html')  # Show search page for GET requests

    return redirect(url_for('index'))  # Redirect to home if not logged in

# 🔹 SKIP LOGIN ROUTE
@app.route('/skip')
def skip():
    return render_template('skip.html')  # Show the introductory page

# 🔹 LOGOUT ROUTE
@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove session
    return redirect(url_for('index'))

@app.route('/yoga', methods=['GET', 'POST'])
def yoga():
    search_query = ""
    if request.method == 'POST':
        search_query = request.form.get('search')

    # Sample Data (Replace with DB/Selenium/YouTube API)
    videos = [
        {"title": "Sun Salutation", "url": "https://www.youtube.com/embed/VaoV1PrYft4"},
        {"title": "Tree Pose", "url": "https://www.youtube.com/embed/VaoV1PrYft4"},
        {"title": "Tree Pose", "url": "https://www.youtube.com/embed/VaoV1PrYft4"},
        {"title": "Tree Pose", "url": "https://www.youtube.com/embed/VaoV1PrYft4"},
    ]
    asanas = ["Tadasana", "Vrikshasana", "Trikonasana", "Bhujangasana", "Padmasana", "Dhanurasana", "Naukasana", "Shavasana", "Surya Namaskar"]
    trainers = [
        {"name": "Ravi Yoga", "price": "$10/month"},
        {"name": "Anjali Wellness", "price": "$15/month"},
        {"name": "Yogify Studio", "price": "$20/month"}
    ]

    return render_template('yoga.html', query=search_query, videos=videos, asanas=asanas, trainers=trainers)

if __name__ == '__main__':
    app.run(debug=True)
