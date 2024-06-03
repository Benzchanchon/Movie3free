import threading
import time

# ฟังก์ชันที่จะใช้ในการสร้าง thread
def print_numbers():
    for i in range(5):
        print("Number:", i)
        time.sleep(1)  # หยุดรอเป็นเวลา 1 วินาที

# สร้าง thread
thread = threading.Thread(target=print_numbers)

# เริ่มการทำงานของ thread
thread.start()

# รอให้ thread ทำงานเสร็จสิ้น
thread.join()

print("Thread finished")
