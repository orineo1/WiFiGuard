# WiFi Guardian

WiFi Guardian is a Python script that acts as a watchdog for your TP-LINK router's WiFi network. It continuously checks the connection status and automatically restarts the router if any issues are detected.

## Features

- **Check WiFi Network:**
  - Utilizes the `netsh` command to identify the current Wi-Fi network name.
  - Verifies if the network matches the specified SSID.

- **TP-LINK Router Login:**
  - Uses Selenium with a headless Chrome browser to automate the login process to the TP-LINK router.
  - Enters the router's login page, inputs the provided password, and logs in.

- **Check Connection Status:**
  - Monitors the connection status using Selenium.
  - Checks if the router is connected to the internet.

- **Reboot Device:**
  - Initiates a router reboot if the connection status is not satisfactory.
  - Logs the time of the reboot action in 'reboot_log.txt'.

