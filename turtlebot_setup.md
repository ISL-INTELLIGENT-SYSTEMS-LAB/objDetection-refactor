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
# 4. Install numpy
The numpy installation is found on [jetson-nano-wheels'
python3.6-numpy-1.19.4, GitHub repo](https://github.com/jetson-nano-wheels/python3.6-numpy-1.19.4).

# 5. Install TurtleBot dependencies
Follow the video linked on the first page of the [TurtleBot3 Overview detailing how to setup the Jetson Nano for TurtleBot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/#notices).

