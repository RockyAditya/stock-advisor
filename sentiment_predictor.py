from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(message):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(message)

    sentiment = "Neutral"
    if score['compound'] >= 0.05:
        sentiment = "Positive"
    elif score['compound'] <= -0.05:
        sentiment = "Negative"

    return sentiment, score['compound']  # Only two values

