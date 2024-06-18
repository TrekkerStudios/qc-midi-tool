import mido
import tkinter as tk
import threading

# Initialize global variables
program_value = 1  # Tracks preset
response_cc_number = 0  # Change this to the CC number you want to send in response
response_cc_value = 0  # Change this to the value of the CC message you want to send
input_name = 'mio'  # Change this to the incoming MIDI port name
output_name = 'mio'  # Change this to the outgoing MIDI port name
target_cc_number = 0  # Change this to the incoming CC number you want to detect

def send_response_cc(outport, cc_number, cc_value, channel=0):
    msg = mido.Message('control_change', channel=channel, control=cc_number, value=cc_value)
    outport.send(msg)
    print(f"Sent CC message: {msg}")

def send_program_change(outport, program_number, channel=0):
    msg = mido.Message('program_change', channel=channel, program=program_number)
    outport.send(msg)
    print(f"Sent Program Change message: {msg}")

def midi_listen():
    global program_value
    global response_cc_value

    # Open the input and output ports
    with mido.open_input(input_name) as inport, mido.open_output(output_name) as outport:
        print(f"Listening for CC {target_cc_number} on {input_name}")
        print(f"Will send CC {response_cc_number} with value {response_cc_value} and PC {program_value} on {output_name}")

        # Loop to receive and process messages
        for msg in inport:
            if msg.type == 'control_change' and msg.control == target_cc_number and msg.value == 127:
                print(f"Received target CC message: {msg}")

                # Check if preset 0-128 or 129-256
                if program_value == 127:
                    response_cc_value = 1 if response_cc_value == 0 else 0
                    program_value = 0

                send_response_cc(outport, response_cc_number, response_cc_value)
                send_program_change(outport, program_value)

                program_value += 1
                update_label()
            else:
                # Passthrough if not change
                print(f"Received message: {msg}")
                outport.send(msg)
                print(f"Passing message: {msg}")

# Function to reset the counter
def reset_counter():
    global program_value
    global response_cc_value
    program_value = 1
    response_cc_value = 0
    update_label()

# Function to update the label with the current counter value
def update_label():
    counter_label.config(text=f"Program Value: {program_value}")
    response_cc_label.config(text=f"Response CC Value: {response_cc_value}")

# Create the main window
root = tk.Tk()
root.title("QC MIDI TOOL")

# Create a label to display the counter
counter_label = tk.Label(root, text=f"Program Value: {program_value}", font=("Helvetica", 48))
counter_label.pack(pady=20, padx=40)

# Create a label to display the response CC value
response_cc_label = tk.Label(root, text=f"Response CC Value: {response_cc_value}", font=("Helvetica", 24))
response_cc_label.pack(pady=20, padx=40)

# Create a button to reset the counter
reset_button = tk.Button(root, text="Reset", command=reset_counter, font=("Helvetica", 24))
reset_button.pack(pady=20, padx=40)

# Start the MIDI listener in a separate thread
midi_thread = threading.Thread(target=midi_listen, daemon=True)
midi_thread.start()

# Start the Tkinter event loop
root.mainloop()