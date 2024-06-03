import json
from locust import HttpUser, task, between

class MovieRecommendationUser(HttpUser):
    wait_time = between(1, 2)  # รอระหว่าง 1 ถึง 2 วินาทีระหว่าง tasks

    @task
    def add_user(self):
        payload = {
            'customer_id': 'test_customer_id',
            'customer_name': 'Test User',
            'interest_movie': 'Action'
        }
        self.client.post('/users', params=payload)

if __name__ == '__main__':
    import os
    os.system("locust -f locustfile.py")
