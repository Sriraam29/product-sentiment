Product Sentiment Analyzer
Overview
This project, product_sentiment.py, is a Streamlit web application that scrapes product reviews from Amazon, analyzes their sentiment using NLTK's VADER sentiment analyzer, and presents the results in a user-friendly interface. The application allows users to input an Amazon product URL, fetches the reviews, determines the sentiment (positive, negative, or neutral) for each review, and calculates an overall sentiment for the product.
Features

Web Scraping: Extracts reviews from Amazon product pages using requests and BeautifulSoup.
Sentiment Analysis: Uses NLTK's VADER (SentimentIntensityAnalyzer) to classify sentiments.
Streamlit Interface: Provides an interactive UI to input URLs and view sentiment analysis results.
Visual Feedback: Displays individual review sentiments with color-coded labels (green for positive, red for negative, gray for neutral) and an overall sentiment summary.

Project Structure

product_sentiment.py: The main Python script containing the Flask application, web scraping logic, sentiment analysis, and Streamlit UI setup.

Prerequisites
To run this project, you'll need the following installed on your system:

Python 3.8+
pip (Python package manager)
A web browser (to interact with the Streamlit app)

Required Python Libraries

requests (for making HTTP requests to scrape reviews)
beautifulsoup4 (for parsing HTML content)
nltk (for sentiment analysis using VADER)
streamlit (for the web interface)

Setup Instructions
1. Clone or Download the Project
Download the project file (product_sentiment.py) to your local machine.
2. Set Up a Python Environment
It’s recommended to use a virtual environment to manage dependencies:
# Create a virtual environment
python -m venv sentiment_env

# Activate the virtual environment
# On Windows
sentiment_env\Scripts\activate
# On macOS/Linux
source sentiment_env/bin/activate

3. Install Dependencies
Install the required Python libraries:
pip install requests beautifulsoup4 nltk streamlit

4. Download NLTK Data
The script uses NLTK's VADER lexicon for sentiment analysis. The script automatically downloads it with:
nltk.download('vader_lexicon', quiet=True)

Ensure you have an internet connection when running the script for the first time, as this download is required.
5. Run the Streamlit Application
Execute the product_sentiment.py script to start the Streamlit server:
streamlit run product_sentiment.py


Streamlit will start a local server and open the app in your default web browser (typically at http://localhost:8501).

Usage
Analyzing Product Reviews

Access the Interface: After running the script, your browser will open to http://localhost:8501. If it doesn’t, navigate to that URL manually.
Input the Product URL:
Enter an Amazon product URL in the text input field (e.g., https://www.amazon.com/dp/B08N5WRWNW).
Ensure the URL points to a product page with reviews.


Analyze Reviews:
Click the "Analyze" button to start the scraping and analysis process.
The app will display a spinner while it fetches and analyzes the reviews.


View Results:
If successful, the app will show the number of reviews found, the overall sentiment (Positive, Negative, or Neutral) with an average compound score, and individual review details.
Each review includes a snippet of the text, its sentiment (color-coded), and the compound score.
If there’s an error (e.g., no reviews found, CAPTCHA blocking, or network issues), an error message will be displayed.



Technical Details
Web Scraping

Target: The script scrapes Amazon reviews by targeting <span> elements with the attribute data-hook="review-body".
Fallback: If no reviews are found on the main product page, it attempts to scrape from the /product-reviews/ subpage.
Error Handling: Detects CAPTCHA blocks and network errors, providing appropriate error messages.

Sentiment Analysis

Tool: Uses NLTK's VADER SentimentIntensityAnalyzer to compute sentiment scores.
Scoring: Each review receives a compound score:
≥ 0.05: Positive
≤ -0.05: Negative
Otherwise: Neutral


Overall Sentiment: Calculated as the average compound score across all reviews, with the same threshold for classification.

Streamlit Interface

Layout: Uses Streamlit's wide layout with custom CSS for styling (e.g., background colors, button styles, text formatting).
Features:
A text input for the URL.
An "Analyze" button to trigger the scraping and analysis.
Dynamic display of results with color-coded sentiment labels.
A footer crediting xAI.



Current Limitations

Amazon Blocking: Amazon may block requests if it detects scraping activity (e.g., via CAPTCHA challenges). The script attempts to mitigate this with a user-agent header but may still fail under heavy restrictions.
Review Length: Long reviews are truncated to 200 characters in the UI for readability.
Static Source: Only Amazon product pages are supported due to the specific HTML parsing logic.
No Persistence: Results are not saved; you must re-run the analysis to view results again.

Future Improvements

Proxy Support: Add support for proxies to bypass Amazon’s scraping restrictions.
Customizable Sources: Extend the scraper to support reviews from other e-commerce platforms (e.g., eBay, Walmart).
Review Filtering: Allow users to filter reviews by sentiment or keyword.
Export Functionality: Add an option to export the sentiment analysis results as a CSV file.
Advanced Sentiment Models: Integrate more sophisticated models (e.g., BERT-based sentiment analysis) for better accuracy.

Troubleshooting

Streamlit Not Starting: Ensure all dependencies are installed (streamlit, requests, beautifulsoup4, nltk). Check for errors in the terminal when running the script.
No Reviews Found: Verify the Amazon URL is correct and contains reviews. If Amazon blocks the request, consider using a VPN or proxy.
NLTK Download Fails: Ensure you have an internet connection for the initial nltk.download('vader_lexicon').

License
This project is open-source and available under the MIT License. Feel free to use, modify, and distribute it as needed.
Contact
For questions or contributions, please reach out via email at sriraamhari04@gmail.com  or open an issue on the project repository (if hosted on GitHub).
