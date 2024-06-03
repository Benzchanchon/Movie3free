from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

app = Flask(__name__)

# YouTube API credentials
YOUTUBE_API_KEY = 'AIzaSyDWUk8YNuzYY-_6nRpo5KkMP28K-YEL0Uc'

# YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    try:
        response = search_youtube(query + " trailer")
        return jsonify(response)
    except HttpError as e:
        return jsonify({'error': 'An error occurred while accessing the YouTube API', 'details': str(e)}), 500

def search_youtube(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query,
        type="video"
    )
    response = request.execute()
    results = []
    for item in response.get('items', []):
        video = {
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        results.append(video)
    return results

if __name__ == "__main__":
    app.run(port=5001, debug=True)
