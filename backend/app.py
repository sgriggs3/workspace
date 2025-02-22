# backend/app.py
from flask import Flask, request, jsonify
from sentiment_analysis import analyze_sentiment, get_video_sentiment, get_channel_sentiment

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_comments():
    comments = request.json.get('comments', [])
    scores = analyze_sentiment(comments)
    return jsonify({"scores": scores})

@app.route('/analyze/<granularity>', methods=['POST'])
def handle_analysis(granularity):
    data = request.json
    if granularity == "comment":
        scores = analyze_sentiment(data['comments'])
    elif granularity == "video":
        scores = get_video_sentiment(data['comment_scores'])
    elif granularity == "channel":
        # Assuming video_scores are provided for channel-level analysis
        scores = get_channel_sentiment(data['video_scores'])
    else:
        return jsonify({"error": "Invalid granularity"}), 400
    return jsonify(scores)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Consider removing debug=True for production