import csv

def read_csv(file_path):
    """Reads CSV and returns a list of dictionaries"""
    with open(file_path, newline="") as csvfile:
        return list(csv.DictReader(csvfile))