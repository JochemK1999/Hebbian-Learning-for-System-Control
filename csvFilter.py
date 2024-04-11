import csv

input_file = 'data.csv'
output_file = 'filtered_data.csv'

with open(input_file, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

filtered_data = []
inside_block = False
block_length = 0

for row in data:
    if sum(map(int, row[:-2])) == 0:
        continue

    if row[-2] == 'True':
        if not inside_block:
            inside_block = True
            filtered_data.append(row[:-2] + row[-1:])
        if row[-1] == "jump":
            block_length += 1
    else:
        if inside_block and block_length > 10:
            filtered_data[-1][-1] = 'long_jump'
        inside_block = False
        block_length = 0
        filtered_data.append(row[:-2] + row[-1:])

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(filtered_data)