import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import streamlit as st
import time


nltk.download('vader_lexicon', quiet=True)
sid = SentimentIntensityAnalyzer()


def scrape_reviews(url):
  
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.216 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

       
        review_elements = soup.find_all('span', {'data-hook': 'review-body'})
        reviews = [review.get_text(strip=True) for review in review_elements if review.get_text(strip=True)]

        
        if not reviews:
            reviews_url = url + "/product-reviews/"
            response = requests.get(reviews_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            review_elements = soup.find_all('span', {'data-hook': 'review-body'})
            reviews = [review.get_text(strip=True) for review in review_elements if review.get_text(strip=True)]

        if not reviews:
            # Check for potential CAPTCHA or blocked access
            if "captcha" in response.text.lower() or "robot" in response.text.lower():
                return ["Amazon has blocked this request. Try again later or use a different IP."]
            return ["No reviews found on this page."]
        return reviews
    except requests.RequestException as e:
        return [f"Error fetching URL: {e}"]
    except Exception as e:
        return [f"Unexpected error: {e}"]

def analyze_sentiment(reviews):
    sentiments = []
    for review in reviews:
        scores = sid.polarity_scores(review)
        if scores['compound'] >= 0.05:
            sentiment = "Positive"
        elif scores['compound'] <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        sentiments.append({"review": review, "sentiment": sentiment, "compound": scores['compound']})
    return sentiments


def calculate_overall_sentiment(sentiment_results):
    if not sentiment_results:
        return "No data", 0.0
    avg_compound = sum(result['compound'] for result in sentiment_results) / len(sentiment_results)
    if avg_compound >= 0.05:
        overall_sentiment = "Positive"
    elif avg_compound <= -0.05:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    return overall_sentiment, avg_compound


def main():
   
    st.set_page_config(page_title="Product Sentiment Analyzer", layout="wide")

   
    st.markdown("""
        <style>
        .main {background-color: #f0f0f0;}
        .stButton>button {background-color: #4CAF50; color: white; font-weight: bold; border: none; padding: 10px 20px;}
        .stButton>button:hover {background-color: #45a049;}
        .title {color: #333333; font-size: 28px; font-weight: bold; text-align: center;}
        .footer {color: #666666; font-size: 12px; text-align: center; margin-top: 20px;}
        .overall {color: #333333; font-size: 18px; font-weight: bold; text-align: center; padding: 10px; background-color: #e0e0e0; border-radius: 5px;}
        </style>
    """, unsafe_allow_html=True)

    
    st.markdown('<div class="title">Product Review Sentiment Analyzer</div>', unsafe_allow_html=True)

   
    url = st.text_input("Enter Product URL (e.g., Amazon link)", "")

   
    if st.button("Analyze"):
        if not url:
            st.error("Please enter a valid URL.")
        else:
            with st.spinner("Scraping and analyzing reviews..."):
                st.write(f"Scraping reviews from: {url}")
                reviews = scrape_reviews(url)

                if reviews and not any(review.startswith("Error") or review.startswith("No") or review.startswith("Amazon") for review in reviews):
                    st.success(f"Found {len(reviews)} reviews!")
                    sentiment_results = analyze_sentiment(reviews)

                    
                    overall_sentiment, avg_compound = calculate_overall_sentiment(sentiment_results)
                    overall_sentiment_color = "green" if overall_sentiment == "Positive" else "red" if overall_sentiment == "Negative" else "gray"
                    st.markdown(f'<div class="overall">Overall Sentiment: <span style="color:{overall_sentiment_color}">{overall_sentiment}</span> (Average Score: {avg_compound:.2f})</div>', unsafe_allow_html=True)

                   
                    for idx, result in enumerate(sentiment_results, 1):
                        st.subheader(f"Review {idx}")
                        st.write(f"**Text:** {result['review'][:200]}..." if len(result['review']) > 200 else result['review'])
                        sentiment_color = "green" if result['sentiment'] == "Positive" else "red" if result['sentiment'] == "Negative" else "gray"
                        st.markdown(f"**Sentiment:** <span style='color:{sentiment_color}'>{result['sentiment']}</span> (Score: {result['compound']:.2f})", unsafe_allow_html=True)
                        st.write("---")
                else:
                    error_message = reviews[0] if reviews else "No reviews found or an error occurred."
                    st.error(error_message)

    
    st.markdown('<div class="footer">Powered by xAI</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()