# Quick Start Guide

Get SmartHomeHarmonizer running in 5 minutes!

## Step 1: Installation

```bash
pip install smarthomeharmonizer
```

## Step 2: Create Your First Device

Create a file called `my_smart_home.py`:

```python
from smarthomeharmonizer import create_app, DeviceManager
from smarthomeharmonizer.adapters.smart_light import SmartLightAdapter

# Create device manager
manager = DeviceManager()

# Add a smart light
light = SmartLightAdapter('living_room', 'Living Room Light')
manager.register_device(light)

# Create and configure the app
app = create_app(manager)

if __name__ == '__main__':
    print("SmartHomeHarmonizer is running!")
    print("Try: curl http://localhost:5000/api/v1/devices")
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Step 3: Run the Server

```bash
python my_smart_home.py
```

## Step 4: Control Your Devices

### List all devices:
```bash
curl http://localhost:5000/api/v1/devices
```

### Turn on the light:
```bash
curl -X POST http://localhost:5000/api/v1/devices/living_room/command \
  -H "Content-Type: application/json" \
  -d '{"command": "turnOn"}'
```

### Set brightness:
```bash
curl -X POST http://localhost:5000/api/v1/devices/living_room/command \
  -H "Content-Type: application/json" \
  -d '{"command": "setBrightness", "parameters": {"brightness": 50}}'
```

### Get device state:
```bash
curl http://localhost:5000/api/v1/devices/living_room/state
```

## Step 5: Add More Devices

```python
# Add multiple devices
bedroom_light = SmartLightAdapter('bedroom', 'Bedroom Light')
kitchen_light = SmartLightAdapter('kitchen', 'Kitchen Light')

manager.register_device(bedroom_light)
manager.register_device(kitchen_light)
```

## What's Next?

### Create Custom Devices

Learn how to create your own device adapters:

```python
from smarthomeharmonizer.adapters.base import DeviceAdapter

class MyCustomDevice(DeviceAdapter):
    def _initialize_state(self):
        return {'status': 'idle'}
    
    def get_supported_commands(self):
        return ['activate', 'deactivate']
    
    def execute_command(self, command, parameters=None):
        if command == 'activate':
            self._state['status'] = 'active'
        elif command == 'deactivate':
            self._state['status'] = 'idle'
        return self.get_state()
```

### Integrate with Voice Assistants

- [Alexa Integration Guide](alexa_integration.md)
- [Google Assistant Guide](google_integration.md)
- [HomeKit Integration](homekit_integration.md)

### Explore Advanced Features

- [Authentication & Security](security.md)
- [WebSocket Support](websockets.md)
- [State Persistence](persistence.md)
- [Automation Rules](automation.md)

## Troubleshooting

### Port Already in Use

If you get a "port already in use" error:

```python
app.run(host='0.0.0.0', port=8080)  # Use different port
```

### Device Not Responding

Check that:
1. Device ID is correct
2. Command is supported
3. Parameters are valid

### Can't Connect Remotely

Ensure firewall allows connections:
```bash
# Ubuntu/Debian
sudo ufw allow 5000

# Or run on all interfaces
app.run(host='0.0.0.0', port=5000)
```

## Example Projects

Check out these complete examples:

- [Smart Coffee Maker](examples/coffee_maker.md)
- [Multi-room Lighting](examples/lighting_system.md)
- [Temperature Control](examples/thermostat.md)
- [Security System](examples/security.md)

Ready to build something amazing? Let's go! 🚀
