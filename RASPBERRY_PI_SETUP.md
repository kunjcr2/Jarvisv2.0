# Setting up Jarvis v2.0 on Raspberry Pi 5

This guide will help you set up and run Jarvis v2.0 on your Raspberry Pi 5.

## Hardware Requirements

- Raspberry Pi 5 (any RAM configuration)
- Microphone (USB or 3.5mm jack)
- Speakers/Headphones
- SD Card (minimum 16GB recommended)
- Power supply (USB-C, 5V/5A recommended)

## Initial Setup

1. Start with a fresh installation of Raspberry Pi OS (64-bit)

   - Download the Raspberry Pi Imager from [raspberrypi.com/software](https://www.raspberrypi.com/software/)
   - Install the 64-bit version of Raspberry Pi OS

2. Update your system:

```bash
sudo apt update
sudo apt upgrade -y
```

## Installing Dependencies

1. Install system packages:

```bash
sudo apt install -y python3-pip
sudo apt install -y python3-venv
sudo apt install -y portaudio19-dev
sudo apt install -y python3-pyaudio
sudo apt install -y espeak
```

2. Set up a Python virtual environment:

```bash
python3 -m venv jarvis_env
source jarvis_env/bin/activate
```

3. Install the required Python packages:

```bash
pip3 install -r requirements.txt
```

## Additional Setup for Audio

1. Configure audio devices:

```bash
sudo raspi-config
```

- Navigate to System Options > Audio
- Select your preferred audio output device

2. Test your microphone:

```bash
arecord -l
arecord --duration=5 test.wav
aplay test.wav
```

## Environment Setup

1. Create a .env file in the project root:

```bash
touch .env
```

2. Add your API keys and configurations (use a text editor):

```
OPENAI_API_KEY=your_api_key_here
```

## Running Jarvis

1. Activate the virtual environment (if not already activated):

```bash
source jarvis_env/bin/activate
```

2. Run the program:

```bash
python3 driver.py
```

## Troubleshooting

### Common Issues:

1. Microphone not detected:

- Check if your microphone is properly connected
- Run `arecord -l` to list audio devices
- Ensure your user is in the `audio` group:

```bash
sudo usermod -a -G audio $USER
```

2. Audio output issues:

- Check volume levels using `alsamixer`
- Verify speaker/headphone connection
- Test with `speaker-test -c2`

3. Python package issues:

- Try reinstalling the problematic package
- Ensure you're using the virtual environment
- Check for Raspberry Pi specific versions of packages

### Performance Optimization

1. Increase swap space:

```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

2. Consider using a cooling solution for the Raspberry Pi 5

## Important Notes

- Keep your Raspberry Pi well-ventilated
- Use a reliable power supply to prevent undervoltage
- Regular system updates are recommended
- Backup your configuration files

## Support

If you encounter any issues:

1. Check the logs in the project directory
2. Verify all dependencies are correctly installed
3. Ensure all required API keys are properly set
4. Check system resource usage with `top` or `htop`
