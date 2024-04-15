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
  

