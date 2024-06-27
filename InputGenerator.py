import csv
import random

def pick_row_from_csv(filename):
    rows = []
    chances = []
    
    # Read the CSV file
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
            chances.append(float(row['Chance']))
    
    # Generate a random number between 0 and 1
    random_number = random.random()
    
    # Find the index of the row based on the chance
    cumulative_chance = 0
    for i, chance in enumerate(chances):
        cumulative_chance += chance
        if random_number <= cumulative_chance:
            return rows[i]
    
    # If no row is found, return None
    return None

# Usage example
filename = 'AllObstacleGame_DataWithChance.csv'
new_filename = 'AllObstacleGame_Resampled_Data.csv'

with open(new_filename, 'w', newline='') as new_file:
    writer = csv.writer(new_file)

    # Write the header
    writer.writerow(['1', '2', '3', '4', '5', '6', 'Action'])

    # Pick a row 100 times and write to the new file
    for _ in range(2000):
        random_row = pick_row_from_csv(filename)
        if random_row:
            writer.writerow([random_row['1'], random_row['2'], random_row['3'], random_row['4'], random_row['5'], random_row['6'], random_row['Action']])
        else:
            print("No row found.")