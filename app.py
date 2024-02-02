import curses
from PyP100 import PyP110
import datetime
import time

# Create P110 object
p110 = PyP110.P110("IP", "email@gmail.com", "password")
p110.handshake()
p110.login()

# List to store power usage data
power_usage_data = []

def update_energy_statistics(stdscr, y=2):
    if power_usage_data:
        powers = [power for _, power in power_usage_data]
        min_power = min(powers)
        max_power = max(powers)
        avg_power = sum(powers) / len(powers)

        stdscr.addstr(y, 0, f"Lowest Energy Usage: {min_power:.2f} W")
        stdscr.addstr(y+1, 0, f"Highest Energy Usage: {max_power:.2f} W")
        stdscr.addstr(y+2, 0, f"Average Energy Usage: {avg_power:.2f} W")
        stdscr.refresh()

def get_device_info(stdscr):
    try:
        device_info = p110.getDeviceInfo()
        status = "On" if device_info['result']['device_on'] else "Off"
        stdscr.addstr(0, 0, f"Device Status: {status}")

        try:
            energy_usage = p110.getEnergyUsage()
            current_power_watts = energy_usage['result']['current_power'] / 1000
            stdscr.addstr(1, 0, f"Current Energy Usage: {current_power_watts:.2f} W")
            current_time = datetime.datetime.now()
            power_usage_data.append((current_time, current_power_watts))

            update_energy_statistics(stdscr)
        except KeyError as e:
            stdscr.addstr(4, 0, f"KeyError in energy usage data: {e}")
            stdscr.refresh()

    except KeyError as e:
        stdscr.addstr(4, 0, f"KeyError in device information: {e}")
        stdscr.refresh()

def main(stdscr):
    # Configure curses settings
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input

    while True:
        stdscr.clear()
        get_device_info(stdscr)
        time.sleep(1)

# Start curses application
curses.wrapper(main)
