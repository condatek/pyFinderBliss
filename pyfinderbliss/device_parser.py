import json

def parse_device_data(payload):
    try:
        data = json.loads(payload)
        devices = data.get('devices', [])
        return [parse_device(device) for device in devices]
    except json.JSONDecodeError:
        return []

def determine_bliss1_mode(settings):
    is_on = settings.get('manualSchedule', {}).get('isOn', False)
    mode = settings.get('mode', 'OFF').upper()

    if mode == 'AUTO':
        return 'auto'
    elif mode == 'OFF' and is_on:
        return 'manual'
    elif mode == 'OFF' and not is_on:
        return 'off'
    return 'unknown'

def determine_bliss2_mode(measures):
    mode = measures.get('mode', 0)
    return {0: 'off', 1: 'auto', 3: 'manual'}.get(mode, 'unknown')

def parse_device(device):
    tag = device.get('tag')
    if tag in ['BLISS1', 'BLISS2']:
        name = device.get('name', 'Unknown')
        serial_number = device.get('serialNumber', 'Unknown')
        model = device.get('tag', 'Unknown')

        # Parsing measures
        measures_str = device.get('measures')
        measures = safe_json_load(measures_str)

        # Parsing settings
        settings_str = device.get('settings')
        settings = safe_json_load(settings_str)

        # Determine the mode
        mode = determine_bliss2_mode(measures) if 'BLISS2' in tag else determine_bliss1_mode(settings)
        status = measures.get('status', 'N/A')
        humidity = measures.get('humidity', 'N/A')
        set_point = measures.get('setPoint', {}).get('value', 'N/A')
        wifi_level = measures.get('wifiLevel', 'N/A')
        battery_level = measures.get('batteryLevel', 'N/A')

        # Temperature handling
        temperature_value = parse_temperature(measures.get('temperature'))

        # Additional BLISS2-specific settings
        if 'BLISS2' in tag:
            primary_settings = settings.get('primary', {})
            mode_setting = primary_settings.get('mode', 'N/A')
            manual_set_point_value = parse_set_point(primary_settings.get('manualSetPoint', {}))
        elif 'BLISS1' in tag:
            mode_setting = settings.get('mode', 'N/A')
            manual_set_point_value = parse_set_point(settings.get('manualSchedule', {}).get('setPoint'))

        return {
            "name": name,
            "serial_number": serial_number,
            "model": model,
            "mode": mode,
            "status": status,
            "set_point_value": set_point,
            "wifi_level": wifi_level,
            "temperature": temperature_value,
            "humidity": humidity,
            "battery_level": battery_level,
            "mode_setting": mode_setting,
            "manual_set_point": manual_set_point_value
        }
    return {}

def safe_json_load(data):
    """Safely loads JSON strings, returns an empty dict on failure."""
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {}
    elif isinstance(data, dict):
        return data
    return {}

def parse_temperature(temp_data):
    """Parse and normalize temperature data."""
    if isinstance(temp_data, dict):
        value = temp_data.get('value', 'N/A')
        if isinstance(value, (int, float)):
            return value / 10  # Convert to Celsius
    elif isinstance(temp_data, (int, float)):
        return temp_data / 10  # Convert to Celsius
    return 'N/A'

def parse_set_point(set_point_data):
    """Parse and normalize set point values."""
    if isinstance(set_point_data, dict):
        value = set_point_data.get('value', 'N/A')
        if isinstance(value, (int, float)):
            return value / 10  # Convert to Celsius
    elif isinstance(set_point_data, (int, float)):
        return set_point_data / 10  # Convert to Celsius
    return 'N/A'
