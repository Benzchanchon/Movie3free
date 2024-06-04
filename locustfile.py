import json
from locust import HttpUser, task, between

class MovieRecommendationUser(HttpUser):
    wait_time = between(1, 2)  # รอระหว่าง 1 ถึง 2 วินาทีระหว่าง tasks
    host = "http://localhost:5000"  # กำหนด host สำหรับการทดสอบ

    @task
    def add_user(self):
        payload = {
            'customer_id': '1',  # กำหนด customer_id เป็น 1
            'customer_name': 'Test User',
            'interest_movie': 'Action'
        }
        self.client.post('/users', params=payload)
    
    @task
    def recommend_movie(self):
        self.client.post('/recommend', params={'customer_id': '1'})  # กำหนด customer_id เป็น 1

if __name__ == '__main__':
    import os
    os.system("locust -f locustfile.py")
