import cv2
import threading
import time
from collections import deque

class RingBuffer:
    def __init__(self, size):
        self.buffer = deque(maxlen=size)
        self.lock = threading.Lock()

    def add(self, item):
        with self.lock:
            if len(self.buffer) == self.buffer.maxlen:
                print("Buffer full. Dropping oldest frame.")
            self.buffer.append(item)

    def get(self):
        with self.lock:
            if self.buffer:
                return self.buffer.popleft()
            else:
                return None

def producer(buffer, cap):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        buffer.add(frame)
        time.sleep(0.03)  # simulate frame capture interval

def consumer(buffer):
    while True:
        frame = buffer.get()
        if frame is not None:
            # Display the frame (or any other processing)
            cv2.imshow('Consumer', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            time.sleep(0.01)  # wait a bit if buffer is empty

def main():
    buffer_size = 10  # size of the ring buffer
    buffer = RingBuffer(buffer_size)

    cap = cv2.VideoCapture(0)

    producer_thread = threading.Thread(target=producer, args=(buffer, cap))
    consumer_thread = threading.Thread(target=consumer, args=(buffer,))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
