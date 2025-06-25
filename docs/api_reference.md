# API Reference

This document provides detailed information about the SmartHomeHarmonizer REST API endpoints.

## Base URL

All API endpoints are relative to the base URL where your SmartHomeHarmonizer server is running:

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. For production deployments, consider implementing proper authentication mechanisms.

## Response Format

All API responses follow a consistent JSON format:

### Success Response
```json
{
  "success": true,
  "data": {...}
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message"
}
```

## Endpoints

### Health Check

#### GET /health

Check if the server is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

**Status Codes:**
- `200 OK` - Server is healthy

---

### Device Management

#### GET /api/v1/devices

List all registered devices.

**Response:**
```json
{
  "success": true,
  "devices": [
    {
      "deviceId": "light1",
      "name": "Living Room Light",
      "type": "SmartLightAdapter",
      "supportedCommands": ["turnOn", "turnOff", "setBrightness", "setColor", "getStatus"],
      "state": {
        "powerState": "OFF",
        "brightness": 100,
        "color": {"r": 255, "g": 255, "b": 255}
      }
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved device list

---

#### GET /api/v1/devices/{device_id}

Get detailed information about a specific device.

**Parameters:**
- `device_id` (path) - Unique identifier of the device

**Response:**
```json
{
  "success": true,
  "deviceId": "light1",
  "name": "Living Room Light",
  "type": "SmartLightAdapter",
  "supportedCommands": ["turnOn", "turnOff", "setBrightness", "setColor", "getStatus"],
  "state": {
    "powerState": "OFF",
    "brightness": 100,
    "color": {"r": 255, "g": 255, "b": 255}
  }
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved device information
- `404 Not Found` - Device not found

---

#### GET /api/v1/devices/{device_id}/state

Get the current state of a specific device.

**Parameters:**
- `device_id` (path) - Unique identifier of the device

**Response:**
```json
{
  "success": true,
  "deviceId": "light1",
  "state": {
    "powerState": "OFF",
    "brightness": 100,
    "color": {"r": 255, "g": 255, "b": 255}
  }
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved device state
- `404 Not Found` - Device not found

---

#### POST /api/v1/devices/{device_id}/command

Execute a command on a specific device.

**Parameters:**
- `device_id` (path) - Unique identifier of the device

**Request Body:**
```json
{
  "command": "turnOn",
  "parameters": {
    "brightness": 75
  }
}
```

**Response:**
```json
{
  "success": true,
  "deviceId": "light1",
  "command": "turnOn",
  "state": {
    "powerState": "ON",
    "brightness": 75,
    "color": {"r": 255, "g": 255, "b": 255}
  }
}
```

**Status Codes:**
- `200 OK` - Command executed successfully
- `400 Bad Request` - Invalid command or parameters
- `404 Not Found` - Device not found

## Device Types and Commands

### Smart Light

**Supported Commands:**
- `turnOn` - Turn the light on
- `turnOff` - Turn the light off
- `setBrightness` - Set brightness level (0-100)
- `setColor` - Set RGB color values
- `getStatus` - Get current state

**Parameters:**
- `setBrightness`: `{"brightness": 75}`
- `setColor`: `{"color": {"r": 255, "g": 0, "b": 0}}`

### Thermostat

**Supported Commands:**
- `turnOn` - Turn the thermostat on
- `turnOff` - Turn the thermostat off
- `setTemperature` - Set target temperature (50-90°F)
- `setMode` - Set operation mode
- `getStatus` - Get current state

**Parameters:**
- `setTemperature`: `{"temperature": 72.0}`
- `setMode`: `{"mode": "heat"}` (heat, cool, auto, off)

### Coffee Maker

**Supported Commands:**
- `turnOn` - Turn the coffee maker on
- `turnOff` - Turn the coffee maker off
- `brew` - Start brewing coffee
- `setStrength` - Set brew strength
- `setSize` - Set brew size
- `clean` - Clean the coffee maker
- `getStatus` - Get current state

**Parameters:**
- `setStrength`: `{"strength": "strong"}` (light, medium, strong, extra_strong)
- `setSize`: `{"size": "large"}` (small, medium, large)

## Error Handling

### Common Error Codes

- `400 Bad Request` - Invalid request format or parameters
- `404 Not Found` - Device or resource not found
- `500 Internal Server Error` - Unexpected server error

### Error Response Format

```json
{
  "success": false,
  "error": "Detailed error message"
}
```

## Examples

### Turn on a light
```bash
curl -X POST http://localhost:5000/api/v1/devices/light1/command \
  -H "Content-Type: application/json" \
  -d '{"command": "turnOn"}'
```

### Set light brightness
```bash
curl -X POST http://localhost:5000/api/v1/devices/light1/command \
  -H "Content-Type: application/json" \
  -d '{"command": "setBrightness", "parameters": {"brightness": 50}}'
```

### Set thermostat temperature
```bash
curl -X POST http://localhost:5000/api/v1/devices/thermostat1/command \
  -H "Content-Type: application/json" \
  -d '{"command": "setTemperature", "parameters": {"temperature": 75.0}}'
```

### Brew coffee
```bash
curl -X POST http://localhost:5000/api/v1/devices/coffee1/command \
  -H "Content-Type: application/json" \
  -d '{"command": "brew"}'
```

## Rate Limiting

Currently, there are no rate limits implemented. For production deployments, consider implementing appropriate rate limiting to prevent abuse.

## Versioning

The API version is included in the URL path (`/api/v1/`). Future versions will maintain backward compatibility where possible, with breaking changes introduced in new version numbers.
