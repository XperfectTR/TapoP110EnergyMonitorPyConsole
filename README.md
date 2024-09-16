<img src="image.jpg" alt="Project Image" style="width:25%;">

<h1>Smart Plug Energy Monitoring Tool</h1>

<p>This Python script enables real-time monitoring of energy usage through a TP-Link Smart Plug (model P110). Utilizing the <code>PyP100</code> library, it communicates with the smart plug to fetch and display device status and energy consumption metrics. The script showcases the current power usage in watts, alongside the minimum, maximum, and average energy consumption recorded during the session.</p>

<h2>Features</h2>
<ul>
  <li><strong>Device Status Display</strong>: Shows whether the smart plug is currently ON or OFF.</li>
  <li><strong>Real-time Energy Usage</strong>: Monitors and displays the current energy consumption in watts.</li>
  <li><strong>Energy Usage Statistics</strong>: Calculates and displays statistics including the lowest, highest, and average power usage.</li>
</ul>

<h2>How It Works</h2>
<p>The script operates by creating an instance of the <code>PyP110.P110</code> class using the smart plug's IP address, and user credentials (email and password). It then performs a handshake and logs in to the device. Once authenticated, it periodically fetches and updates the device's status and energy usage data, displaying these details in a curses-based terminal interface.</p>

<h2>Setup and Configuration</h2>
<ol>
  <li><strong>Dependencies</strong>: Ensure you have Python 3.x installed along with the <code>PyP100</code> library and <code>curses</code> (pre-installed with Python on Linux/MacOS, for Windows use <code>windows-curses</code>).</li>
  <li><strong>Smart Plug Setup</strong>: Assign a static IP address to your TP-Link Smart Plug through your router settings to ensure consistent connectivity.</li>
  <li><strong>Script Configuration</strong>: Replace <code>"IP"</code>, <code>"email@gmail.com"</code>, and <code>"password"</code> in the script with your smart plug's IP address and your TP-Link account credentials.</li>
</ol>

<h2>Customization</h2>
<ul>
  <li><strong>Refresh Rate</strong>: Modify the sleep duration in the main loop (<code>time.sleep(1)</code>) to adjust the data refresh rate.</li>
  <li><strong>Display Layout</strong>: Adjust the <code>y</code> parameter in <code>update_energy_statistics</code> and coordinate values in <code>stdscr.addstr</code> calls to customize the display layout.</li>
  <li><strong>Additional Metrics</strong>: Extend the script by incorporating more data points available from the <code>PyP100</code> library, such as daily or monthly usage.</li>
</ul>

<h2>Installation Troubleshooting</h2>
<p>If you encounter an <code>error: externally-managed-environment</code> when attempting to install the package using pip, your Python environment is likely managed by your operating system. This is common in systems like Debian or Ubuntu where Python packages are managed system-wide.</p>

<p>To safely install the <code>TapoP100</code> library, you should use a virtual environment. This approach prevents conflicts with system-managed packages and ensures that your system remains stable. Here are the steps to follow:</p>

<ol>
  <li>First, ensure that you have the necessary tools by installing <code>python3-venv</code> and <code>pipx</code> if not already installed:
    <pre><code>sudo apt install python3-venv pipx</code></pre>
  </li>
  <li>Create a virtual environment:
    <pre><code>python3 -m venv ~/myvenv</code></pre>
  </li>
  <li>Activate the virtual environment:
    <pre><code>source ~/myvenv/bin/activate</code></pre>
  </li>
  <li>Now, try installing the package again within this virtual environment:
    <pre><code>pip install git+https://github.com/XperfectTR/TapoP100.git@main</code></pre>
  </li>
</ol>

<p>If you prefer to override this protection and install the package system-wide, you can do so at your own risk by using the <code>--break-system-packages</code> option:
  <pre><code>pip install git+https://github.com/XperfectTR/TapoP100.git@main --break-system-packages</code></pre>
</p>

<p><strong>Note:</strong> Overriding system package management is not recommended as it may lead to system instability or conflicts with other Python packages managed by your OS.</p>

<h2>More Information</h2>
<p>For more detailed information about managing Python environments and packages, see the official Python documentation on virtual environments and pip:</p>
<ul>
  <li><a href="https://docs.python.org/3/tutorial/venv.html">Python Virtual Environments: A Primer</a></li>
  <li><a href="https://pip.pypa.io/en/stable/">pip documentation</a></li>
</ul>


<h2>Contributions</h2>
<p>Contributions are welcome! Feel free to fork this project and submit pull requests with improvements, bug fixes, or additional features.</p>

<h2>Disclaimer</h2>
<p>This script is for educational and personal use. It is not officially affiliated with or endorsed by TP-Link. Use it at your own risk.</p>

<h2>License</h2>
<p>This project is open-sourced under the MIT license. See the LICENSE file for more details.</p>
