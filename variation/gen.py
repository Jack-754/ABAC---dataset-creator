import config
import random
import gen_rules
import json

n1 = config.n1
n2 = config.n2
n3 = config.n3
n4 = config.n4
n5 = config.n5
n6 = config.n6
subject_attributes = config.subject_attributes
object_attributes = config.object_attributes
environment_attributes = config.environment_attributes
N = config.n

# SUBJECT, OBJECT, ENVIRONMENT
S = [f"S_{i}" for i in range(1, n1 + 1)]
O = [f"O_{i}" for i in range(1, n2 + 1)]
E = [f"E_{i}" for i in range(1, n3 + 1)]

# ATTRIBUTES
SA = [f"SA_{i}" for i in range(1, n4 + 1)]
OA = [f"OA_{i}" for i in range(1, n5 + 1)]
EA = [f"EA_{i}" for i in range(1, n6 + 1)]

attributes = SA + OA + EA

# VALUES FOR EACH ATTRIBUTE
SA_values = {}
for i, (attr, num_values) in enumerate(zip(SA, subject_attributes), start=1):
    SA_values[attr] = [f"S_{i}_{j}" for j in range(1, num_values + 1)]

OA_values = {}
for i, (attr, num_values) in enumerate(zip(OA, object_attributes), start=1):
    OA_values[attr] = [f"O_{i}_{j}" for j in range(1, num_values + 1)]

EA_values = {}
for i, (attr, num_values) in enumerate(zip(EA, environment_attributes), start=1):
    EA_values[attr] = [f"E_{i}_{j}" for j in range(1, num_values + 1)]

# filling SV matrix 
SV = [[random.choice(SA_values[SA[j]]) for j in range(n4)] for i in range(n1)]
OV = [[random.choice(OA_values[OA[j]]) for j in range(n5)] for i in range(n2)]
EV = [[random.choice(EA_values[EA[j]]) for j in range(n6)] for i in range(n3)]

# WRITE ABOVE TO A FILE
data = {
    "SV": SV,
    "OV": OV,
    "EV": EV
}
with open(r'C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\output.json', 'w') as f:
    json.dump(data, f, indent=4)

# RULE GENERATION FUNCTION
rules = gen_rules.generate_rules_half(N, n4, n5, n6, SA_values, OA_values, EA_values) # STAR PROB = 0.5

# WRITE RULES TO .TXT FILE
with open(r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\rules_temp.txt", "w") as file:
    for rule in rules:
        file.write(rule + "\n")

# ACCESS MATRIX
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

no_of_ones = 0
def fill_matrix(A, SV, OV, EV, rules, n1, n2, n3):
    global no_of_ones
    for i in range(n1):
        for j in range(n2):
            for k in range(n3):
                SA1 = SV[i]
                OA1 = OV[j]
                EA1 = EV[k]
                A[i][j][k] = 1 if any(satisfies_rule(rule, SA1, OA1, EA1) for rule in rules) else 0
                no_of_ones += A[i][j][k]

fill_matrix(A, SV, OV, EV, rules, n1, n2, n3)
# print("No. of ones in ACM : ", no_of_ones)

# WRITE ACCESS CONTROL MATRIX TO FILE
with open(r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\ACM.txt", "w") as file:
    for i in range(config.n1):
        for row in A[i]:
            file.write(" ".join(map(str, row)) + "\n")
        file.write("\n")

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

# WRITE ACCESS DATA TO FILE
with open(r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\access_data.txt", "w") as file:
    for row in access_data:
        file.write(" ".join(map(str, row)) + "\n")
