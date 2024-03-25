#Galih Putra Aditama (2602227421)
import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = []  # Shared buffer to store generated numbers
lock = threading.Lock()  # Lock for protecting access to the buffer
condition = threading.Condition()  # Condition variable for synchronization

def producer():
    global buffer
    with condition:
        for _ in range(MAX_COUNT):
            num = random.randint(LOWER_NUM, UPPER_NUM)
            with lock:
                buffer.append(num)  # Add generated number to the buffer
                with open("all.txt", "a") as f:
                    f.write(str(num) + "\n")  # Log the generated number to 'all.txt'
            condition.notify_all()  # Notify waiting consumers

def customer_odd():
    global buffer
    with condition:
        while True:
            condition.wait_for(lambda: buffer and buffer[-1] % 2 != 0 or not buffer)  # Wait until an odd number is available or until the buffer is empty
            if not buffer:  # Exit loop if buffer is empty (producer is done)
                break
            num = buffer.pop()  # Consume the last number from the buffer
            with open("odd.txt", "a") as f:
                f.write(str(num) + "\n")  # Log the consumed odd number to 'odd.txt'

def customer_even():
    global buffer
    with condition:
        while True:
            condition.wait_for(lambda: buffer and buffer[-1] % 2 == 0 or not buffer)  # Wait until an even number is available or until the buffer is empty
            if not buffer:  # Exit loop if buffer is empty (producer is done)
                break
            num = buffer.pop()  # Consume the last number from the buffer
            with open("even.txt", "a") as f:
                f.write(str(num) + "\n")  # Log the consumed even number to 'even.txt'

if __name__ == "__main__":
    producer_thread = threading.Thread(target=producer)
    odd_customer_thread = threading.Thread(target=customer_odd)
    even_customer_thread = threading.Thread(target=customer_even)

    producer_thread.start()
    odd_customer_thread.start()
    even_customer_thread.start()

    producer_thread.join()
    odd_customer_thread.join()
    even_customer_thread.join()
