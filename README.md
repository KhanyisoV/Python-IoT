#Facility Monitoring Server
A multi-threaded Python server application for real-time facility occupancy monitoring and activity logging. This system tracks personnel entry/exit events and maintains comprehensive logs of all facility activities.
##Overview
This server application manages connected IoT devices (entry systems, safety systems) to monitor facility occupancy in real-time. It uses socket programming and multi-threading to handle multiple device connections simultaneously, logging all events with timestamps.
Features

Real-time Occupancy Tracking: Monitors the current number of people in the facility
Multi-device Support: Handles multiple connected devices concurrently using threading
Activity Logging: Records all events with timestamps to activity_log.txt
Emergency Protocol: Automatic evacuation count reset when safety system is activated
Thread-safe Operations: Uses locks to prevent race conditions on shared resources

#Requirements

Python 3.x
Standard library modules:

socket
threading
datetime



###Configuration
The server is configured with the following default settings:
pythonSERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
Modify these values in the source code if you need to run the server on a different address or port.
Usage
Starting the Server
Run the server with:
bashpython server.py
```

The server will start listening for device connections and display:
```
Facility Monitoring Server running...
```

### Device Communication Protocol

Connected devices should send the following commands:

| Command | Description | Effect |
|---------|-------------|--------|
| `SafetySystem_Active` | Emergency evacuation triggered | Resets occupancy to 0 |
| `EntrySystem_Active` | Entry system comes online | Logs system activation |
| `PersonEntered` | Someone enters the facility | Increments occupancy count |
| `PersonExited` | Someone leaves the facility | Decrements occupancy count |

## Log Format

All activities are logged to `activity_log.txt` in the following format:
```
YYYY-MM-DD HH:MM:SS, [Activity Description], [Current Occupancy]
```

**Example:**
```
2025-01-11 14:30:45, Person entered facility, 5
2025-01-11 14:32:10, Person left facility, 4
2025-01-11 15:00:00, Safety system activated, 0
Architecture
Multi-threading Design

Main Thread: Runs the connection listener
Connection Handler Thread: Accepts new device connections
Device Handler Threads: One thread per connected device for message processing

##Thread Safety
The application uses:

threading.Lock() to protect the connected_devices list from concurrent modification
Thread-safe file writing with context managers

#Functions
record_activity(activity_message)
Logs an activity with timestamp and current occupancy to both console and file.
handle_device_connection(device_socket, device_address)
Manages communication with a single connected device. Processes incoming commands and updates occupancy counts.
wait_for_connections(main_socket)
Continuously listens for new device connections and spawns handler threads.
Error Handling

Connection Reset: Gracefully handles device disconnections and logs the event
Socket Cleanup: Properly closes sockets and removes them from the connected devices list

##Student Information
Student ID: s224252941
Name: Khanyiso Vabaza
License
This project is developed for educational purposes.
Future Enhancements

##Add authentication for connected devices
Implement maximum occupancy alerts
Create a web dashboard for real-time monitoring
Add database support for historical data analysis
Implement device heartbeat monitoring
