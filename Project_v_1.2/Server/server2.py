from flask import Flask, jsonify, request
import requests
import json
import threading
import keyboard
import time








app = Flask(__name__)
url = "http://localhost:8090/api/objects/info?format=json"

latest_command = "Idle"
latest_speed = 'f'
stop_thread = False
lock = threading.Lock()



@app.route('/track')
def object_data():
    result_data_gui = requests.get(url).json()
    alt = result_data_gui["altitude"]
    az = result_data_gui["azimuth"]
    above = result_data_gui["above-horizon"]
    if above == "false":
        above = False
    else:
        above = True

    print(alt, az, above)
    return jsonify({
            'altitude_deg': alt,
            'azimuth_deg': az,
            'above-horizon': above
        })


@app.route('/calibrate', methods=['GET'])
def calibrate():
    global latest_command
    global stop_thread
    global latest_speed

    try:
        # Fetch data from the Stellarium API
        result_data_gui = requests.get(url).json()
        alt = result_data_gui["altitude"]
        az = result_data_gui["azimuth"]
        above = result_data_gui["above-horizon"]

        # Convert the string to a boolean
        if above == "false":
            above = False
        else:
            above = True

        # Get the latest command from the shared variable
        with lock:
            command_to_process = latest_command
            speed = latest_speed
            if command_to_process != "Idle" and command_to_process != "stop":
                # Reset the command to "Idle" after it's been read
                latest_command = "Idle"
            # Optional: reset the command after it's been processed once
            # latest_command = "Idle"
        if command_to_process == "stop":
            stop_thread = True

        print(f"Flask route accessed. Latest command: {command_to_process}")

        # This is where you'd add the logic to send 'command_to_process' to your ESP32.
        # Example: requests.post("http://<esp32_ip>/motor", json={'command': command_to_process})

        return jsonify({
            'altitude_deg': alt,
            'azimuth_deg': az,
            'above-horizon': above,
            'command': command_to_process,
            'speed': speed
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to Stellarium API', 'details': str(e)}), 500
    except (KeyError, json.JSONDecodeError) as e:
        return jsonify({'error': 'Invalid data from Stellarium API', 'details': str(e)}), 500

def keyboard_listener_thread():
    """
    A separate thread that listens for keyboard input and updates a global variable.
    Stops when 'stop_thread' is set to True.
    """
    global latest_command
    global stop_thread
    global latest_speed

    def on_key_press(event):
        global latest_command
        global latest_speed
        valid_keys = ['w', 'a', 's', 'd']
        valid_speeds = ['f', 'g']

        if event.name in valid_keys:
            with lock:
                latest_command = event.name
            print(f"Key listener detected: {event.name}")
        elif event.name in valid_speeds:
            with lock:
                latest_speed = event.name
            print(f"Key listener detected: {event.name}")
        elif event.name == 'q':
            with lock:
                latest_command = "stop"
            print("Key listener detected 'q'. Setting command to 'stop'.")

    keyboard.on_press(on_key_press)

    print("Keyboard listener started. To calibrate, use W A S D for movement, F for 'fast' speed and G for 'slow', Q to quit")

    # This loop keeps the thread alive until 'stop_thread' is True
    while not stop_thread:
        time.sleep(0.05)

    print("Keyboard listener stopping.")
    # Stop the keyboard hook
    keyboard.unhook_all()



def run_flask():
    app.run(host='0.0.0.0', port=5000)
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    listener_thread = threading.Thread(target=keyboard_listener_thread, daemon=True)
    listener_thread.start()
    run_flask()



