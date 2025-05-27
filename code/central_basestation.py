import cv2
import cv2.aruco as aruco
import numpy as np
import socket
import time
import threading

ARUCO_IDS = [1, 3]
PROXIMITY_THRESHOLD = 400 
SPEED_THRESHOLD = 15       
STATUS_UPDATE_INTERVAL = 0.1

tracker = {
    1: {'position': None, 'last_time': None, 'status': None, 'speed': 0.0, 'last_sent': {}},
    3: {'position': None, 'last_time': None, 'status': None,  'speed': 0.0,'last_sent': {}}
}

detected = {}

# socket setup 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 5000))
server_socket.listen(5)
print("Server started, waiting for RC vehicles to connect...")

client_sockets = {}

def accept_clients():
    while True:
        client, addr = server_socket.accept()
        ip = addr[0]
        try:
            client.settimeout(5.0)
            data = client.recv(1024)
            if not data:
                raise ValueError("Empty data")
            
            try:
                client_id = int(data.decode().strip())
            except ValueError:
                raise ValueError("Non-integer client ID")

            if client_id in client_sockets:
                raise ValueError(f"Duplicate client ID: {client_id}")

            client_sockets[client_id] = client
            print(f"Connected ID {client_id} from {ip}")
        except Exception as e:
            print(f" Failed to connect  {ip}: {e}")
            client.close()
            
threading.Thread(target=accept_clients, daemon=True).start()


def estimate_speed(curr_pos, prev_pos, dt):
    if prev_pos is None or dt == 0:
        return 0.0
    dist = np.linalg.norm(np.array(curr_pos) - np.array(prev_pos))
    return dist / dt

def send_command(car_id, message):
    if car_id in client_sockets:
        try:
            client_sockets[car_id].send((message + "\n").encode())
            print(f"Send to Car {car_id}: {message}")
       
        except:
        
            print(f"Error in sending to Car {car_id}")
            client_sockets.pop(car_id)

# ArUco Setup 
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco.detectMarkers(gray,  aruco_dict,  parameters=parameters)

    detected.clear()


    if ids is not None:
        ids = ids.flatten()
        for i, marker_id in enumerate(ids):
            marker_id = int(marker_id)
            if marker_id not in ARUCO_IDS:
                continue

            corner = corners[i][0]
            center = tuple(np.mean(corner, axis=0).astype(int))
            detected[marker_id] = center


            # Draw marker and ID
            cv2.circle(frame, center, 6, (255, 0, 0), -1)
            cv2.putText(frame, f"ID {marker_id}", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Tracking and status update
            last_pos = tracker[marker_id]['position']
            last_time = tracker[marker_id]['last_time']
            status = tracker[marker_id]['status']


            if last_time is None or (current_time - last_time >= STATUS_UPDATE_INTERVAL):
                dt = current_time - last_time if last_time else 0
                speed = estimate_speed(center, last_pos, dt)
                new_status = "moving" if speed > SPEED_THRESHOLD else "stopped"
                
                tracker[marker_id]['speed'] = speed

                if new_status != status:
                    print(f" Car {marker_id}: {new_status.upper()} (Speed: {speed:.2f})")
                    tracker[marker_id]['status'] = new_status

                tracker[marker_id]['position'] = center
                tracker[marker_id]['last_time'] = current_time

            # Show status on frame
            display_status = tracker[marker_id]['status'] or "unknown"
            cv2.putText(frame, f"{display_status}", (center[0], center[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Proximity check 
        
    if 1 in detected and 3 in detected:
        dist = np.linalg.norm(np.array(detected[1]) - np.array(detected[3]))
        cv2.line(frame, detected[1], detected[3], (255, 0, 255), 2)
        cv2.putText(frame, f"Distance: {int(dist)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        if dist < PROXIMITY_THRESHOLD:
            for marker_id in [1, 3]:
                last_sent = tracker[marker_id]['last_sent']
                if not last_sent.get("proximity_alert"):
                    send_command(marker_id, "proximity_alert")
                    last_sent["proximity_alert"] = True


            # faster car change ltrack
            speed_1 = tracker[1].get('speed')
            speed_3 = tracker[3].get('speed')

            if speed_1 > speed_3 and tracker[1]['status'] == "moving":
                if not tracker[1]['last_sent'].get("50"):
                    send_command(1, "50")
                    tracker[1]['last_sent']["50"] = True
                    print("1 change track")
            elif speed_3 > speed_1 and tracker[3]['status'] == "moving":
                if not tracker[3]['last_sent'].get("50"):
                    send_command(3, "50")
                    tracker[3]['last_sent']["50"] = True
                    print("3 change track")
                    

        else:
            for marker_id in [1, 3]:
                last_sent = tracker[marker_id]['last_sent']
                if last_sent.get("proximity_alert") or last_sent.get("50"):
                    print(f"Reset Proximity cleared for Car {marker_id}")
                    last_sent.pop("proximity_alert", None)
                    last_sent.pop("50", None)
                
                    if not last_sent.get("90"):
                        send_command(marker_id, "90")
                        last_sent["90"] = True

                else:
            
                    last_sent.pop("90", None)

    # Display 
    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Cleanup 
cap.release()
cv2.destroyAllWindows()
server_socket.close()
for sock in client_sockets.values():
    sock.close()
