import csv
from backend.directions import *


def test_get_direction():
    with open("test/sample_addresses.csv", "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        address_list = []
        for row in reader:
            home, target = row["home_address"], row["target_address"]
            address_list.append([home, target])
