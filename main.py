import mido

def send_response_cc(outport, cc_number, cc_value, channel=0):
    """
    Send a Control Change message.
    
    Parameters:
    - outport: The MIDI output port
    - cc_number: Control Change number to send
    - cc_value: Value of the Control Change message
    - channel: MIDI channel (default is 0)
    """
    msg = mido.Message('control_change', channel=channel, control=cc_number, value=cc_value)
    outport.send(msg)
    print(f"Sent CC message: {msg}")

def send_program_change(outport, program_number, channel=0):
    """
    Send a Program Change message.
    
    Parameters:
    - outport: The MIDI output port
    - program_number: The program number to change to (0-127)
    - channel: MIDI channel (default is 0)
    """
    msg = mido.Message('program_change', channel=channel, program=program_number)
    outport.send(msg)
    print(f"Sent Program Change message: {msg}")

def main():
    input_name = 'Soleman MIDI 1'
    output_name = 'Quad Cortex'
    target_cc_number = 0  # Change this to the incoming CC number you want to detect
    response_cc_number = 0  # Change this to the CC number you want to send in response
    response_cc_value = 0  # Change this to the value of the CC message you want to send
    counter_before_reset = 0
    program_value = 0

    # Open the input port
    with mido.open_input(input_name) as inport:
        # Open the output port
        with mido.open_output(output_name) as outport:
            print(f"Listening for CC {target_cc_number} on {input_name}")
            print(f"Will send CC {response_cc_number} with value {response_cc_value} and PC {program_value} on {output_name}")

            # Loop to receive and process messages
            for msg in inport:
                if msg.type == 'control_change' and msg.control == target_cc_number:
                    print(f"Received target CC message: {msg}")

                    #check if preset 0-128 or 129-256
                    counter_before_reset = (counter_before_reset + 1)
                    if counter_before_reset > 127:
                        if response_cc_value == 1:
                            response_cc_value = 0
                        elif response_cc_value == 0:
                            response_cc_value = 1

                    send_response_cc(outport, response_cc_number, response_cc_value)
                    send_program_change(outport, program_value)
                else:
                    #passthrough if not change
                    print(f"Received message: {msg}")
                    outport.send(msg)
                    print(f"Passing message: {msg}")

if __name__ == "__main__":
    main()
