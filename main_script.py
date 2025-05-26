
#s224252941 - Khanyiso Vabaza
#s224178059 - Sivuyisiwe Maqundeni


import datetime
import threading
import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

current_occupancy = 0

connected_devices = []
connection_lock = threading.Lock()


def record_activity(activity_message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp}, {activity_message}, {current_occupancy}"
    with open('activity_log.txt', 'a') as log_file:
        log_file.write(log_entry + '\n')
    print(log_entry)


def handle_device_connection(device_socket, device_address):
    global current_occupancy
    print(f"Connection established with {device_address}")
    try:
        while True:
            received_data = device_socket.recv(1024).decode()

           
            if received_data == "SafetySystem_Active":
                record_activity("Safety system activated")
                current_occupancy = 0
                record_activity("Emergency protocol - Facility evacuated")

            if received_data == "EntrySystem_Active":
                record_activity("Entry system online")
            elif received_data.startswith("PersonEntered"):
                current_occupancy += 1
                record_activity("Person entered facility")
            elif received_data.startswith("PersonExited"):
                current_occupancy -= 1
                record_activity("Person left facility")

    except ConnectionResetError:
        print("Device connection terminated.")
        record_activity("Device disconnected")
        device_socket.close()
        with connection_lock:
            connected_devices.remove(device_socket)


def wait_for_connections(main_socket):
    while True:
        socket_connection, device_info = main_socket.accept()
        with connection_lock:
            connected_devices.append(socket_connection)
        device_handler = threading.Thread(target=handle_device_connection, args=(socket_connection, device_info))
        device_handler.start()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as main_socket:
    main_socket.bind((SERVER_IP, SERVER_PORT))
    main_socket.listen()
    print("Facility Monitoring Server running...")

    connection_handler = threading.Thread(target=wait_for_connections, args=(main_socket,))
    connection_handler.start()
    connection_handler.join()
