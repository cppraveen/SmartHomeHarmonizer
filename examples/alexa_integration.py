"""Example Alexa Smart Home Skill integration."""

import json
from flask import request, jsonify
from smarthomeharmonizer import create_app, DeviceManager
from smarthomeharmonizer.adapters.smart_light import SmartLightAdapter
import logging

logger = logging.getLogger(__name__)


def create_alexa_app(device_manager: DeviceManager = None):
    """Create Flask app with Alexa endpoints."""
    app = create_app(device_manager)
    
    @app.route('/alexa/smart_home', methods=['POST'])
    def alexa_smart_home():
        """Handle Alexa Smart Home directives."""
        directive = request.json
        
        # Extract directive information
        header = directive.get('directive', {}).get('header', {})
        namespace = header.get('namespace')
        name = header.get('name')
        
        # Handle discovery
        if namespace == 'Alexa.Discovery' and name == 'Discover':
            return handle_discovery()
        
        # Handle control
        if namespace == 'Alexa.PowerController':
            return handle_power_control(directive)
        
        if namespace == 'Alexa.BrightnessController':
            return handle_brightness_control(directive)
        
        # Handle state reporting
        if namespace == 'Alexa' and name == 'ReportState':
            return handle_report_state(directive)
        
        # Unknown directive
        return create_error_response('INVALID_DIRECTIVE', 'Unknown directive')
    
    def handle_discovery():
        """Handle device discovery requests from Alexa."""
        devices = app.device_manager.list_devices()
        endpoints = []
        
        for device in devices:
            endpoint = {
                'endpointId': device['deviceId'],
                'friendlyName': device['name'],
                'description': f'SmartHomeHarmonizer {device["type"]}',
                'manufacturerName': 'SmartHomeHarmonizer',
                'displayCategories': ['LIGHT'],  # Adjust based on device type
                'capabilities': []
            }
            
            # Add capabilities based on supported commands
            if 'turnOn' in device['supportedCommands']:
                endpoint['capabilities'].append({
                    'type': 'AlexaInterface',
                    'interface': 'Alexa.PowerController',
                    'version': '3',
                    'properties': {
                        'supported': [{'name': 'powerState'}],
                        'proactivelyReported': True,
                        'retrievable': True
                    }
                })
            
            if 'setBrightness' in device['supportedCommands']:
                endpoint['capabilities'].append({
                    'type': 'AlexaInterface',
                    'interface': 'Alexa.BrightnessController',
                    'version': '3',
                    'properties': {
                        'supported': [{'name': 'brightness'}],
                        'proactivelyReported': True,
                        'retrievable': True
                    }
                })
            
            endpoints.append(endpoint)
        
        return jsonify({
            'event': {
                'header': {
                    'namespace': 'Alexa.Discovery',
                    'name': 'Discover.Response',
                    'payloadVersion': '3',
                    'messageId': generate_message_id()
                },
                'payload': {
                    'endpoints': endpoints
                }
            }
        })
    
    def handle_power_control(directive):
        """Handle power control directives."""
        endpoint_id = directive['directive']['endpoint']['endpointId']
        name = directive['directive']['header']['name']
        
        command = 'turnOn' if name == 'TurnOn' else 'turnOff'
        
        try:
            state = app.device_manager.execute_command(endpoint_id, command)
            
            return create_response(
                directive,
                'Alexa.PowerController',
                [
                    {
                        'namespace': 'Alexa.PowerController',
                        'name': 'powerState',
                        'value': state['powerState'],
                        'timeOfSample': get_utc_timestamp()
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Error handling power control: {e}")
            return create_error_response('ENDPOINT_UNREACHABLE', str(e))
    
    def handle_brightness_control(directive):
        """Handle brightness control directives."""
        endpoint_id = directive['directive']['endpoint']['endpointId']
        brightness = directive['directive']['payload']['brightness']
        
        try:
            state = app.device_manager.execute_command(
                endpoint_id, 
                'setBrightness',
                {'brightness': brightness}
            )
            
            return create_response(
                directive,
                'Alexa.BrightnessController',
                [
                    {
                        'namespace': 'Alexa.BrightnessController',
                        'name': 'brightness',
                        'value': state['brightness'],
                        'timeOfSample': get_utc_timestamp()
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Error handling brightness control: {e}")
            return create_error_response('ENDPOINT_UNREACHABLE', str(e))
    
    def handle_report_state(directive):
        """Handle state reporting requests."""
        endpoint_id = directive['directive']['endpoint']['endpointId']
        
        try:
            state = app.device_manager.get_device_state(endpoint_id)
            properties = []
            
            # Add power state
            if 'powerState' in state:
                properties.append({
                    'namespace': 'Alexa.PowerController',
                    'name': 'powerState',
                    'value': state['powerState'],
                    'timeOfSample': get_utc_timestamp()
                })
            
            # Add brightness
            if 'brightness' in state:
                properties.append({
                    'namespace': 'Alexa.BrightnessController',
                    'name': 'brightness',
                    'value': state['brightness'],
                    'timeOfSample': get_utc_timestamp()
                })
            
            return create_response(directive, 'Alexa', properties)
            
        except Exception as e:
            logger.error(f"Error reporting state: {e}")
            return create_error_response('ENDPOINT_UNREACHABLE', str(e))
    
    return app


def create_response(request_directive, namespace, properties):
    """Create Alexa response."""
    import uuid
    from datetime import datetime
    
    return jsonify({
        'event': {
            'header': {
                'namespace': namespace,
                'name': 'Response',
                'messageId': str(uuid.uuid4()),
                'correlationToken': request_directive['directive']['header'].get('correlationToken'),
                'payloadVersion': '3'
            },
            'endpoint': request_directive['directive']['endpoint'],
            'payload': {}
        },
        'context': {
            'properties': properties
        }
    })


def create_error_response(error_type, message):
    """Create Alexa error response."""
    import uuid
    
    return jsonify({
        'event': {
            'header': {
                'namespace': 'Alexa',
                'name': 'ErrorResponse',
                'messageId': str(uuid.uuid4()),
                'payloadVersion': '3'
            },
            'payload': {
                'type': error_type,
                'message': message
            }
        }
    })


def generate_message_id():
    """Generate unique message ID."""
    import uuid
    return str(uuid.uuid4())


def get_utc_timestamp():
    """Get current UTC timestamp in ISO format."""
    from datetime import datetime
    return datetime.utcnow().isoformat() + 'Z'


# Example usage
if __name__ == '__main__':
    # Create device manager
    manager = DeviceManager()
    
    # Register devices
    light1 = SmartLightAdapter('light1', 'Living Room Light')
    light2 = SmartLightAdapter('light2', 'Bedroom Light')
    
    manager.register_device(light1)
    manager.register_device(light2)
    
    # Create Alexa-enabled app
    app = create_alexa_app(manager)
    
    print("Alexa Smart Home Skill endpoint ready!")
    print("Configure your Alexa skill to use:")
    print("  https://your-domain.com/alexa/smart_home")
    print("\nNote: As an Amazon employee, ensure you have proper approvals")
    print("This is a personal project and not affiliated with Amazon.")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
