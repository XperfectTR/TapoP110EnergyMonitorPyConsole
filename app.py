import curses
from PyP100 import PyP110
import datetime
import time

# P110 object creation
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
        stdscr.addstr(4, 0, f"A KeyError occurred: {e}")
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
        time.sleep(5)  # update every 5 seconds

# Start curses application
curses.wrapper(main)
