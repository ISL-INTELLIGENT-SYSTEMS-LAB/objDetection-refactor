# 1. Flash OS image to the Jetson Nano computer
The instructions for this step are found on the [QEngineering Jetson Nano Github](https://github.com/Qengineering/Jetson-Nano-image?tab=readme-ov-file). Please follow the README instructions.

This image will install a version of Jetpack that has ML and AI dependencies, libraries and packages. Please follow hostname and username naming conventions, ex: jetson@nano45. The two digits that end the hostname will be the two digit ip address that you will set as the static ip for the turtebot. As in the other turtlebots, if you are setting a new IP address use increments of 5, ex: nano45, nano50, nano55, etc. To change the hostname, in terminal run:

```bash
sudo hostnamectl set-hostname <newhostname>
# exit current terminal an start new terminal
hostname    #this command will display new hostname
```

# 2. Setup static IP and SSH
For this step, follow the steps below. This will set up a manual static IPv4 address on the lab network. You will be using the network NETGEAR43 and the current password is fuzzyspider423.

In Settings > Network > Wireless, select NETGEAR43, connect, then '>'. Go to 'Settings...' > IPv4 Settings. Select Manual from the dropdown. Add a static address. Address: 192.168.0.<__>, Netmask: 24, Gateway: 192.168.0.1. 

Once this is setup, attempt to ping the ip address from another computer on the same network. Once pinged, attempt to ssh into the device. If you encounter an error in your ssh attempt that states "REMOTE HOST IDENTIFICATION HAS CHANGED", run the command listed below to clear the ssh history. If successful, run jtop in ssh terminal. This will display the system info under the INFO tab. Quit.

```bash
ping 192.168.0.45
ssh jetson@nano45
ssh-keygen -R "192.168.0.45"   #if ssh error
jtop   #if successful ssh
```

# 3. Add SSH key to GitHub
These steps to [generate a new SSH key are found here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and the steps to [add the SSH key to GitHub are found here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account). The terminal steps are condensed below. Make sure to generate a new key and add it to GitHub. Leave the password empty.

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub    #copy output
```

# 4. Create environment and install dependencies
Always work within an environment on the TurtleBots. The goal is to have the turtlebots be completely stable outside of environments. The steps covered here are similar but not identical to the steps in the README.md for [ISL repo OBJDETECTION-REFACTOR](https://github.com/ISL-INTELLIGENT-SYSTEMS-LAB/objDetection-refactor). 

## 1. System Dependencies

To update your system and install necessary packages such as `venv` and `nmap`, open a terminal and execute the following commands:

```bash
sudo apt-get update
sudo apt-get install python3-venv
sudo apt-get install -y nmap
sudo apt install zstd
```

## 2. Python Environment Setup

Always create environments in the Environments directory at home. If there is not an Environments directory, create one. Create and activate your Python virtual environment. Install the required Python packages using bash. Make sure to set parameter 'include-system-site-packages' to 'true', if you would like to system dependencies in your new environment. Below is an example of an environment creation for `collection_env`.

```bash
mkdir ~/Environments
cd ~/Environments
python3 -m venv collection_env
cd collection_env
nano pyvenv.cfg    #optional
include-system-site-packages = true    #make sure to safe the file
source ~/Environments/collection_env/bin/activate
```

## 3. Install numpy
Our `numpy` is currently downloaded from this [Jetson-Nano repo](https://github.com/jetson-nano-wheels/python3.6-numpy-1.19.4#readme).

```bash
pip install 'https://github.com/jetson-nano-wheels/python3.6-numpy-1.19.4/releases/download/v0.0.2/numpy-1.19.4-cp36-cp36m-linux_aarch64.whl'
```

## 4. ZED SDK Installation

To install the ZED SDK on your Jetson device, follow these steps:

1. **Download the SDK**:
   - Visit the [Stereolabs developers release page](https://www.stereolabs.com/developers/release).
   - Download the ZED SDK for JetPack 4.6.X (L4T 32.7) 4.1 suitable for Jetson Nano, TX2/TX2 NX, and CUDA 10.2. Ensure the file has a `.sh` extension.

2. **Prepare the Installation**:
   - Transfer the downloaded `.sh` file to your Jetson device.

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
    ```
# 5. Install requirements for project
Enter environment. Navigate to project directory and run requirements.txt.
```bash
pip install -r requirements_client.txt
```

# 6. Install TurtleBot dependencies
Follow the video linked on the first page of the [TurtleBot3 Overview detailing how to setup the Jetson Nano for TurtleBot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/#notices).

