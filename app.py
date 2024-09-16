import curses
from PyP100 import PyP110
import datetime
import time

# P110 object creation
p110 = PyP110.P110("192.168.3.113", "msvcr32@gmail.com", "mehmetAs1")
p110.handshake()
p110.login()

# List to store power usage data
power_usage_data = []

def update_energy_statistics(stdscr, y=4):
    if power_usage_data:
        powers = [power for _, power in power_usage_data]
        min_power = min(powers)
        max_power = max(powers)
        avg_power = sum(powers) / len(powers)

        stdscr.addstr(y, 0, f"Minimum Energy Usage: {min_power:.2f} W")
        stdscr.addstr(y+1, 0, f"Maximum Energy Usage: {max_power:.2f} W")
        stdscr.addstr(y+2, 0, f"Average Energy Usage: {avg_power:.2f} W")
        stdscr.refresh()

def get_device_info(stdscr):
    try:
        device_info = p110.getDeviceInfo()
        status = "On" if device_info['device_on'] else "Off"
        stdscr.addstr(0, 0, f"Device Status: {status}")

        energy_usage = p110.getEnergyUsage()
        current_power_watts = energy_usage['current_power'] / 1000
        stdscr.addstr(1, 0, f"Current Power Usage: {current_power_watts:.2f} W")
        current_time = datetime.datetime.now()
        power_usage_data.append((current_time, current_power_watts))

        update_energy_statistics(stdscr)
    except KeyError as e:
        stdscr.addstr(5, 0, f"A KeyError occurred: {e}")
        stdscr.refresh()

def toggle_device(stdscr):
    try:
        device_info = p110.getDeviceInfo()
        if device_info['device_on']:
            p110.turnOff()
            stdscr.addstr(3, 0, "Turning off the device...")
        else:
            p110.turnOn()
            stdscr.addstr(3, 0, "Turning on the device...")
        stdscr.refresh()
        time.sleep(1)
    except KeyError as e:
        stdscr.addstr(5, 0, f"A KeyError occurred while toggling: {e}")
        stdscr.refresh()

def main(stdscr):
    # curses settings
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(True)  # non-blocking input
    p110.handshake()
    p110.login()

    while True:
        stdscr.clear()
        get_device_info(stdscr)
        stdscr.addstr(2, 0, "Press Enter to toggle the device.")  # Added message
        key = stdscr.getch()

        # Toggle device on Enter key press
        if key == 10:  # Enter key ASCII code
            toggle_device(stdscr)

        time.sleep(0.1)  # update every 5 seconds

# Start curses application
curses.wrapper(main)
