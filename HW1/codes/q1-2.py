import csv

def read_data(filename):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        data = [tuple(row) for row in reader]
    return data

def map_function(input):
    product_category = input[0]
    action = input[2]  
    return [(product_category, action)]

def group_by(data):
    grouped_data = {}
    for key, value in data:
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(value)
    return grouped_data.items()

def reduce_function(grouped_data):
    results = {}
    for key, values in grouped_data:
        count = len(values)
        results[key] = count
    return results


input_data = read_data("social_media_dataset.csv")

mapped_data = []
for entry in input_data:
    mapped_data.extend(map_function(entry))
# print("\nData after Map Function:")
# print(mapped_data[:10])

grouped_data = group_by(mapped_data)
# print("\nData after Group-By Function:")
# print(grouped_data)

reduced_data = reduce_function(grouped_data)

# sorted_data = sorted(reduced_data.items(), key=lambda x: x[1], reverse=True)
sorted_data = sorted(reduced_data.items(), key=lambda x: (-x[1], -int(x[0])))


print("Top 10 users:")
for i, (user_id, action_type) in enumerate(sorted_data[:10], 1):
    print(f"{i}. User ID: {user_id}, Number of actions: {action_type}")