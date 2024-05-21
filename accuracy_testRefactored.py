import os
import numpy as np

class Node:
    def __init__(self, position):
        self.position = position

def get_data_path():
    """Return the data directory path."""
    return '/home/mrrobot/Documents/ISL-Projects-main/TurtlebotZED/data_collection' 

def get_csv_file():
    """Return the CSV file name."""
    return "data_exp_testFiles-1pos_-3-2.83-2+rot_0-0-0.csv" 

def get_people_truth():
    """Return a list of ground truth positions."""
    person0 = Node(np.array([-1, (69/12)/2, -10]))  # Eric
    return [person0] 

def convert_coordinates(coord_str):
    """Convert a string of coordinates to a list of floats."""
    if not coord_str:
        return []
    negative_sign = -1 if coord_str[0] == '-' else 1
    coordinates = coord_str.split('-')
    list_final = []
    for coordinate in coordinates:
        if coordinate.startswith('-'):
            list_final.append(negative_sign * float(coordinate[1:]))
        else:
            list_final.append(float(coordinate))
    return list_final

def positional_accuracy(person_truth_coords, person_exp_coords):
    """Calculate the positional accuracy between ground truth and experimental coordinates."""
    distance = np.linalg.norm(person_truth_coords - person_exp_coords)
    return distance

def load_csv_data(file_path):
    """Load CSV data into a pandas DataFrame."""
    try:
        import pandas as pd
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

if __name__ == "__main__":
    root = get_data_path()
    csvfile = get_csv_file()
    people_truth = get_people_truth()

    file_path = os.path.join(root, csvfile)
    df = load_csv_data(file_path)
    if df is not None:
        total_pos_diff = sum([positional_accuracy(person_truth.position, convert(coordinates)) for person_truth, coordinates in zip(people_truth, df["Object_Position"])])
        person_pos_diff = total_pos_diff / len(people_truth)
        print(person_pos_diff)
