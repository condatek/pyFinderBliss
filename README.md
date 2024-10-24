# pyFinderBliss

`pyFinderBliss` is a Python API designed for interacting with FINDER BLISS thermostats. This library allows users to retrieve data such as temperature, humidity, and mode from BLISS1 and BLISS2 devices. It can be used for integration with platforms like Home Assistant. 

**Note:** This python package is unofficial and is not related in any way to Finder. It was developed by reverse-engineering the requests made by the official app, and the API may stop working at any time if the provider makes changes.

## Features

- Retrieve temperature and humidity data from BLISS1 and BLISS2 thermostats.
- Monitor device status, battery level, and Wi-Fi signal strength.
- Currently, only data retrieval is supported. Writing parameters to the thermostats will be added in future releases.

## Installation

Install the library via pip:

```bash
pip install pyFinderBliss
```

## Usage Example
Here is a basic example showing how to retrieve temperature data from your BLISS devices using the pyFinderBliss API:
```python
import asyncio
from pyfinderbliss.api import get_finder_devices

USER = "your_username"
PASSWORD = "your_password"

async def fetch_devices():
    devices = await get_finder_devices(USER, PASSWORD)
    
    for device in devices:
        if device.get('model') in ['BLISS1', 'BLISS2']:
            name = device.get('name')
            temperature = device.get('temperature')
            print(f"Device: {name}, Temperature: {temperature}°C")

asyncio.run(fetch_devices())
```

## Home Assistant Integration
An official Home Assistant integration based on this library, called finderBliss, is currently under development. Stay tuned for updates!

## Contributing
Contributions to this project are welcome! If you'd like to help develop features such as thermostat control, or improve functionality, please fork the repository and create a pull request.

## TODOs for Future Versions
Implement support for controlling thermostat settings (e.g., set temperature, switch modes).
Improve error handling and extend test coverage.
Optimize the WebSocket connection for real-time updates.