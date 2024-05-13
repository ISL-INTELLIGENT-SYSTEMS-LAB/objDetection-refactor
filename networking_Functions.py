import cv2
import datetime
import ipaddress
import math
import nmap
import numpy as np
import os
import pandas as pd
import pickle
import pytz
import pyzed.sl as sl
import socket
import sys
import threading
import time
import traceback
from io import StringIO
import netifaces as ni

##########################
#### Sever Functions #####
##########################

# Function to get the local IP address of the server
def get_server_ip():
    """
    Retrieves the local IP address of the machine running the script on the '192.168.0.0/24' network.

    Returns:
    str: The local IP address of the machine on the specific network.
    """
    # Loop through the network interfaces
    for interface in netifaces.interfaces():
        try:
            ip_info = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
            ip_address = ip_info['addr']
            netmask = ip_info['netmask']

            # Check if the IP address is in the range of the desired network
            if ipaddress.IPv4Address(ip_address) in ipaddress.IPv4Network('192.168.0.0/24'):
                return ip_address
        except KeyError:
            continue

    return None

# Function to handle a client connection
def handle_client(client_socket, client_address):
    """
    Handles a client connection by receiving data from the client and processing it.
    
    Parameters:
    client_socket (socket.socket): The socket object associated with the client. This is used to receive data from the client.
    client_address (tuple): The address of the client. This is a tuple containing the client's IP address and port number.

    Returns: None

    The function first initializes two variables: 'data_bytes' to store the received data and 'total_received' to keep track of the total amount of data received.
    It then enters a loop where it continuously receives data from the client in chunks of 1024 bytes using the 'recv' method of the client socket.
    If no data is received (i.e., 'recv' returns an empty byte string), the function breaks the loop.
    Otherwise, it adds the received data to 'data_bytes' and the length of the received data to 'total_received'.
    After all the data is received, the function calls the 'process_data' function, passing it 'data_bytes', 'client_address', and 'total_received'.
    Finally, the function closes the client socket using its 'close' method.
    """
    # Initialize the data bytes and total received
    data_bytes = b''
    total_received = 0
    # Loop until no more data is received from the client
    while True:
        # Receive data from the client
        packet = client_socket.recv(1024)
        # If no data was received, break the loop
        if not packet: 
            break
        # Add the received data to the data bytes
        data_bytes += packet
        # Add the length of the received data to the total
        total_received += len(packet)
    # Process the received data
    process_data(data_bytes, client_address, total_received)
    # Close the client socket
    client_socket.close()

# Function to start the server
def start_server():
    """
    Starts the server, listens for client connections, and starts a new thread for each client that connects.

    Parameters: None

    Returns: None

    The function first creates a server socket using the 'socket.socket' function.
    It then binds the server socket to the server address using the 'bind' method of the server socket. The server address is defined.
    The server socket starts listening for client connections with a backlog of 5 using the 'listen' method.
    A message indicating that the server is listening is printed to the console.
    The function then enters an infinite loop where it continuously accepts client connections using the 'accept' method of the server socket.
    When a client connects, the 'accept' method returns a new socket object and the address of the client.
    A message indicating that a client has connected is printed to the console, and a message is sent to the client using the 'send' method of the client socket.
    A new thread is then started to handle the client connection. The 'threading.Thread' function is used to create the new thread, 
    with the 'target' parameter set to the 'handle_client' function and the 'args' parameter set to a tuple containing the client socket and address.
    The 'start' method of the thread object is called to start the thread.
    """
    # Get the server IP address
    ip_address = get_server_ip()
    # Assign the port number
    port = 16666
    # Define the server address
    server_address = (ip_address, port) # change to correct server IPv4 address
    # Create a server socket
    server_socket = socket.socket()
    # Bind the server socket to the server address
    server_socket.bind(server_address) 
    # Start listening for client connections
    server_socket.listen(5)
    # Print the server IP address and port number
    print(f'\nServer IP: {ip_address}, Port assignment: {port}')
    # Print the path to the collection directory
    collection_dir_path = create_collection_dir()
    print(f"Collection will be stored in the '{collection_dir_path}' directory.")
    # Print a message indicating that the server is listening
    print(f'\n*** Server {server_address} is listening... ***\n')
    # Loop indefinitely
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        # Print a message indicating a client has connected
        print(f"Client {client_address} connected.")
        # Send a message to the client indicating it has connected to the server
        client_socket.send(f'\nConnected to server {server_address}.'.encode('ascii'))
        # Start a new thread to handle the client connection
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

##########################
#### Client Functions ####
##########################

def get_client_ip(network_interface='wlan0'):
    """
    Gets the client's IP address.

    Parameters:
    network_interface (str): The name of the network interface to check (default is 'wlan0').

    Returns:
    str: The client's IP address, or None if the interface does not have an IPv4 address.
    """
    try:
        # Get the IP address of the network interface
        ip_address = ni.ifaddresses(network_interface)[ni.AF_INET][0]['addr']
        two_digit_ip = ip_address.split('.')[-1]
        return ip_address, two_digit_ip
    
    except ValueError:
        print(f"No IP address found for interface {network_interface}")
        return None

# Function to get the network CIDR for a specific network interface
def get_network_cidr(interface_name='wlan0'):
    """
    Returns the network in CIDR notation for a specific network interface.
    
    Parameters:
    interface_name (str): The name of the network interface to check (default is 'wlan0').
    """
    # Get the network addresses for the specified interface
    addresses = ni.ifaddresses(interface_name)
    # If the interface has an IPv4 address
    if ni.AF_INET in addresses:
        # Get the IPv4 address
        for link in addresses[ni.AF_INET]:
            # Get the IP address and netmask
            ip = link['addr']
            netmask = link['netmask']
            # Calculate the network CIDR
            network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
            return str(network)

    return None

def get_server_address(client_ip):
    """
    Retrieves the IP addresses of all devices in the same network using nmap and prompts the user to choose one.

    Parameters:
    network (str): The network in CIDR notation.

    Returns:
    str: The chosen IP address.
    """
    while True:
        network = get_network_cidr(interface_name='wlan0')
        nm = nmap.PortScanner()
        nm.scan(hosts=network, arguments='-sn')
        ips = [host for host in nm.all_hosts()]
        print(f"\n*** Found {len(ips)} devices in your network. ***\n"
            "Please select a Server IP from the following list or press 's' to scan again:")
        for i, ip in enumerate(ips):
            print(f"\t{i + 1}) {ip}")
        choice = input("Enter a Server IP address list number or 's' to scan again: ")
        if choice.lower() == 's':
            continue
        else:
            choice = int(choice) - 1
            ip_address = ips[choice]
            port = 16666
            print(f"\nClient IP: {client_ip}, Server IP: {ip_address}")
            return (ip_address, port)

# Function to send the DataFrame to another device running the server script
def transmit_data(df, filename, server_address):
    """
    Transmits a DataFrame to a server.

    Parameters:
    df (pd.DataFrame): The DataFrame to be transmitted.
    filename (str): The filename to prepend to the DataFrame.

    Returns: None

    The function first defines the server address and port. It then converts the DataFrame to JSON, prepends the filename, and encodes the data as bytes.
    It creates a new socket, connects to the server, and receives a message from the server, which it prints.
    It then enters a while loop that continues until all data has been sent. Inside the loop, it sends the remaining data, checks if any data was sent, and updates the total amount of data sent.
    If no data was sent, it raises a RuntimeError.
    After all data has been sent, it prints a message indicating that the file was transmitted and that the connection was terminated.
    """
    
    # Convert the DataFrame to JSON and prepend the filename
    data = filename + '|||' + df.to_json()
    # Encode the data as bytes
    data_bytes = data.encode()
    
    # Create a new socket
    with socket.socket() as s:
        # Connect to the server
        s.connect(server_address)
        # Receive a message from the server
        msg = s.recv(1024)
        # Print the message
        print(msg.decode('ascii'))
        
        # Initialize the total amount of data sent
        total_sent = 0
        # Continue sending data until all data has been sent
        while total_sent < len(data_bytes):
            # Send the remaining data
            sent = s.send(data_bytes[total_sent:])
            # If no data was sent, raise an exception
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            # Update the total amount of data sent
            total_sent += sent
            
    # Print a message indicating that the file was transmitted
    print(f"Transmitted file: '{filename}'.")        
    # Print a message indicating that the connection was terminated
    print(f"Terminated connection to server {server_address}.\n")   
