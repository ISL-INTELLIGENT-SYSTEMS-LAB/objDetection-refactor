# Standard python libraries
import os
import pickle
import re
import signal
import socket
import threading
import time
import math
from fractions import Fraction
from typing import Tuple

# External libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import pytorch3d
import nums_from_string
from scipy.spatial import ConvexHull
from scipy.spatial.distance import directed_hausdorff
from torch.autograd import Function

# Specific libraries
from pytorch3d import _C, ops
from utils import *
import pyzed.sl as sl
from network_relation_MOD import network_relation
from hungarian import linear_sum_assignment
import torch.nn.functional as F
from pytorch3d.ops import box3d_overlap

cwd = os.getcwd()

def generate_Relation(expPath=cwd):
	expPath =  expPath 
	files = os.listdir(expPath)
	# Remove files that don't start with 'data'
	files = [file for file in files if file.startswith('data')]

  # Prints out the files in the list post removal
	for file in files:
		print(file)

def main():
  # Experiment Path listed below is for testing purposes
  expPath = os.path.join(cwd, 'data_collection', '10-24-23', 'Exp10A')
	generate_Relation(expPath)


if __name__ == '__main__':
	main()
  

def generate_Relation(expPath=cwd, n=0):
	"""
	Generates a correspondence matrix between objects in different frames

	Parameters:
		expPath (str): path to the experiment directory containing the data files
	"""
	expPath =  expPath
	# Get the list of files in the directory 
	try:
		files = os.listdir(expPath)
		# Remove files that don't start with 'data'
		files = [file for file in files if file.startswith('data').endswith('.csv')]
	except FileNotFoundError:
		print("Directory not found")
		return
	except Exception as e:
		print(e)
		return 

	# Print the filenames
	for file in files:
		print(file)
	# Assemble pandas dataframes for each file
	correspondence = pd.DataFrame(np.random.randint(0,5,size=(1, 3)), columns = [file.split('.csv')[0] for file in files], index=['Person_0'])
	correspondence[:] = np.nan
	# Create a correspondence matrix between objects in different frames
	for first_file in files:
		for second_file in files:
	 		# Skip if the same file		
			if first_file != second_file:
				df_1 = get_data(first_file)
				df_2 = get_data(second_file)
				print("new frame")
				# Check if the dataframes have the same number of objects
				if df_1.shape[0] != df_2.shape[0]:
					print('Error')
					if df_1.shape[0] > df_2.shape[0]:
						df_2.loc[len(df_2.index)] = [None, None] 
					else:
						df_1.loc[len(df_1.index)] = [None, None] 
				# Create a temporary dataframe to store the distances between objects
				temp = pd.DataFrame(np.random.random_sample(size=(1, 1)), columns = df_1['Object'].to_list(), index=df_2['Object'].to_list())
				# Calculate the Hausdorff distance between the 3D bounding boxes of the objects
				for i in range(0,len(df_1)):
					for j in range(0,len(df_2)):
						u = df_1['3D_Bounding_Box'][i]
						v = df_2['3D_Bounding_Box'][j]
						print(u)
						print("-----")
						print(v)
						dist = hausdorff(u, v)
						# Store the distance in the temporary dataframe
						temp.at[df_2['Object'][j], df_1['Object'][i]] = dist[0]
				# Solve the assignment problem using the Hungarian algorithm
				cols, rows, _ = hungarian(temp.to_numpy())
				
				# Update the correspondence matrix
				if n == 0:
					correspondence[first_file.split('.csv')[0]] = cols
					correspondence[second_file.split('.csv')[0]] = rows
				else: 
					correspondence = update_correspondence(cols, rows, correspondence, first_file.split('.csv')[0], second_file.split('.csv')[0])
				n+=1

	print(correspondence)

	# Return the correspondence matrix
	return correspondence


def main():
	# Path to the experiment directory
	expPath = os.path.join(cwd, 'data_collection', '10-24-23', 'Exp10A')
	generate_Relation(expPath)


if __name__ == '__main__':
	main()

