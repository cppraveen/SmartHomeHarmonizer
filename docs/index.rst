SmartHomeHarmonizer Documentation
================================

Welcome to SmartHomeHarmonizer, a lightweight Python framework for bridging IoT devices with voice assistants.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api_reference
   examples/index

Overview
--------

SmartHomeHarmonizer provides a unified interface for integrating custom IoT devices with popular voice assistants including Amazon Alexa, Google Assistant, and Apple HomeKit. By abstracting the complexity of each platform's APIs and protocols, it enables developers to focus on device functionality rather than platform-specific implementations.

Key Features
-----------

* **Unified API**: Single RESTful interface for all voice assistant platforms
* **Modular Architecture**: Easy-to-implement device adapters
* **Lightweight**: Minimal resource footprint suitable for Raspberry Pi
* **Thread-Safe**: Concurrent device access with proper synchronization
* **Extensible**: Plugin architecture for new devices and platforms
* **Well-Tested**: Comprehensive test suite with >90% coverage
* **PyPI Available**: Easy installation via ``pip install smarthomeharmonizer``

Quick Start
----------

Install SmartHomeHarmonizer:

.. code-block:: bash

   pip install smarthomeharmonizer

Create a simple device:

.. code-block:: python

   from smarthomeharmonizer import create_app, DeviceManager
   from smarthomeharmonizer.adapters.smart_light import SmartLightAdapter

   manager = DeviceManager()
   light = SmartLightAdapter('light1', 'Living Room Light')
   manager.register_device(light)
   
   app = create_app(manager)
   app.run()

Control with HTTP:

.. code-block:: bash

   curl -X POST http://localhost:5000/api/v1/devices/light1/command \
     -H "Content-Type: application/json" \
     -d '{"command": "turnOn"}'

For more information, see the :doc:`quickstart` guide.

Installation
-----------

See the :doc:`installation` guide for detailed installation instructions.

API Reference
------------

See the :doc:`api_reference` for complete API documentation.

Examples
--------

See the :doc:`examples/index` for example projects and use cases.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 