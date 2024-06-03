import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np

# โหลดข้อมูลจากไฟล์ Excel
df = pd.read_excel('train_model1.xlsx', sheet_name='Sheet1')

# แปลงข้อความหมวดหมู่หนังเป็นเวกเตอร์เชิงตัวเลข
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['GenresTH'])

# เตรียมโมเดล KNN
knn = NearestNeighbors(n_neighbors=20, metric='cosine')
knn.fit(X)

# ฟังก์ชันเพื่อแนะนำหนัง
def recommend_movies(genre_input, df, knn, vectorizer):
    genre_vector = vectorizer.transform([genre_input])
    distances, indices = knn.kneighbors(genre_vector, n_neighbors=30)
    
    recommended_titles = df.iloc[indices[0]]['Title'].unique()
    return np.random.choice(recommended_titles, 5, replace=False)

# รับอินพุตจากผู้ใช้
user_input = 'หนังตลก (Comedy)'

# ให้คำแนะนำ
recommended_movies = recommend_movies(user_input, df, knn, vectorizer)
print("Recommended movies:", recommended_movies)
