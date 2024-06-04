import pika
import json
import redis
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np
import json

# ตั้งค่า RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='recommend_queue')
channel.queue_declare(queue='response_queue')  # Queue สำหรับส่งกลับผลลัพธ์

# ตั้งค่า Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# โหลดข้อมูลและเตรียมโมเดล KNN
df = pd.read_excel('train_model1.xlsx', sheet_name='Sheet1')
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['GenresTH'])
knn = NearestNeighbors(n_neighbors=30, metric='cosine')
knn.fit(X)

def recommend_movies(genre_input, previous_recommendations):
    genre_vector = vectorizer.transform([genre_input])
    distances, indices = knn.kneighbors(genre_vector, n_neighbors=30)
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

def callback(ch, method, properties, body):
    data = json.loads(body)
    customer_id = data['customer_id']
    interest_movie = data['interest_movie']
    print(customer_id)
    print(interest_movie)
    print("################################################")
    previous_recommendations = redis_client.get(customer_id)
    previous_recommendations = json.loads(previous_recommendations) if previous_recommendations else []

    recommended_movies = recommend_movies(interest_movie, previous_recommendations)
    if not recommended_movies:
        previous_recommendations = []
        recommended_movies = recommend_movies(interest_movie, previous_recommendations)
    available_movies = [movie for movie in recommended_movies if movie['Title'] not in previous_recommendations]
    if available_movies:
        recommended_movie = np.random.choice(available_movies, 1, replace=False)[0]
        previous_recommendations.append(recommended_movie['Title'])
        redis_client.set(customer_id, json.dumps(previous_recommendations))
        result = json.dumps(recommended_movie, ensure_ascii=False)
        print(result)
        
        # ส่งผลลัพธ์กลับไปยังคิว response_queue และระบุ correlation_id
        if properties.correlation_id:
            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=result.encode('utf-8')
            )
    else:
        # ส่งข้อความว่าหาไม่เจอหนังที่แนะนำ
        result = json.dumps({'error': 'No more movies to recommend'}, ensure_ascii=False)
        print(result)
        if properties.correlation_id:
            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=result.encode('utf-8')
            )

channel.basic_consume(queue='recommend_queue', on_message_callback=callback, auto_ack=True)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
