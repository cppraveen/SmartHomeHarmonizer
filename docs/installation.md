# Installation Guide

This guide covers installing SmartHomeHarmonizer on various platforms.

## Requirements

- Python 3.8 or higher
- pip package manager
- (Optional) virtualenv for isolated environments

## Quick Install

The easiest way to install SmartHomeHarmonizer is via pip:

```bash
pip install smarthomeharmonizer
```

## Development Installation

For development or to get the latest features:

```bash
# Clone the repository
git clone https://github.com/yourusername/SmartHomeHarmonizer.git
cd SmartHomeHarmonizer

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Platform-Specific Instructions

### Raspberry Pi

SmartHomeHarmonizer is optimized for Raspberry Pi deployment:

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade

# Install Python and pip
sudo apt-get install python3 python3-pip

# Install SmartHomeHarmonizer
pip3 install smarthomeharmonizer

# For GPIO access (if needed)
pip3 install RPi.GPIO
```

### Docker

We provide Docker images for easy deployment:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m", "smarthomeharmonizer.cli", "run"]
```

Build and run:

```bash
docker build -t smarthomeharmonizer .
docker run -p 5000:5000 smarthomeharmonizer
```

### Ubuntu/Debian

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv ~/smarthomeharmonizer-env
source ~/smarthomeharmonizer-env/bin/activate

# Install
pip install smarthomeharmonizer
```

### macOS

```bash
# Using Homebrew
brew install python@3.10

# Install SmartHomeHarmonizer
pip3 install smarthomeharmonizer
```

### Windows

```powershell
# Install Python from python.org
# Then in PowerShell or Command Prompt:

pip install smarthomeharmonizer
```

## Verifying Installation

After installation, verify everything is working:

```bash
# Check version
python -c "import smarthomeharmonizer; print(smarthomeharmonizer.__version__)"

# Run tests (development installation)
pytest

# Start example server
python -m smarthomeharmonizer.examples.basic_usage
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'smarthomeharmonizer'**
   - Ensure you've activated your virtual environment
   - Check that installation completed successfully

2. **Permission denied errors**
   - Use `pip install --user smarthomeharmonizer` for user installation
   - Or use virtual environments (recommended)

3. **Version conflicts**
   - Create a fresh virtual environment
   - Update pip: `pip install --upgrade pip`

### Getting Help

If you encounter issues:

1. Check our [FAQ](faq.md)
2. Search [existing issues](https://github.com/yourusername/SmartHomeHarmonizer/issues)
3. Open a new issue with:
   - Python version (`python --version`)
   - pip version (`pip --version`)
   - Full error message
   - Steps to reproduce

## Next Steps

- Follow the [Quick Start Guide](quickstart.md)
- Learn about [Creating Device Adapters](adapters.md)
- Explore [Voice Assistant Integration](integration.md)
