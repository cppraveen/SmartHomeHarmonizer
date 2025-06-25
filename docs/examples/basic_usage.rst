Basic Usage Example
==================

This example demonstrates the basic setup and usage of SmartHomeHarmonizer.

Installation
-----------

First, install SmartHomeHarmonizer:

.. code-block:: bash

   pip install smarthomeharmonizer

Simple Setup
-----------

Create a file called ``my_smart_home.py``:

.. literalinclude:: ../../examples/basic_usage.py
   :language: python
   :caption: Basic SmartHomeHarmonizer setup

Running the Example
------------------

Run the example:

.. code-block:: bash

   python my_smart_home.py

The server will start on ``http://localhost:5000``.

Testing the API
--------------

List all devices:

.. code-block:: bash

   curl http://localhost:5000/api/v1/devices

Turn on a light:

.. code-block:: bash

   curl -X POST http://localhost:5000/api/v1/devices/living_room_light/command \
     -H "Content-Type: application/json" \
     -d '{"command": "turnOn"}'

Set brightness:

.. code-block:: bash

   curl -X POST http://localhost:5000/api/v1/devices/living_room_light/command \
     -H "Content-Type: application/json" \
     -d '{"command": "setBrightness", "parameters": {"brightness": 75}}'

Get device state:

.. code-block:: bash

   curl http://localhost:5000/api/v1/devices/living_room_light/state

What's Next?
-----------

* See :doc:`../api_reference` for complete API documentation
* See :doc:`custom_adapter` for creating custom device adapters
* See :doc:`alexa_integration` for voice assistant integration 