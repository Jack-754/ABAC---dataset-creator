import config
import ast
import json

with open(r'C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\output.json', 'r') as f:
    data = json.load(f)

SV = data["SV"]
OV = data["OV"]
EV = data["EV"]

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

# INPUT MATRIX A1
A1 = []
with open(r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\ACM.txt", "r") as file:
    matrix = []
    for line in file:
        line = line.strip()
        if line:
            matrix.append(list(map(int, line.split())))
        else:
            if matrix:
                A1.append(matrix)
                matrix = []
    
    if matrix:
        A1.append(matrix)

# print("Old matrix : ")
# print(A1)

# MATRIX GENERATED FROM GENERATED RULES
def satisfies_rule(rule, SA1, OA1, EA1):
    for key, value in rule:
        if key.startswith("SA_") and value not in SA1 and value != '*':
            return False
        if key.startswith("OA_") and value not in OA1 and value != '*':
            return False
        if key.startswith("EA_") and value not in EA1 and value != '*':
            return False
    return True

# READ RULES FROM FILE
rules = []
with open(r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\rules.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line:
            rule_entry = ast.literal_eval(line)
            rules.append(rule_entry)

# INITIALIZE ACCESS CONTROL MATRIX WITH DEFAULT VALUE 0
A2 = [[[0] * n3 for _ in range(n2)] for _ in range(n1)]

def fill_matrix(A2, SV, OV, EV, rules, n1, n2, n3):
    for i in range(n1):
        for j in range(n2):
            for k in range(n3):
                SA1 = SV[i]
                OA1 = OV[j]
                EA1 = EV[k]
                
                # Default is 0 (deny)
                decision = 0
                
                for rule_entry in rules:
                    if satisfies_rule(rule_entry['rule'], SA1, OA1, EA1):
                        if rule_entry['decision'] == 'permit':
                            decision = 1  # Permit takes precedence if matched
                        elif rule_entry['decision'] == 'deny':
                            decision = 0  # Deny overrides permit
                            break
                
                A2[i][j][k] = decision

fill_matrix(A2, SV, OV, EV, rules, n1, n2, n3)

# print("New matrix : ")
# print(A2)

# WRITE ACCESS CONTROL MATRIX TO FILE
with open(r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\ACM2.txt", "w") as file:
    for i in range(config.n1):
        for row in A2[i]:
            file.write(" ".join(map(str, row)) + "\n")
        file.write("\n")

# COMPARE WHETHER MATRICES ARE SAME OR NOT
def are_matrices_equal(A1, A2):
    if len(A1) != len(A2) or len(A1[0]) != len(A2[0]) or len(A1[0][0]) != len(A2[0][0]):
        return False
    
    for i in range(len(A1)):
        for j in range(len(A1[i])):
            for k in range(len(A1[i][j])):
                if A1[i][j][k] != A2[i][j][k]:
                    return False
    return True

if are_matrices_equal(A1, A2):
    print("The matrices are the same.")
else:
    print("The matrices are different.")
