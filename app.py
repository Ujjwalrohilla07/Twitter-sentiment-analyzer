from flask import Flask, render_template, request
from textblob import TextBlob
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Analyze route
@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']

    tweets = text.split('\n')
    results = []

    # Initialize counters
    pos = 0
    neu = 0
    neg = 0

    # Process each tweet
    for tweet in tweets:
        if tweet.strip() == "":
            continue

        blob = TextBlob(tweet)
        polarity = blob.sentiment.polarity

        if polarity > 0:
            sentiment = "Positive 😊"
            pos += 1
        elif polarity < 0:
            sentiment = "Negative 😠"
            neg += 1
        else:
            sentiment = "Neutral 😐"
            neu += 1

        results.append((tweet, sentiment))

    # Create graph data
    labels = ["Positive", "Neutral", "Negative"]
    values = [pos, neu, neg]

    # Plot graph
    plt.figure()
    plt.bar(labels, values)
    plt.title("Overall Sentiment Analysis")

    # Save graph in static folder
    graph_path = os.path.join(app.root_path, 'static', 'graph.png')

    # Ensure static folder exists
    if not os.path.exists(os.path.dirname(graph_path)):
        os.makedirs(os.path.dirname(graph_path))

    plt.savefig(graph_path)
    plt.close()

    return render_template('index.html',
                           results=results,
                           pos=pos,
                           neu=neu,
                           neg=neg,
                           graph='graph.png')


if __name__ == '__main__':
    app.run(debug=True)