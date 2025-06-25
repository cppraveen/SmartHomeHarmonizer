# SmartHomeHarmonizer Documentation

Welcome to SmartHomeHarmonizer, a lightweight Python framework for bridging IoT devices with voice assistants.

## Overview

SmartHomeHarmonizer provides a unified interface for integrating custom IoT devices with popular voice assistants including Amazon Alexa, Google Assistant, and Apple HomeKit. By abstracting the complexity of each platform's APIs and protocols, it enables developers to focus on device functionality rather than platform-specific implementations.

## Key Features

- **Unified API**: Single RESTful interface for all voice assistant platforms
- **Modular Architecture**: Easy-to-implement device adapters
- **Lightweight**: Minimal resource footprint suitable for Raspberry Pi
- **Thread-Safe**: Concurrent device access with proper synchronization
- **Extensible**: Plugin architecture for new devices and platforms
- **Well-Tested**: Comprehensive test suite with >90% coverage

## Quick Links

- [Installation Guide](installation.md)
- [Quick Start Tutorial](quickstart.md)
- [API Reference](api_reference.md)
- [Creating Device Adapters](adapters.md)
- [Voice Assistant Integration](integration.md)
- [Examples](examples.md)

## Why SmartHomeHarmonizer?

Unlike comprehensive home automation platforms that try to do everything, SmartHomeHarmonizer focuses on one thing: making it easy to control your custom IoT devices with voice commands. This focused approach means:

- **Faster Development**: Get voice control working in minutes, not days
- **Lower Resource Usage**: Runs comfortably on a Raspberry Pi 3B+
- **Easier Debugging**: Simple, understandable codebase
- **Better Learning**: Perfect for understanding how voice assistants work

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Amazon Alexa   │     │ Google Assistant│     │  Apple HomeKit  │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  SmartHomeHarmonizer    │
                    │      RESTful API        │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┴──────────────────┐
              │          Device Manager             │
              └──────────────────┬──────────────────┘
                                 │
        ┌────────────┬───────────┴───────────┬────────────┐
        │            │                       │            │
   ┌────▼────┐  ┌────▼────┐            ┌────▼────┐  ┌────▼────┐
   │ Light   │  │ Coffee  │            │Thermo-  │  │ Custom  │
   │ Adapter │  │ Maker   │            │ stat    │  │ Device  │
   └─────────┘  └─────────┘            └─────────┘  └─────────┘
```

## Getting Started

1. **Install SmartHomeHarmonizer**:
   ```bash
   pip install smarthomeharmonizer
   ```

2. **Create a simple device**:
   ```python
   from smarthomeharmonizer import create_app, DeviceManager
   from smarthomeharmonizer.adapters.smart_light import SmartLightAdapter

   manager = DeviceManager()
   light = SmartLightAdapter('light1', 'Living Room Light')
   manager.register_device(light)
   
   app = create_app(manager)
   app.run()
   ```

3. **Control with HTTP**:
   ```bash
   curl -X POST http://localhost:5000/api/v1/devices/light1/command \
     -H "Content-Type: application/json" \
     -d '{"command": "turnOn"}'
   ```

## Community

- **GitHub**: [github.com/cppraveen/SmartHomeHarmonizer](https://github.com/cppraveen/SmartHomeHarmonizer)
- **Issues**: [Report bugs or request features](https://github.com/cppraveen/SmartHomeHarmonizer/issues)
- **Discussions**: [Join the conversation](https://github.com/cppraveen/SmartHomeHarmonizer/discussions)

## License

SmartHomeHarmonizer is released under the MIT License. See [LICENSE](https://github.com/yourusername/SmartHomeHarmonizer/blob/main/LICENSE) for details.
