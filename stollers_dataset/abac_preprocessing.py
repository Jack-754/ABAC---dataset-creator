# def preprocess_healthcare_data(input_file, output_file):
#     """
#     Preprocess healthcare access decisions data to create a fixed-width format
#     suitable for the policy mining algorithm.
#     """
#     # Read the input file
#     with open(input_file, 'r') as f:
#         lines = f.readlines()
    
#     # Parse all lines to extract all possible attributes
#     all_attributes = set()
#     access_data = []
    
#     for line in lines:
#         # Parse the line into attribute-value pairs
#         pairs = line.strip().split(', ')
#         entry = {}
        
#         for pair in pairs:
#             if ' = ' in pair:
#                 attr, value = pair.split(' = ', 1)
#                 entry[attr] = value
#                 all_attributes.add(attr)
    
#         access_data.append(entry)
    
#     # Remove access_decision from attributes and ensure it's the last column
#     all_attributes.discard('access_decision')
    
#     # Convert to sorted list for consistent ordering
#     sorted_attributes = sorted(list(all_attributes))
    
#     # Write the standardized data to output file
#     with open(output_file, 'w') as f:
#         # Write header
#         f.write(' '.join(sorted_attributes + ['access_decision']) + '\n')
        
#         # Write data rows
#         for entry in access_data:
#             row = []
#             for attr in sorted_attributes:
#                 if attr in entry:
#                     row.append(entry[attr])
#                 else:
#                     row.append('NA')  # Placeholder for missing values
            
#             # Add access decision at the end
#             row.append(entry.get('access_decision', '0'))  # Default to 0 if missing
            
#             f.write(' '.join(row) + '\n')
    
#     return sorted_attributes

# def modify_policy_mining_code(attributes_list):
#     """
#     Generate modified policy mining code based on the attributes list.
#     """
#     code = """
# import numpy as np

# # Define attributes based on preprocessed data
# attributes = {0}

# def compute_gini_index(access_data, attribute_index):
#     yes_no_counts = {{}}
#     for entry in access_data:
#         key = entry[attribute_index]
#         if key not in yes_no_counts:
#             yes_no_counts[key] = [0, 0]  # [no_count, yes_count]
#         yes_no_counts[key][int(entry[-1])] += 1

#     total_entries = len(access_data)
#     gini_index = 0
#     for key, (no_count, yes_count) in yes_no_counts.items():
#         total = no_count + yes_count
#         if total > 0:  # Avoid division by zero
#             gini_coefficient = 1 - (yes_count / total) ** 2 - (no_count / total) ** 2
#             gini_index += (total / total_entries) * gini_coefficient

#     return gini_index

# def split_access_data(access_data, attribute_index):
#     split_data = {{}}
#     for entry in access_data:
#         key = entry[attribute_index]
#         if key not in split_data:
#             split_data[key] = []
#         split_data[key].append(entry)
#     return split_data

# def all_decisions_uniform(access_data):
#     first_decision = access_data[0][-1]
#     return all(entry[-1] == first_decision for entry in access_data)

# def recursive_policy_mining(access_data, attributes, current_rule):
#     if not access_data:  # Handle empty data case
#         return []
        
#     if all_decisions_uniform(access_data):
#         decision = "permit" if access_data[0][-1] == '1' else "deny"
#         return [{{"rule": current_rule, "decision": decision}}]
    
#     gini_list = [(compute_gini_index(access_data, i), i) for i in range(len(attributes))]
#     gini_list.sort()

#     best_attribute_index = gini_list[0][1]
#     best_attribute = attributes[best_attribute_index]
    
#     split_data = split_access_data(access_data, best_attribute_index)
#     policy_rules = []

#     for attribute_value, subset in split_data.items():
#         new_rule = current_rule + [(best_attribute, attribute_value)]
#         policy_rules.extend(recursive_policy_mining(subset, attributes, new_rule))

#     return policy_rules

# def policy_mining(access_data, attributes):
#     return recursive_policy_mining(access_data, attributes, [])

# # Read preprocessed access data
# access_data = []
# with open("healthcare_preprocessed.txt", "r") as file:
#     # Skip header line
#     header = file.readline().strip().split()
    
#     for line in file:
#         access_data.append(line.strip().split())

# # Run policy mining
# policy = policy_mining(access_data, attributes)

# # Write policy to file
# with open("healthcare_rules.txt", "w") as file:
#     for rule in policy:
#         file.write(str(rule) + "\\n")
#     file.write("\\n")

# print(f"Policy mining complete. Generated {{len(policy)}} rules.")
# """.format(attributes_list)
    
#     return code

# # Main execution
# if __name__ == "__main__":
#     # Preprocess the healthcare data
#     attributes = preprocess_healthcare_data(r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\healthcare_access_decisions.txt", r"healthcare_preprocessed.txt")
    
#     # Generate modified policy mining code
#     mining_code = modify_policy_mining_code(attributes)
    
#     # Write the modified policy mining code to a file
#     with open("healthcare_policy_mining.py", "w") as f:
#         f.write(mining_code)
    
#     print("Preprocessing complete. Run healthcare_policy_mining.py to generate rules.")

"""
Modified policy mining algorithm to handle variable-length data rows
"""

# Define attributes in a more flexible way
attributes = [
    "user",
    "resource",
    "action",
    "user_position",
    "user_ward",
    "resource_type",
    "resource_author",
    "resource_patient",
    "resource_topics",
    "resource_treatingTeam",
    "resource_ward"
]

def get_attribute_value(entry, attribute_index):
    """Safely get attribute value, handling variable-length entries"""
    if attribute_index < len(entry) - 1:  # -1 to account for decision at the end
        return entry[attribute_index]
    return "N/A"  # Default value for missing attributes

def compute_gini_index(access_data, attribute_index):
    """Calculate Gini index with handling for variable-length entries"""
    yes_no_counts = {}
    for entry in access_data:
        key = get_attribute_value(entry, attribute_index)
        if key not in yes_no_counts:
            yes_no_counts[key] = [0, 0]  # [no_count, yes_count]
        
        # Always assume the decision is the last element
        decision = entry[-1]
        yes_no_counts[key][decision] += 1

    total_entries = len(access_data)
    gini_index = 0
    for key, (no_count, yes_count) in yes_no_counts.items():
        total = no_count + yes_count
        gini_coefficient = 1 - (yes_count / total) ** 2 - (no_count / total) ** 2
        gini_index += (total / total_entries) * gini_coefficient

    return gini_index

def split_access_data(access_data, attribute_index):
    """Split data based on attribute values, handling variable-length entries"""
    split_data = {}
    for entry in access_data:
        key = get_attribute_value(entry, attribute_index)
        if key not in split_data:
            split_data[key] = []
        split_data[key].append(entry)
    return split_data

def all_decisions_uniform(access_data):
    """Check if all decisions in the dataset are the same"""
    first_decision = access_data[0][-1]
    return all(entry[-1] == first_decision for entry in access_data)

def recursive_policy_mining(access_data, attributes, current_rule):
    """Recursively mine policy rules, handling variable-length entries"""
    if not access_data:
        return []
        
    if all_decisions_uniform(access_data):
        decision = "permit" if access_data[0][-1] == 1 else "deny"
        return [{"rule": current_rule, "decision": decision}]
    
    # Calculate Gini index for each attribute
    gini_list = []
    for i in range(len(attributes)):
        gini_value = compute_gini_index(access_data, i)
        gini_list.append((gini_value, i))

    gini_list.sort()  # Sort by Gini value (lowest first)

    best_attribute_index = gini_list[0][1]
    best_attribute = attributes[best_attribute_index]
    
    split_data = split_access_data(access_data, best_attribute_index)
    policy_rules = []

    for attribute_value, subset in split_data.items():
        new_rule = current_rule + [(best_attribute, attribute_value)]
        policy_rules.extend(recursive_policy_mining(subset, attributes, new_rule))

    return policy_rules

def policy_mining(access_data, attributes):
    """Mine policy rules from access data"""
    return recursive_policy_mining(access_data, attributes, [])

def parse_access_data(file_path):
    """Parse access data from file, handling variable-length rows"""
    access_data = []
    with open(file_path, "r") as file:
        for line in file:
            row = line.strip().split()
            # Convert numeric values to integers
            row = [int(x) if x.isdigit() else x for x in row]
            access_data.append(row)
    return access_data

def main():
    # Path to your dataset
    file_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\healthcare_access_decisions.txt"
    
    # Parse access data
    access_data = parse_access_data(file_path)
    
    # Mine policy rules
    policy = policy_mining(access_data, attributes)
    
    # Write policy to file
    output_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\rules_stollers.txt"
    with open(output_path, "w") as file:
        for rule in policy:
            file.write(str(rule) + "\n")
        file.write("\n")
    
    print(f"Policy mining completed. Rules written to {output_path}")

if __name__ == "__main__":
    main()