import threading

# A shared variable
counter = 0

# Create a lock
lock = threading.Lock()

# A function to modify the shared variable
def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

# Create threads that run the `increment` function
thread1 = threading.Thread(target=increment)
thread2 = threading.Thread(target=increment)

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print(f"Final counter value: {counter}")