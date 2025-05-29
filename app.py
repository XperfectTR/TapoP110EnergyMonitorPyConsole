import curses
from PyP100 import PyP110
import datetime
import time
import os
import sys
import socket # For network-related errors
# Attempt to import requests.exceptions for more specific error handling
try:
    import requests.exceptions
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# --- Global Variables ---
power_usage_data = [] # List to store power usage data

# --- UI Configuration ---
# Line numbers for UI elements
Y_DEVICE_STATUS = 0
Y_CURRENT_POWER = 1
Y_TODAY_ENERGY = 2 # New line for Today's Total Energy
# Line 3: Blank (Implicitly, or Y_STATS_HEADER can start here if no blank needed)
Y_STATS_HEADER = 4 # Was 3
Y_MIN_POWER = 5    # Was 4
Y_MAX_POWER = 6    # Was 5
Y_AVG_POWER = 7    # Was 6
# Line 8: Blank (Implicitly)
Y_ACTION_STATUS = 9 # Was 8
Y_INSTRUCTIONS = 10 # Was 9
# Line 11: Blank (Implicitly)
Y_ERROR_LINE = 12   # Was 11

# Messages
current_error_message = "" # Stores the current error message
current_action_message = "" # Stores temporary action messages like "Toggling..."
last_action_time = 0 # Timestamp of the last action message
ACTION_MSG_DURATION = 2 # Seconds to display action message

# --- Helper Functions for UI ---

def safe_addstr(stdscr, y, x, text, attr=0):
    """Safely add a string to the screen, handling potential errors."""
    try:
        if y < curses.LINES and x < curses.COLS and (x + len(text)) < curses.COLS:
            stdscr.addstr(y, x, text, attr)
    except curses.error:
        pass

def clear_line(stdscr, y):
    """Clears a specific line."""
    safe_addstr(stdscr, y, 0, " " * (curses.COLS - 1))

def display_message(stdscr, y, message, is_error=False):
    """Displays a message on a specific line, clearing it first."""
    global current_error_message, current_action_message, last_action_time
    
    clear_line(stdscr, y)
    if message:
        safe_addstr(stdscr, y, 0, message)

    if is_error:
        current_error_message = message
    else:
        current_action_message = message
        last_action_time = time.time()

def clear_error_message_data():
    global current_error_message
    current_error_message = ""

def clear_action_message_data():
    global current_action_message
    current_action_message = ""

# --- Core Logic Functions ---

def update_energy_statistics():
    """Calculates and prepares strings for energy statistics."""
    stats_strings = {
        "header": "Energy Statistics:",
        "min": "Min Power: --- W",
        "max": "Max Power: --- W",
        "avg": "Avg Power: --- W"
    }
    if power_usage_data:
        powers = [power for _, power in power_usage_data]
        if powers:
            min_power = min(powers)
            max_power = max(powers)
            avg_power = sum(powers) / len(powers)
            stats_strings["min"] = f"Min Power: {min_power:.2f} W"
            stats_strings["max"] = f"Max Power: {max_power:.2f} W"
            stats_strings["avg"] = f"Avg Power: {avg_power:.2f} W"
    return stats_strings

def get_device_data(p110_device):
    """Fetches device status and energy usage. Returns data or error message."""
    global current_error_message 
    try:
        clear_error_message_data() 

        device_info = p110_device.getDeviceInfo()
        status = "On" if device_info['device_on'] else "Off"
        
        energy_usage_dict = p110_device.getEnergyUsage()
        current_power_watts = energy_usage_dict.get('current_power', 0) / 1000.0 # Default to 0 if key missing
        
        # Attempt to get today's energy from getEnergyUsage()
        today_energy_wh = energy_usage_dict.get('today_energy', None) # In Wh typically
        
        today_energy_str = "Today's Energy: --- kWh"
        if today_energy_wh is not None:
            today_energy_kwh = today_energy_wh / 1000.0
            today_energy_str = f"Today's Energy: {today_energy_kwh:.2f} kWh"
        else:
            # Fallback or alternative: try getDailyEnergy if today_energy is not in getEnergyUsage
            # This part assumes getDailyEnergy(year, month, day) exists and returns a list/dict
            # For now, we'll just stick to the placeholder if not found in getEnergyUsage for simplicity
            # as per the current interpretation of the task. If getDailyEnergy is required,
            # it would involve more error handling for that specific call.
            # Example for a future step if needed:
            # now = datetime.datetime.now()
            # daily_energy_data = p110_device.getDailyEnergy(now.year, now.month, now.day)
            # if daily_energy_data and isinstance(daily_energy_data, (list, dict)): # process it
            pass


        current_time_dt = datetime.datetime.now() # Renamed to avoid conflict
        power_usage_data.append((current_time_dt, current_power_watts))
        max_records = 36000 
        if len(power_usage_data) > max_records:
            power_usage_data.pop(0)
        
        return {
            "status": f"Device Status: {status}",
            "current_power": f"Current Power: {current_power_watts:.2f} W",
            "today_energy_str": today_energy_str
        }

    except KeyError as e:
        current_error_message = f"Error: Data format error (KeyError: {e})."
    except (socket.error, OSError) as e:
        current_error_message = f"Error: Network issue ({type(e).__name__}: {e})."
    except AttributeError as e: # If a method like getEnergyUsage() itself is missing
        current_error_message = f"Error: Device API attribute error ({type(e).__name__}: {e})."
    except Exception as e:
        if REQUESTS_AVAILABLE and isinstance(e, requests.exceptions.RequestException):
            current_error_message = f"Error: Device comms failed (RequestException: {e})."
        else:
            current_error_message = f"Error: Unexpected ({type(e).__name__}: {e})."
    # Ensure all expected keys are present in the return dictionary even on error, with default values
    return {
        "status": "Device Status: ---",
        "current_power": "Current Power: --- W",
        "today_energy_str": "Today's Energy: --- kWh" # Default value on error
    }


def do_toggle_device(p110_device): 
    """Toggles device state. Returns action message or sets error message."""
    global current_error_message, current_action_message, last_action_time 
    try:
        clear_error_message_data()
        clear_action_message_data()

        device_info = p110_device.getDeviceInfo() 
        if device_info['device_on']:
            p110_device.turnOff() 
            current_action_message = "Device turning Off..."
        else:
            p110_device.turnOn() 
            current_action_message = "Device turning On..."
        
        last_action_time = time.time()
        time.sleep(0.5) 
        
        updated_device_info = p110_device.getDeviceInfo() 
        new_status_on = updated_device_info['device_on']
        if (device_info['device_on'] and not new_status_on) or \
           (not device_info['device_on'] and new_status_on):
            current_action_message = f"Device is now {'On' if new_status_on else 'Off'}."
            last_action_time = time.time() 
        else:
            current_action_message = "Device state did not change as expected."
            last_action_time = time.time()

    except KeyError as e:
        current_error_message = f"Error: Toggle data format (KeyError: {e})."
    except (socket.error, OSError) as e:
        current_error_message = f"Error: Toggle network issue ({type(e).__name__}: {e})."
    except AttributeError as e:
        current_error_message = f"Error: Toggle API attribute error ({type(e).__name__}: {e})."
    except Exception as e:
        if REQUESTS_AVAILABLE and isinstance(e, requests.exceptions.RequestException):
            current_error_message = f"Error: Toggle device comms failed (RequestException: {e})."
        else:
            current_error_message = f"Error: Toggle unexpected ({type(e).__name__}: {e})."


def initialize_device(): 
    tapo_ip = os.getenv("TAPO_IP")
    tapo_email = os.getenv("TAPO_EMAIL")
    tapo_password = os.getenv("TAPO_PASSWORD")

    if not all([tapo_ip, tapo_email, tapo_password]):
        print("Fatal Error: TAPO_IP, TAPO_EMAIL, and TAPO_PASSWORD env vars must be set.", file=sys.stderr)
        sys.exit(1)

    local_p110 = PyP110.P110(tapo_ip, tapo_email, tapo_password) 
    
    try:
        local_p110.handshake()
        local_p110.login()
        return local_p110 
    except Exception as e:
        print(f"Fatal Error: Device handshake or login failed.", file=sys.stderr)
        print(f"Details: {type(e).__name__}: {e}", file=sys.stderr)
        print("Check credentials, IP, and device reachability.", file=sys.stderr)
        sys.exit(1) 

def main(stdscr, p110_instance): 
    global current_error_message, current_action_message, last_action_time 
    
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100) 

    while True:
        stdscr.clear()

        if current_action_message and (time.time() - last_action_time > ACTION_MSG_DURATION):
            clear_action_message_data()
            clear_line(stdscr, Y_ACTION_STATUS)

        device_data = get_device_data(p110_instance) 
        energy_stats = update_energy_statistics() 

        # Display data from device_data (which now includes defaults on error)
        safe_addstr(stdscr, Y_DEVICE_STATUS, 0, device_data["status"].ljust(curses.COLS -1))
        safe_addstr(stdscr, Y_CURRENT_POWER, 0, device_data["current_power"].ljust(curses.COLS -1))
        safe_addstr(stdscr, Y_TODAY_ENERGY, 0, device_data["today_energy_str"].ljust(curses.COLS-1)) # New line

        # Display stats
        safe_addstr(stdscr, Y_STATS_HEADER, 0, energy_stats["header"])
        safe_addstr(stdscr, Y_MIN_POWER, 0, energy_stats["min"].ljust(curses.COLS -1))
        safe_addstr(stdscr, Y_MAX_POWER, 0, energy_stats["max"].ljust(curses.COLS -1))
        safe_addstr(stdscr, Y_AVG_POWER, 0, energy_stats["avg"].ljust(curses.COLS -1))
        
        instructions_text = "Enter: Toggle | Q: Quit".ljust(curses.COLS -1)
        safe_addstr(stdscr, Y_INSTRUCTIONS, 0, instructions_text)


        if current_action_message:
            display_message(stdscr, Y_ACTION_STATUS, current_action_message, is_error=False)
        else: 
            clear_line(stdscr, Y_ACTION_STATUS)

        if current_error_message:
            display_message(stdscr, Y_ERROR_LINE, current_error_message, is_error=True)
        else: 
            clear_line(stdscr, Y_ERROR_LINE)
        
        try:
            key = stdscr.getch() 
        except curses.error: 
            key = -1

        if key == 10 or key == curses.KEY_ENTER:
            clear_action_message_data()
            clear_line(stdscr, Y_ACTION_STATUS)
            do_toggle_device(p110_instance) 
        elif key == ord('q') or key == ord('Q'):
            break
        
        stdscr.refresh()

if __name__ == "__main__":
    if not all(os.getenv(var) for var in ["TAPO_IP", "TAPO_EMAIL", "TAPO_PASSWORD"]):
        print("Fatal Error: TAPO_IP, TAPO_EMAIL, and TAPO_PASSWORD environment variables must be set.", file=sys.stderr)
        print("Example (Linux/macOS): export TAPO_IP=\"your_ip\"", file=sys.stderr)
        sys.exit(1)
    
    p110_initialized_instance = initialize_device() 
    curses.wrapper(lambda stdscr: main(stdscr, p110_initialized_instance))
