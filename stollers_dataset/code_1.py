import matplotlib.pyplot as plt
import random

def compute_gini_index(access_data, attribute_index):
    yes_no_counts = {}
    for entry in access_data:
        key = entry[attribute_index]
        if key not in yes_no_counts:
            yes_no_counts[key] = [0, 0]  # [no_count, yes_count]
        yes_no_counts[key][entry[-1]] += 1

    total_entries = len(access_data)
    gini_index = 0
    for key, (no_count, yes_count) in yes_no_counts.items():
        total = no_count + yes_count
        gini_coefficient = 1 - (yes_count / total) ** 2 - (no_count / total) ** 2
        gini_index += (total / total_entries) * gini_coefficient

    return gini_index

def split_access_data(access_data, attribute_index):
    split_data = {}
    for entry in access_data:
        key = entry[attribute_index]
        if key not in split_data:
            split_data[key] = []
        split_data[key].append(entry)
    return split_data

def all_decisions_uniform(access_data):
    first_decision = access_data[0][-1]
    return all(entry[-1] == first_decision for entry in access_data)

def recursive_policy_mining(access_data, attributes, current_rule):
    if all_decisions_uniform(access_data):
        decision = "permit" if access_data[0][-1] == 1 else "deny"
        return [{"rule": current_rule, "decision": decision}]
    
    gini_list = [(compute_gini_index(access_data, i), i) for i in range(len(attributes))]
    gini_list.sort()

    best_attribute_index = gini_list[0][1]
    best_attribute = attributes[best_attribute_index]
    
    split_data = split_access_data(access_data, best_attribute_index)
    policy_rules = []

    for attribute_value, subset in split_data.items():
        new_rule = current_rule + [(best_attribute, attribute_value)]
        policy_rules.extend(recursive_policy_mining(subset, attributes, new_rule))

    return policy_rules

def policy_mining(access_data, attributes):
    return recursive_policy_mining(access_data, attributes, [])

# # Example usage with sample input data
# S = ["Alice", "Bob"]
# O = ["Document1", "Document2"]
# E = ["Lab", "Office"]

# SV = [["Professor", "CSE"], ["Student", "CSE"]]
# OV = [["Assignment", "Confidential"], ["Report", "Public"]]
# EV = [["Lab", "Morning"], ["Office", "Evening"]]

# A = [[[1, 0], [0, 1]], [[1, 1], [0, 0]]]

# attributes = ["Designation", "Department", "Type", "Classification", "Location", "Time"]

# SUBJECT, OBJECT, ENVIRONMENT
n1 = int(input("Enter size of Subject : "))
S = [f"S_{i}" for i in range(1, n1 + 1)]

n2 = int(input("Enter size of Object : "))
O = [f"O_{i}" for i in range(1, n2 + 1)]

n3 = int(input("Enter size of Environment : "))
E = [f"E_{i}" for i in range(1, n3 + 1)]


# ATTRIBUTES
n4 = int(input("Enter number of attributes for each Subject : "))
SA = [f"SA_{i}" for i in range(1, n4 + 1)]

n5 = int(input("Enter number of attributes for each Object : "))
OA = [f"OA_{i}" for i in range(1, n5 + 1)]

n6 = int(input("Enter number of attributes for each Environment : "))
EA = [f"EA_{i}" for i in range(1, n6 + 1)]

attributes = SA + OA + EA

# NUMBER OF DIFFERENT VALUES FOR EACH ATTRIBUTE
SA_values = {}
for i, attr in enumerate(SA, start=1):
    num_values = int(input(f"Enter number of values for {attr}: "))
    SA_values[attr] = [f"S_{i}_{j}" for j in range(1, num_values + 1)]
print("\nGenerated Values for Each Attribute:")
for attr, values in SA_values.items():
    print(f"{attr}: {', '.join(values)}")

OA_values = {}
for i, attr in enumerate(OA, start=1):
    num_values = int(input(f"Enter number of values for {attr}: "))
    OA_values[attr] = [f"O_{i}_{j}" for j in range(1, num_values + 1)]
print("\nGenerated Values for Each Attribute:")
for attr, values in OA_values.items():
    print(f"{attr}: {', '.join(values)}")

EA_values = {}
for i, attr in enumerate(EA, start=1):
    num_values = int(input(f"Enter number of values for {attr}: "))
    EA_values[attr] = [f"E_{i}_{j}" for j in range(1, num_values + 1)]
print("\nGenerated Values for Each Attribute:")
for attr, values in EA_values.items():
    print(f"{attr}: {', '.join(values)}")

# filling SV matrix 
SV = [[random.choice(SA_values[SA[j]]) for j in range(n4)] for i in range(n1)]
OV = [[random.choice(OA_values[OA[j]]) for j in range(n5)] for i in range(n2)]
EV = [[random.choice(EA_values[EA[j]]) for j in range(n6)] for i in range(n3)]
# # ATTRIBUTE VALUES
# SV = [[f"S_{i}_{j}" for j in range(1, n4 + 1)] for i in range(1, n1 + 1)]

# OV = [[f"O_{i}_{j}" for j in range(1, n5 + 1)] for i in range(1, n2 + 1)]

# EV = [[f"E_{i}_{j}" for j in range(1, n6 + 1)] for i in range(1, n3 + 1)]

# # ACCESS MATRIX
# A = [[[random.choice([0, 1]) for _ in range(n3)] for _ in range(n2)] for _ in range(n1)]
# print("Generated 3D Access matrix:")
# for row in A:
#     for column in row:
#         print(column)

###### NO OF RULES AND FILLING ACCESS CONTROL MATRIX
N = int(input("Enter the number of rules : "))

def generate_rules_1(N, n4, n5, n6, SA_values, OA_values, EA_values):
    rules = []
    
    for _ in range(N):
        rule_parts = []
        
        # Generate SA attributes
        for i in range(1, n4 + 1):
            key = f"SA_{i}"
            choices = SA_values.get(key, []) + ['*']
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        # Generate OA attributes
        for i in range(1, n5 + 1):
            key = f"OA_{i}"
            choices = OA_values.get(key, []) + ['*']
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        # Generate EA attributes
        for i in range(1, n6 + 1):
            key = f"EA_{i}"
            choices = EA_values.get(key, []) + ['*']
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        rules.append(", ".join(rule_parts))
        # print(rule_parts)
    
    return rules

def generate_rules_2(N, n4, n5, n6, SA_values, OA_values, EA_values):
    rules = []
    
    for _ in range(N):
        rule_parts = []
        
        # Generate SA attributes
        for i in range(1, n4 + 1):
            key = f"SA_{i}"
            choices = SA_values.get(key, []) + ['*', '*']  # Double the probability of '*'
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        # Generate OA attributes
        for i in range(1, n5 + 1):
            key = f"OA_{i}"
            choices = OA_values.get(key, []) + ['*', '*']  # Double the probability of '*'
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        # Generate EA attributes
        for i in range(1, n6 + 1):
            key = f"EA_{i}"
            choices = EA_values.get(key, []) + ['*', '*']  # Double the probability of '*'
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        rules.append(", ".join(rule_parts))
    
    return rules

def generate_rules_half(N, n4, n5, n6, SA_values, OA_values, EA_values):
    rules = []
    
    for _ in range(N):
        rule_parts = []
        
        # Function to choose with 50% probability for '*'
        def choose_value(values):
            if random.random() < 0.5:  # 50% probability of choosing '*'
                return '*'
            return random.choice(values) if values else '*'

        # Generate SA attributes
        for i in range(1, n4 + 1):
            key = f"SA_{i}"
            rule_parts.append(f"{key} = {choose_value(SA_values.get(key, []))}")
        
        # Generate OA attributes
        for i in range(1, n5 + 1):
            key = f"OA_{i}"
            rule_parts.append(f"{key} = {choose_value(OA_values.get(key, []))}")
        
        # Generate EA attributes
        for i in range(1, n6 + 1):
            key = f"EA_{i}"
            rule_parts.append(f"{key} = {choose_value(EA_values.get(key, []))}")
        
        rules.append(", ".join(rule_parts))
    
    return rules

def flatten_and_compute_weights(matrix):
    value_counts = {}
    total_count = 0

    for row in matrix:
        for value in row:
            value_counts[value] = value_counts.get(value, 0) + 1
            total_count += 1

    # Convert counts to probabilities
    weighted_values = list(value_counts.keys())
    weights = [count / total_count for count in value_counts.values()]

    print("Values and their probabilities:")
    for val, weight in zip(weighted_values, weights):
        print(f"{val}: {weight:.4f}")

    return weighted_values, weights

def generate_rules_weighted(N, n4, n5, n6, SV, OV, EV):
    rules = []

    # Compute weighted value distributions
    SA_values_, SA_weights_ = flatten_and_compute_weights(SV)
    OA_values_, OA_weights_ = flatten_and_compute_weights(OV)
    EA_values_, EA_weights_ = flatten_and_compute_weights(EV)

    for _ in range(N):
        rule_parts = []

        # Function to sample a value based on weights with '*' having fixed probability
        def choose_weighted(values, weights, star_prob=0.5):
            return random.choices(values, weights=weights, k=1)[0]

        # Generate SA attributes
        for i in range(1, n4 + 1):
            rule_parts.append(f"SA_{i} = {choose_weighted(SA_values_, SA_weights_)}")

        # Generate OA attributes
        for i in range(1, n5 + 1):
            rule_parts.append(f"OA_{i} = {choose_weighted(OA_values_, OA_weights_)}")

        # Generate EA attributes
        for i in range(1, n6 + 1):
            rule_parts.append(f"EA_{i} = {choose_weighted(EA_values_, EA_weights_)}")

        rules.append(", ".join(rule_parts))

    return rules

def flatten_and_compute_weights_1(matrix, star_weight):
    value_counts = {}
    total_count = 0

    for row in matrix:
        for value in row:
            value_counts[value] = value_counts.get(value, 0) + 1
            total_count += 1

    # Add '*' to the value list with a custom weight
    value_counts['*'] = star_weight
    total_count += star_weight

    # Convert counts to probabilities
    weighted_values = list(value_counts.keys())
    weights = [count / total_count for count in value_counts.values()]

    return weighted_values, weights

def generate_rules_weighted_1(N, n4, n5, n6, SV, OV, EV, star_weight=1):
    rules = []

    # Compute weighted value distributions with star_weight
    SA_values_, SA_weights_ = flatten_and_compute_weights_1(SV, star_weight)
    OA_values_, OA_weights_ = flatten_and_compute_weights_1(OV, star_weight)
    EA_values_, EA_weights_ = flatten_and_compute_weights_1(EV, star_weight)

    for _ in range(N):
        rule_parts = []

        # Function to sample a value based on weights
        def choose_weighted(values, weights):
            return random.choices(values, weights=weights, k=1)[0]

        # Generate SA attributes
        for i in range(1, n4 + 1):
            rule_parts.append(f"SA_{i} = {choose_weighted(SA_values_, SA_weights_)}")

        # Generate OA attributes
        for i in range(1, n5 + 1):
            rule_parts.append(f"OA_{i} = {choose_weighted(OA_values_, OA_weights_)}")

        # Generate EA attributes
        for i in range(1, n6 + 1):
            rule_parts.append(f"EA_{i} = {choose_weighted(EA_values_, EA_weights_)}")

        rules.append(", ".join(rule_parts))

    return rules

def generate_rules_weighted_half(N, n4, n5, n6, SV, OV, EV):
    rules = []

    # Compute weighted value distributions
    SA_values_, SA_weights_ = flatten_and_compute_weights(SV)
    OA_values_, OA_weights_ = flatten_and_compute_weights(OV)
    EA_values_, EA_weights_ = flatten_and_compute_weights(EV)

    for _ in range(N):
        rule_parts = []

        # Function to sample a value based on weights with '*' having fixed probability
        def choose_weighted(values, weights, star_prob=0.5):
            if random.random() < star_prob:
                return '*'
            return random.choices(values, weights=weights, k=1)[0]

        # Generate SA attributes
        for i in range(1, n4 + 1):
            rule_parts.append(f"SA_{i} = {choose_weighted(SA_values_, SA_weights_)}")

        # Generate OA attributes
        for i in range(1, n5 + 1):
            rule_parts.append(f"OA_{i} = {choose_weighted(OA_values_, OA_weights_)}")

        # Generate EA attributes
        for i in range(1, n6 + 1):
            rule_parts.append(f"EA_{i} = {choose_weighted(EA_values_, EA_weights_)}")

        rules.append(", ".join(rule_parts))

    return rules


# rules = generate_rules_1(N, n4, n5, n6, SA_values, OA_values, EA_values) # 1 STAR
# rules = generate_rules_2(N, n4, n5, n6, SA_values, OA_values, EA_values) # 2 STAR
rules = generate_rules_half(N, n4, n5, n6, SA_values, OA_values, EA_values) # STAR PROB = 0.5
# rules = generate_rules_weighted(N, n4, n5, n6, SA_values, OA_values, EA_values) # NO STAR, WEIGHTED 
# rules = generate_rules_weighted_1(N, n4, n5, n6, SA_values, OA_values, EA_values) # 1 STAR, WEIGHTED 
# rules = generate_rules_weighted_half(N, n4, n5, n6, SA_values, OA_values, EA_values)  # STAR PROB = 0.5 , WEIGHTED
# for rule in rules:
#     print(rule)

# print("Access Control Matrix")

# # ACCESS MATRIX
A = [[[0] * n3 for _ in range(n2)] for _ in range(n1)]

def satisfies_rule(rule, SA1, OA1, EA1):
    rule_parts = rule.split(", ")
    for part in rule_parts:
        key, value = part.split(" = ")
        if key.startswith("SA_") and value not in SA1 and value != '*':
            return False
        if key.startswith("OA_") and value not in OA1 and value != '*':
            return False
        if key.startswith("EA_") and value not in EA1 and value != '*':
            return False
    return True

def fill_matrix(A, SV, OV, EV, rules, n1, n2, n3):
    for i in range(n1):
        for j in range(n2):
            for k in range(n3):
                SA1 = SV[i]
                OA1 = OV[j]
                EA1 = EV[k]
                A[i][j][k] = 1 if any(satisfies_rule(rule, SA1, OA1, EA1) for rule in rules) else 0

fill_matrix(A, SV, OV, EV, rules, n1, n2, n3)
# for layer in A:
#     for row in layer:
#         print(row)
#     print()

# n1 = int(input("Enter size of S : "))
# array = [f"S{i}" for i in range(1, n1 + 1)]
# print("Generated array:", array)


# Preparing access data
def prepare_access_data(S, O, E, SV, OV, EV, A):
    access_data = []
    for i in range(len(S)):
        for j in range(len(O)):
            for k in range(len(E)):
                T = SV[i] + OV[j] + EV[k] + [A[i][j][k]]  # Concatenate attributes and access decision
                access_data.append(T)
    return access_data

access_data = prepare_access_data(S, O, E, SV, OV, EV, A)

# Plot the distribution of "permit" and "deny" decisions
def plot_access_decision_distribution(access_data):
    decision_counts = {"permit": 0, "deny": 0}
    for entry in access_data:
        decision = "permit" if entry[-1] == 1 else "deny"
        decision_counts[decision] += 1

    # Plotting
    labels = list(decision_counts.keys())
    counts = list(decision_counts.values())

    plt.bar(labels, counts, color=["green", "red"])
    plt.xlabel("Access Decision")
    plt.ylabel("Count")
    plt.title("Distribution of Access Decisions")
    plt.show()

# Compute and plot Gini Index values for each attribute
def plot_gini_indices(access_data, attributes):
    gini_values = [compute_gini_index(access_data, i) for i in range(len(attributes))]

    # Plotting
    plt.bar(attributes, gini_values, color="blue")
    plt.xlabel("Attributes")
    plt.ylabel("Gini Index")
    plt.title("Gini Index for Each Attribute")
    plt.xticks(rotation=45)
    plt.show()

# Display the access data
# print("\nAccess data : ")
# for individual_access_data in access_data:
#     print(individual_access_data)

# Visualize the data
plot_access_decision_distribution(access_data)
plot_gini_indices(access_data, attributes)

# Mine the ABAC policy
policy = policy_mining(access_data, attributes)
print("\nGenerated ABAC Policy:")
for rule in policy:
    print(rule)
print()
