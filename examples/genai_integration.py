"""Example GenAI integration for natural language device control."""

import json
from typing import Dict, Any, List, Optional
from flask import request, jsonify
from smarthomeharmonizer import create_app, DeviceManager
from smarthomeharmonizer.adapters.smart_light import SmartLightAdapter
from smarthomeharmonizer.adapters.base import DeviceAdapter
import re
import logging

logger = logging.getLogger(__name__)


class NaturalLanguageProcessor:
    """Process natural language commands for device control."""
    
    def __init__(self, device_manager: DeviceManager):
        self.device_manager = device_manager
        self.context = {}  # Store conversation context
        
        # Command patterns for natural language understanding
        self.patterns = {
            'turn_on': [
                r'turn on (?:the )?(.+)',
                r'switch on (?:the )?(.+)',
                r'activate (?:the )?(.+)',
                r'enable (?:the )?(.+)',
                r'(.+) on',
            ],
            'turn_off': [
                r'turn off (?:the )?(.+)',
                r'switch off (?:the )?(.+)',
                r'deactivate (?:the )?(.+)',
                r'disable (?:the )?(.+)',
                r'(.+) off',
            ],
            'brightness': [
                r'set (?:the )?(.+) (?:brightness )?to (\d+)%?',
                r'make (?:the )?(.+) (\w+)',
                r'dim (?:the )?(.+)',
                r'brighten (?:the )?(.+)',
            ],
            'query': [
                r'(?:what is|what\'s) (?:the )?status of (?:the )?(.+)',
                r'is (?:the )?(.+) on\??',
                r'how bright is (?:the )?(.+)',
                r'tell me about (?:the )?(.+)',
            ],
            'scene': [
                r'(?:set|create) (\w+) (?:scene|mood)',
                r'(?:i\'m|i am) (\w+)',
                r'time for (\w+)',
            ]
        }
        
        # Device name aliases for better natural language understanding
        self.aliases = {
            'living room': ['living room', 'lounge', 'main room'],
            'bedroom': ['bedroom', 'bed room', 'sleeping room'],
            'kitchen': ['kitchen', 'cooking area'],
            'all': ['all lights', 'everything', 'all devices', 'the lights'],
        }
        
        # Brightness descriptors
        self.brightness_map = {
            'bright': 100,
            'dim': 30,
            'dark': 10,
            'medium': 60,
            'half': 50,
            'full': 100,
        }
        
        # Scene definitions
        self.scenes = {
            'movie': {'brightness': 20, 'devices': ['living_room']},
            'reading': {'brightness': 80, 'devices': ['bedroom', 'living_room']},
            'cooking': {'brightness': 100, 'devices': ['kitchen']},
            'sleeping': {'brightness': 0, 'devices': 'all'},
            'working': {'brightness': 90, 'devices': ['office', 'desk']},
            'romantic': {'brightness': 30, 'devices': 'all'},
        }
    
    def process_command(self, text: str) -> Dict[str, Any]:
        """Process natural language command and return structured response."""
        text = text.lower().strip()
        
        # Check for scene commands first
        for pattern in self.patterns['scene']:
            match = re.match(pattern, text)
            if match:
                scene_name = match.group(1)
                return self._handle_scene(scene_name)
        
        # Check for query commands
        for pattern in self.patterns['query']:
            match = re.match(pattern, text)
            if match:
                device_ref = match.group(1)
                return self._handle_query(device_ref, text)
        
        # Check for turn on commands
        for pattern in self.patterns['turn_on']:
            match = re.match(pattern, text)
            if match:
                device_ref = match.group(1)
                return self._handle_turn_on(device_ref)
        
        # Check for turn off commands
        for pattern in self.patterns['turn_off']:
            match = re.match(pattern, text)
            if match:
                device_ref = match.group(1)
                return self._handle_turn_off(device_ref)
        
        # Check for brightness commands
        for pattern in self.patterns['brightness']:
            match = re.match(pattern, text)
            if match:
                if '%' in text or any(char.isdigit() for char in text):
                    device_ref = match.group(1)
                    brightness = int(re.findall(r'\d+', match.group(2))[0])
                    return self._handle_brightness(device_ref, brightness)
                else:
                    # Handle descriptive brightness
                    device_ref = match.group(1)
                    descriptor = match.group(2) if len(match.groups()) > 1 else None
                    return self._handle_descriptive_brightness(device_ref, descriptor, text)
        
        # If no pattern matches, try to understand intent
        return self._handle_unknown_command(text)
    
    def _find_devices(self, device_ref: str) -> List[str]:
        """Find device IDs matching the reference."""
        device_ref = device_ref.strip()
        devices = self.device_manager.list_devices()
        
        # Check if it's "all devices"
        if device_ref in ['all', 'everything', 'all lights', 'the lights']:
            return [d['deviceId'] for d in devices]
        
        # Direct device ID match
        device_ids = [d['deviceId'] for d in devices]
        if device_ref in device_ids:
            return [device_ref]
        
        # Check device names
        for device in devices:
            if device_ref in device['name'].lower():
                return [device['deviceId']]
        
        # Check aliases
        for device_id, aliases in self.aliases.items():
            if device_ref in aliases:
                # Find actual device IDs that match this alias
                matching = [d['deviceId'] for d in devices 
                           if device_id in d['deviceId'] or device_id in d['name'].lower()]
                if matching:
                    return matching
        
        return []
    
    def _handle_turn_on(self, device_ref: str) -> Dict[str, Any]:
        """Handle turn on commands."""
        device_ids = self._find_devices(device_ref)
        
        if not device_ids:
            return {
                'success': False,
                'message': f"I couldn't find any device matching '{device_ref}'",
                'suggestion': 'Try saying the device name differently or check what devices are available.'
            }
        
        results = []
        for device_id in device_ids:
            try:
                state = self.device_manager.execute_command(device_id, 'turnOn')
                results.append(f"{self._get_device_name(device_id)} is now on")
            except Exception as e:
                results.append(f"Couldn't turn on {self._get_device_name(device_id)}: {str(e)}")
        
        return {
            'success': True,
            'message': '. '.join(results),
            'devices_affected': device_ids
        }
    
    def _handle_turn_off(self, device_ref: str) -> Dict[str, Any]:
        """Handle turn off commands."""
        device_ids = self._find_devices(device_ref)
        
        if not device_ids:
            return {
                'success': False,
                'message': f"I couldn't find any device matching '{device_ref}'"
            }
        
        results = []
        for device_id in device_ids:
            try:
                state = self.device_manager.execute_command(device_id, 'turnOff')
                results.append(f"{self._get_device_name(device_id)} is now off")
            except Exception as e:
                results.append(f"Couldn't turn off {self._get_device_name(device_id)}: {str(e)}")
        
        return {
            'success': True,
            'message': '. '.join(results),
            'devices_affected': device_ids
        }
    
    def _handle_brightness(self, device_ref: str, brightness: int) -> Dict[str, Any]:
        """Handle brightness commands with numeric values."""
        device_ids = self._find_devices(device_ref)
        
        if not device_ids:
            return {
                'success': False,
                'message': f"I couldn't find any device matching '{device_ref}'"
            }
        
        results = []
        for device_id in device_ids:
            try:
                state = self.device_manager.execute_command(
                    device_id, 
                    'setBrightness',
                    {'brightness': brightness}
                )
                results.append(f"{self._get_device_name(device_id)} brightness set to {brightness}%")
            except Exception as e:
                results.append(f"Couldn't adjust {self._get_device_name(device_id)}: {str(e)}")
        
        return {
            'success': True,
            'message': '. '.join(results),
            'devices_affected': device_ids
        }
    
    def _handle_descriptive_brightness(self, device_ref: str, descriptor: str, text: str) -> Dict[str, Any]:
        """Handle brightness commands with descriptive terms."""
        # Check for dim/brighten commands
        if 'dim' in text:
            brightness = 30
        elif 'brighten' in text:
            brightness = 100
        elif descriptor and descriptor in self.brightness_map:
            brightness = self.brightness_map[descriptor]
        else:
            brightness = 50  # Default
        
        return self._handle_brightness(device_ref, brightness)
    
    def _handle_query(self, device_ref: str, text: str) -> Dict[str, Any]:
        """Handle status query commands."""
        device_ids = self._find_devices(device_ref)
        
        if not device_ids:
            return {
                'success': False,
                'message': f"I couldn't find any device matching '{device_ref}'"
            }
        
        results = []
        for device_id in device_ids:
            try:
                state = self.device_manager.get_device_state(device_id)
                device_name = self._get_device_name(device_id)
                
                # Format response based on query type
                if 'is' in text and 'on' in text:
                    is_on = state.get('powerState', 'OFF') == 'ON'
                    results.append(f"{device_name} is {'on' if is_on else 'off'}")
                elif 'bright' in text:
                    brightness = state.get('brightness', 0)
                    results.append(f"{device_name} is at {brightness}% brightness")
                else:
                    # General status
                    power = state.get('powerState', 'OFF')
                    brightness = state.get('brightness', 0)
                    results.append(f"{device_name} is {power.lower()} at {brightness}% brightness")
            except Exception as e:
                results.append(f"Couldn't get status for {device_name}: {str(e)}")
        
        return {
            'success': True,
            'message': '. '.join(results),
            'devices_queried': device_ids
        }
    
    def _handle_scene(self, scene_name: str) -> Dict[str, Any]:
        """Handle scene commands."""
        if scene_name not in self.scenes:
            return {
                'success': False,
                'message': f"I don't know the '{scene_name}' scene",
                'available_scenes': list(self.scenes.keys())
            }
        
        scene = self.scenes[scene_name]
        affected_devices = []
        
        # Get devices for this scene
        if scene['devices'] == 'all':
            devices = self.device_manager.list_devices()
            device_ids = [d['deviceId'] for d in devices]
        else:
            device_ids = []
            for device_ref in scene['devices']:
                device_ids.extend(self._find_devices(device_ref))
        
        # Apply scene settings
        for device_id in device_ids:
            try:
                if scene['brightness'] == 0:
                    self.device_manager.execute_command(device_id, 'turnOff')
                else:
                    self.device_manager.execute_command(device_id, 'turnOn')
                    self.device_manager.execute_command(
                        device_id, 
                        'setBrightness',
                        {'brightness': scene['brightness']}
                    )
                affected_devices.append(device_id)
            except Exception as e:
                logger.error(f"Error setting scene for {device_id}: {e}")
        
        return {
            'success': True,
            'message': f"Set {scene_name} scene",
            'devices_affected': affected_devices,
            'scene_settings': scene
        }
    
    def _handle_unknown_command(self, text: str) -> Dict[str, Any]:
        """Handle commands that don't match any pattern."""
        # Try to be helpful
        suggestions = []
        
        if any(word in text for word in ['light', 'lamp', 'bulb']):
            suggestions.append("Try 'turn on the living room light' or 'dim the bedroom light'")
        
        if any(word in text for word in ['status', 'state', 'check']):
            suggestions.append("Try 'what's the status of the kitchen light?'")
        
        if any(word in text for word in ['scene', 'mood', 'mode']):
            suggestions.append(f"Available scenes: {', '.join(self.scenes.keys())}")
        
        return {
            'success': False,
            'message': "I didn't understand that command",
            'suggestions': suggestions if suggestions else [
                "Try commands like 'turn on the lights', 'dim the bedroom light', or 'set movie scene'"
            ],
            'original_text': text
        }
    
    def _get_device_name(self, device_id: str) -> str:
        """Get friendly name for device."""
        devices = self.device_manager.list_devices()
        for device in devices:
            if device['deviceId'] == device_id:
                return device['name']
        return device_id


def create_genai_app(device_manager: DeviceManager = None):
    """Create Flask app with GenAI natural language endpoints."""
    app = create_app(device_manager)
    nlp = NaturalLanguageProcessor(app.device_manager)
    
    @app.route('/api/v1/genai/command', methods=['POST'])
    def genai_command():
        """Process natural language command."""
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing text in request'
            }), 400
        
        # Process the natural language command
        result = nlp.process_command(data['text'])
        
        # Add conversation context if provided
        if 'context' in data:
            nlp.context.update(data['context'])
        
        return jsonify(result)
    
    @app.route('/api/v1/genai/chat', methods=['POST'])
    def genai_chat():
        """Handle conversational interaction."""
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing messages in request'
            }), 400
        
        messages = data['messages']
        last_message = messages[-1]['content'] if messages else ''
        
        # Process the last message
        result = nlp.process_command(last_message)
        
        # Add conversational response
        response = {
            'success': result['success'],
            'message': result['message'],
            'context': nlp.context,
            'conversation_id': data.get('conversation_id', 'default')
        }
        
        return jsonify(response)
    
    @app.route('/api/v1/genai/capabilities', methods=['GET'])
    def genai_capabilities():
        """Return GenAI capabilities and available commands."""
        devices = app.device_manager.list_devices()
        
        capabilities = {
            'natural_language': True,
            'conversation_context': True,
            'available_devices': [
                {
                    'id': d['deviceId'],
                    'name': d['name'],
                    'type': d['type'],
                    'commands': d['supportedCommands']
                }
                for d in devices
            ],
            'available_scenes': list(nlp.scenes.keys()),
            'example_commands': [
                "Turn on all lights",
                "Dim the bedroom light",
                "Set movie scene",
                "What's the status of the living room?",
                "Make the kitchen bright",
                "I'm going to sleep",
                "Turn off everything"
            ]
        }
        
        return jsonify(capabilities)
    
    return app


# Example usage
if __name__ == '__main__':
    # Create device manager and register devices
    manager = DeviceManager()
    light = SmartLightAdapter('light1', 'Living Room Light')
    manager.register_device(light)
    
    # Create and run Flask app
    app = create_app(manager)
    app.run(host='0.0.0.0', port=5000)