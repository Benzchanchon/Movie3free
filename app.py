from flask import Flask, request, jsonify
from flask_session import Session
from models import db, User
from config import Config
from datetime import datetime, timedelta
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np
import json
import redis
import jwt
from concurrent.futures import ThreadPoolExecutor
from googleapiclient.discovery import build
import pika
import pytz

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'supersecretkey'

# YouTube API credentials
YOUTUBE_API_KEY = 'AIzaSyC4PDLc-MzSrSFnGjP_hIYGvog7XKt8usI'

# YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# การตั้งค่าสำหรับ Flask-Session และ Redis
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'session:'
app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)

# Initialize session
Session(app)

db.init_app(app)

with app.app_context():
    db.create_all()

# โหลดข้อมูลจากไฟล์ Excel
df = pd.read_excel('train_model1.xlsx', sheet_name='Sheet1')

# แปลงข้อความหมวดหมู่หนังเป็นเวกเตอร์เชิงตัวเลข
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['GenresTH'])

# เตรียมโมเดล KNN
knn = NearestNeighbors(n_neighbors=70, metric='cosine')
knn.fit(X)

# ฟังก์ชันเพื่อแนะนำหนัง
def recommend_movies(genre_input, previous_recommendations):
    genre_vector = vectorizer.transform([genre_input])
    distances, indices = knn.kneighbors(genre_vector, n_neighbors=50)
    
    recommended_indices = indices[0]
    recommended_movies = df.iloc[recommended_indices]

    recommended_list = []
    for _, row in recommended_movies.iterrows():
        movie_info = {
            'Title': row['Title'],
            'GenresTH': row['GenresTH'],
            'Poster': row['Poster'],
            'Description': row['Description'],
            'website': row.get('website')
        }
        if movie_info['Title'] not in previous_recommendations:
            recommended_list.append(movie_info)

    return recommended_list

def create_jwt(customer_id, customer_name, interest_movie_choose):
    payload = {
        'customer_id': customer_id,
        'customer_name': customer_name,
        'interest_movie_choose': interest_movie_choose,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    return token

@app.route('/users', methods=['POST'])
def add_user():
    customer_id = request.args.get('customer_id')
    customer_name = request.args.get('customer_name')
    interest_movie = request.args.get('interest_movie')
    
    if not customer_id or not customer_name or not interest_movie:
        return jsonify({'error': 'customer_id, customer_name, and interest_movie are required'}), 400

    user = User.query.filter_by(customer_id=customer_id).first()
       # กำหนดเวลาไทย
    thailand_tz = pytz.timezone('Asia/Bangkok')
    current_time_thailand = datetime.now(thailand_tz)

    if user:
        user.customer_name = customer_name
        user.interest_movie = interest_movie
        user.date = current_time_thailand
        
        # Update interest_movie_choose with non-duplicate values
        current_interests = user.interest_movie_choose.split(',') if user.interest_movie_choose else []
        if interest_movie not in current_interests:
            current_interests.append(interest_movie)
        # Limit to 3 interests
        if len(current_interests) > 3:
            current_interests = current_interests[-3:]
        user.interest_movie_choose = ','.join(current_interests)

        token = create_jwt(customer_id, customer_name, user.interest_movie_choose)
        user.token = token

        db.session.commit()
        message = 'User updated successfully'
    else:
        interest_movie_choose = interest_movie
        token = create_jwt(customer_id, customer_name, interest_movie_choose)
        
        new_user = User(
            customer_id=customer_id,
            customer_name=customer_name,
            interest_movie=interest_movie,
            date=current_time_thailand,
            token=token,
            interest_movie_choose=interest_movie_choose
        )
        db.session.add(new_user)
        db.session.commit()
        message = 'User created successfully'

    return jsonify({'message': message, 'token': token}), 201

executor = ThreadPoolExecutor(max_workers=4)

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def search_youtube(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query,
        type="video"
    )
    response = request.execute()
    if response['items']:
        item = response['items'][0]
        video = {
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        return video
    return None

def send_to_rabbitmq(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='recommend_queue')
    channel.basic_publish(exchange='', routing_key='recommend_queue', body=json.dumps(data))
    connection.close()

@app.route('/recommend', methods=['POST'])
def recommend():
    customer_id = request.args.get('customer_id')

    if not customer_id:
        return jsonify({'error': 'customer_id is required'}), 400

    user = User.query.filter_by(customer_id=customer_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    interest_movie = user.interest_movie

    # ดึงข้อมูล movie_watched จาก Redis
    previous_recommendations = redis_client.get(customer_id)
    previous_recommendations = json.loads(previous_recommendations) if previous_recommendations else []

    recommended_movies = recommend_movies(interest_movie, previous_recommendations)
    
    if not recommended_movies:
        previous_recommendations = []
        recommended_movies = recommend_movies(interest_movie, previous_recommendations)

    available_movies = [movie for movie in recommended_movies if movie['Title'] not in previous_recommendations]
    
    if not available_movies:
        return jsonify({'error': 'No more movies to recommend'}), 404
    
    recommended_movie = np.random.choice(available_movies, 1, replace=False)[0]
    
    previous_recommendations.append(recommended_movie['Title'])
    redis_client.set(customer_id, json.dumps(previous_recommendations))

    future = executor.submit(search_youtube, recommended_movie['Title'] + " Trailer")
    youtube_video = future.result()

    data = {
        'customer_id': customer_id,
        'interest_movie': interest_movie
    }
    executor.submit(send_to_rabbitmq, data)

    return jsonify({
        'Title': recommended_movie['Title'],
        'GenresTH': recommended_movie['GenresTH'],
        'Poster': recommended_movie['Poster'],
        'Description': recommended_movie['Description'],
        'website': recommended_movie['website'],
        'youtube_video': youtube_video
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
