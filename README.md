# Refactor/Rebase Efforts
A place for us to refactor for the code base and plan out its inner workings and how each function 
will work with each other (what data will be processed, the return values, documentation, variable naming, 
Level-2 Data flow diagram showing its inner workings, and a few other things). The sole reason we are 
performing this is to make the program more streamlined along with making it more understandable for people 
in the future when we inevitably pass it on.
<br><br>

## Files That Exceed Github's File Size Limits
**PDC files for the experiments:** [Here](https://drive.google.com/drive/folders/1ALwyBN3_T4iz4_cKKzfMz8ZIbbp9zOQS?usp=drive_link) <br>
![image](https://github.com/ISL-INTELLIGENT-SYSTEMS-LAB/objDetection-refactor/assets/78773029/71c605ee-40bf-44a8-a539-2a2cfa0f32f8) <br>
**Old Code Base:** [Here](https://drive.google.com/file/d/1MFZpc6wPdFgUKO2ngvbvKa_0UebA4hJU/view?usp=drive_link) <br>
![Screenshot 2024-04-12 155450](https://github.com/ISL-INTELLIGENT-SYSTEMS-LAB/objDetection-refactor/assets/78773029/c379147f-742a-458d-ac9a-d41efb75c852) <br>

## Referenced Repositories
[Hierarchical-Localization](https://github.com/cvg/Hierarchical-Localization)

## Authors
- [@Etoragon](https://github.com/Etoragon)
- [@TaylorBrown96](https://github.com/TaylorBrown96)
- [@oTinoSan](https://github.com/oTinoSan)
- [@MrBHerring](https://github.com/MrBHerring)
- [@TobyyW](https://github.com/TobyyW)
- [@xodezzio](https://github.com/xodezzio)

# Installation Guide

This guide provides detailed instructions for setting up the necessary environment and dependencies for your project on a Jetson device.

## Prerequisites

Ensure that your system has the following:
- A compatible Jetson device (e.g., Jetson Nano, TX2)
- Access to terminal with admin (sudo) permissions

## Setup Instructions

### Step 1: System Dependencies

To update your system and install necessary packages such as `nmap`, open a terminal and execute the following commands:

```bash
sudo apt-get update
sudo apt-get install -y nmap
```

### Step 2: Python Environment Setup

Activate your Python virtual environment and install the required Python packages using bash. Make sure to set parameter 'include-system-site-packages' to 'true'. 

```bash
cd ~/Environments

python3 -m venv collection_env

cd collection_env

nano pyvenv.cfg

include-system-site-packages = true    #make sure to safe the file

source /home/jetson/Environments/multirobot_env/bin/activate

pip install -r requirements.txt
```

### Step 3: ZED SDK Installation

To install the ZED SDK on your Jetson device, follow these steps:

1. **Download the SDK**:
   - Visit the [Stereolabs developers release page](https://www.stereolabs.com/developers/release).
   - Download the ZED SDK for JetPack 4.6.X (L4T 32.7) 4.1 suitable for Jetson Nano, TX2/TX2 NX, and CUDA 10.2. Ensure the file has a `.sh` extension.

2. **Prepare the Installation**:
   - Transfer the downloaded `.sh` file to your Jetson device, preferably in your project directory.

3. **Install the SDK**:
   - Navigate to the directory containing the downloaded file.
   - Make the installer executable and start the installation process by running:
   
   ```bash
   sudo chmod +x [Downloaded_SDK_file].sh
   ./[Downloaded_SDK_file].sh
   ```

   Replace `[Downloaded_SDK_file]` with the actual name of your downloaded file.

4. **Download the pyzed api
   -Navigate to directory of ZED SDK installation and run installation program:

    ```bash
    cd /usr/local/zed/
    python3 get_python_api.py

## Final Steps

After completing the above steps, ensure that all installations have completed successfully and that the environment variables (if any) are set correctly. Verify the operation of the ZED SDK and `nmap` by running a simple test command or script that uses these tools.
