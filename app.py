from flask import Flask, render_template, request
from sentiment_predictor import analyze_sentiment
from stock_predictor import get_stock_trend

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form["ticker"].upper()
        message = request.form["message"]

        # Analyze sentiment of the message
        sentiment, score = analyze_sentiment(message)

        # Get stock trend, avg_return, and graph
        avg_return, trend, _, graph_path = get_stock_trend(ticker)

        if avg_return is None:
            error = "Invalid Ticker or Data Not Available."
            return render_template("index.html", error=error)

        # Determine final suggestion based on both sentiment and trend
        suggestion = "HOLD"  # default

        if trend == "Upward":
            if score > 0.1:
                suggestion = "SELL"
            else:
                suggestion = "HOLD"
        elif trend == "Flat":
            if score > 0.1:
                suggestion = "HOLD"
            else:
                suggestion = "SELL"
        elif trend == "Downward":
            if score < -0.1:
                suggestion = "BUY"
            else:
                suggestion = "HOLD"

        return render_template("index.html",
                               ticker=ticker,
                               message=message,
                               sentiment=sentiment,
                               score=score,
                               avg_return=avg_return,
                               trend=trend,
                               suggestion=suggestion,
                               graph_path=graph_path)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
