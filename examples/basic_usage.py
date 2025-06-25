"""Basic usage example for SmartHomeHarmonizer."""

from smarthomeharmonizer import create_app, DeviceManager
from smarthomeharmonizer.adapters.smart_light import SmartLightAdapter

def main():
    """Run a basic SmartHomeHarmonizer server."""
    # Create device manager
    manager = DeviceManager()
    
    # Register devices
    living_room_light = SmartLightAdapter('living_room_light', 'Living Room Light')
    bedroom_light = SmartLightAdapter('bedroom_light', 'Bedroom Light')
    
    manager.register_device(living_room_light)
    manager.register_device(bedroom_light)
    
    # Create Flask application
    app = create_app(manager)
    
    print("SmartHomeHarmonizer is running!")
    print("Available devices:")
    for device in manager.list_devices():
        print(f"  - {device['name']} (ID: {device['deviceId']})")
    
    print("\nAPI Endpoints:")
    print("  GET  /api/v1/devices                      - List all devices")
    print("  GET  /api/v1/devices/<device_id>          - Get device info")
    print("  GET  /api/v1/devices/<device_id>/state    - Get device state")
    print("  POST /api/v1/devices/<device_id>/command  - Execute command")
    
    # Run the server
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
