# """
# Updated comparison script for healthcare dataset with variable-length rows
# """
# import ast

# # Define attributes
# attributes = [
#     "user",
#     "resource",
#     "action",
#     "user_position",
#     "user_ward",
#     "resource_type",
#     "resource_author",
#     "resource_patient",
#     "resource_topics",
#     "resource_treatingTeam",
#     "resource_ward"
# ]

# def parse_access_data(file_path):
#     """Parse access data from file, handling variable-length rows"""
#     access_data = []
#     with open(file_path, "r") as file:
#         for line in file:
#             row = line.strip().split()
#             # Convert numeric values to integers
#             row = [int(x) if x.isdigit() else x for x in row]
#             access_data.append(row)
#     return access_data

# def parse_rules(file_path):
#     """Parse policy rules from file"""
#     rules = []
#     with open(file_path, "r") as file:
#         for line in file:
#             line = line.strip()
#             if line:
#                 try:
#                     rule_entry = ast.literal_eval(line)
#                     rules.append(rule_entry)
#                 except (SyntaxError, ValueError) as e:
#                     print(f"Error parsing rule: {line}")
#                     print(f"Error details: {e}")
#     return rules

# def get_attribute_value(entry, attribute_index):
#     """Safely get attribute value, handling variable-length entries"""
#     if attribute_index < len(entry) - 1:  # -1 to account for decision at the end
#         return entry[attribute_index]
#     return "N/A"  # Default value for missing attributes

# def satisfies_rule(rule, entry):
#     """Check if an entry satisfies a rule"""
#     for attribute, value in rule:
#         attr_index = attributes.index(attribute)
#         entry_value = get_attribute_value(entry, attr_index)
        
#         if entry_value != value and value != '*':
#             return False
#     return True

# def apply_rules(access_data, rules):
#     """Apply rules to predict decisions"""
#     predicted_decisions = []
    
#     for entry in access_data:
#         # Default is 0 (deny)
#         decision = 0
        
#         for rule_entry in rules:
#             if satisfies_rule(rule_entry['rule'], entry):
#                 if rule_entry['decision'] == 'permit':
#                     decision = 1
#                     break  # Permit takes precedence if matched
#                 elif rule_entry['decision'] == 'deny':
#                     decision = 0
#                     # Don't break, continue checking other rules
        
#         predicted_decisions.append(decision)
    
#     return predicted_decisions

# def compare_decisions(original_decisions, predicted_decisions):
#     """Compare original and predicted decisions"""
#     if len(original_decisions) != len(predicted_decisions):
#         print(f"Error: Different number of decisions: Original={len(original_decisions)}, Predicted={len(predicted_decisions)}")
#         return False
    
#     correct_count = 0
#     for i in range(len(original_decisions)):
#         if original_decisions[i] == predicted_decisions[i]:
#             correct_count += 1
    
#     accuracy = correct_count / len(original_decisions) * 100
#     print(f"Accuracy: {accuracy:.2f}% ({correct_count}/{len(original_decisions)} correct)")
    
#     if correct_count == len(original_decisions):
#         print("The mined policy perfectly reproduces the original decisions.")
#     else:
#         print("There are discrepancies between the original decisions and the mined policy.")
        
#         # Show incorrect predictions
#         incorrect_indices = [i for i in range(len(original_decisions)) if original_decisions[i] != predicted_decisions[i]]
#         print(f"Incorrect predictions at indices: {incorrect_indices}")
        
#         for idx in incorrect_indices[:5]:  # Show up to 5 incorrect predictions
#             print(f"Entry {idx}: Original={original_decisions[idx]}, Predicted={predicted_decisions[idx]}")
    
#     return accuracy

# def main():
#     # File paths
#     access_data_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\healthcare_access_decisions.txt"
#     rules_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\rules_stollers.txt"
    
#     # Parse access data and rules
#     access_data = parse_access_data(access_data_path)
#     rules = parse_rules(rules_path)
    
#     # Extract original decisions (last element of each row)
#     original_decisions = [entry[-1] for entry in access_data]
    
#     # Apply rules to predict decisions
#     predicted_decisions = apply_rules(access_data, rules)
    
#     # Compare original and predicted decisions
#     accuracy = compare_decisions(original_decisions, predicted_decisions)
    
#     # Write results to file
#     results_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\comparison_results.txt"
#     with open(results_path, "w") as file:
#         file.write(f"Total entries: {len(original_decisions)}\n")
#         file.write(f"Correctly predicted: {sum(1 for i in range(len(original_decisions)) if original_decisions[i] == predicted_decisions[i])}\n")
#         file.write(f"Accuracy: {accuracy:.2f}%\n\n")
        
#         file.write("Detailed comparison:\n")
#         for i in range(len(original_decisions)):
#             file.write(f"Entry {i}: Original={original_decisions[i]}, Predicted={predicted_decisions[i]}, " + 
#                       f"{'Correct' if original_decisions[i] == predicted_decisions[i] else 'Incorrect'}\n")
    
#     print(f"Results written to {results_path}")

# if __name__ == "__main__":
#     main()

"""
Updated comparison script for healthcare dataset with variable-length rows
Outputs original and predicted matrices to separate files
"""
import ast
import json
import pandas as pd
import numpy as np

# Define attributes
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

def parse_rules(file_path):
    """Parse policy rules from file"""
    rules = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    rule_entry = ast.literal_eval(line)
                    rules.append(rule_entry)
                except (SyntaxError, ValueError) as e:
                    print(f"Error parsing rule: {line}")
                    print(f"Error details: {e}")
    return rules

def get_attribute_value(entry, attribute_index):
    """Safely get attribute value, handling variable-length entries"""
    if attribute_index < len(entry) - 1:  # -1 to account for decision at the end
        return entry[attribute_index]
    return "N/A"  # Default value for missing attributes

def satisfies_rule(rule, entry):
    """Check if an entry satisfies a rule"""
    for attribute, value in rule:
        attr_index = attributes.index(attribute)
        entry_value = get_attribute_value(entry, attr_index)
        
        if entry_value != value and value != '*':
            return False
    return True

def apply_rules(access_data, rules):
    """Apply rules to predict decisions"""
    predicted_decisions = []
    rule_matches = []  # Track which rule matched for each entry
    
    for entry in access_data:
        # Default is 0 (deny)
        decision = 0
        matched_rule_index = -1
        
        for i, rule_entry in enumerate(rules):
            if satisfies_rule(rule_entry['rule'], entry):
                if rule_entry['decision'] == 'permit':
                    decision = 1
                    matched_rule_index = i
                    break  # Permit takes precedence if matched
                elif rule_entry['decision'] == 'deny':
                    decision = 0
                    matched_rule_index = i
                    # Don't break, continue checking other rules
        
        predicted_decisions.append(decision)
        rule_matches.append(matched_rule_index)
    
    return predicted_decisions

def compare_decisions(original_decisions, predicted_decisions):
    """Compare original and predicted decisions"""
    if len(original_decisions) != len(predicted_decisions):
        print(f"Error: Different number of decisions: Original={len(original_decisions)}, Predicted={len(predicted_decisions)}")
        return False
    
    correct_count = 0
    for i in range(len(original_decisions)):
        if original_decisions[i] == predicted_decisions[i]:
            correct_count += 1
    
    accuracy = correct_count / len(original_decisions) * 100
    print(f"Accuracy: {accuracy:.2f}% ({correct_count}/{len(original_decisions)} correct)")
    
    if correct_count == len(original_decisions):
        print("The mined policy perfectly reproduces the original decisions.")
    else:
        print("There are discrepancies between the original decisions and the mined policy.")
        
        # Show incorrect predictions
        incorrect_indices = [i for i in range(len(original_decisions)) if original_decisions[i] != predicted_decisions[i]]
        print(f"Incorrect predictions at indices: {incorrect_indices}")
        
        for idx in incorrect_indices[:5]:  # Show up to 5 incorrect predictions
            print(f"Entry {idx}: Original={original_decisions[idx]}, Predicted={predicted_decisions[idx]}")
    
    return accuracy

def create_matrix_representation(access_data, decisions):
    """Create a structured matrix representation from the access data and decisions"""
    # Create a DataFrame to organize data
    matrix_data = []
    
    for i, entry in enumerate(access_data):
        # Create a row with all available attribute values and the decision
        row_data = {}
        for j, attr in enumerate(attributes):
            if j < len(entry) - 1:  # Skip the decision at the end of entry
                row_data[attr] = entry[j]
            else:
                row_data[attr] = "N/A"
        
        # Add the decision (original or predicted)
        row_data["decision"] = decisions[i]
        matrix_data.append(row_data)
    
    return pd.DataFrame(matrix_data)

def export_matrices(access_data, original_decisions, predicted_decisions):
    """Export original and predicted matrices to files"""
    # Create matrix representations
    original_matrix = create_matrix_representation(access_data, original_decisions)
    predicted_matrix = create_matrix_representation(access_data, predicted_decisions)
    
    # # Export as CSV
    # original_matrix_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\original_matrix.csv"
    # predicted_matrix_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\predicted_matrix.csv"
    
    # original_matrix.to_csv(original_matrix_path, index=False)
    # predicted_matrix.to_csv(predicted_matrix_path, index=False)
    
    # Export as formatted text (more readable)
    original_matrix_txt_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\original_matrix.txt"
    predicted_matrix_txt_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\predicted_matrix.txt"
    
    with open(original_matrix_txt_path, "w") as f:
        f.write("=== ORIGINAL MATRIX ===\n\n")
        f.write(original_matrix.to_string())
    
    with open(predicted_matrix_txt_path, "w") as f:
        f.write("=== PREDICTED MATRIX ===\n\n")
        f.write(predicted_matrix.to_string())
    
    # # Export as JSON for programmatic access
    # original_matrix_json_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\original_matrix.json"
    # predicted_matrix_json_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\predicted_matrix.json"
    
    # original_matrix.to_json(original_matrix_json_path, orient="records", indent=2)
    # predicted_matrix.to_json(predicted_matrix_json_path, orient="records", indent=2)
    
    return {
        # "original_csv": original_matrix_path,
        # "predicted_csv": predicted_matrix_path,
        "original_txt": original_matrix_txt_path,
        "predicted_txt": predicted_matrix_txt_path,
        # "original_json": original_matrix_json_path,
        # "predicted_json": predicted_matrix_json_path
    }

def main():
    # File paths
    access_data_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\healthcare_access_decisions.txt"
    rules_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\rules_stollers.txt"
    
    # Parse access data and rules
    access_data = parse_access_data(access_data_path)
    rules = parse_rules(rules_path)
    
    # Extract original decisions (last element of each row)
    original_decisions = [entry[-1] for entry in access_data]
    
    # Apply rules to predict decisions
    predicted_decisions = apply_rules(access_data, rules)
    
    # Compare original and predicted decisions
    accuracy = compare_decisions(original_decisions, predicted_decisions)
    
    # Export matrices to files
    matrix_files = export_matrices(access_data, original_decisions, predicted_decisions)
    
    # Write results to file
    # results_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\comparison_results.txt"
    # with open(results_path, "w") as file:
    #     file.write(f"Total entries: {len(original_decisions)}\n")
    #     file.write(f"Correctly predicted: {sum(1 for i in range(len(original_decisions)) if original_decisions[i] == predicted_decisions[i])}\n")
    #     file.write(f"Accuracy: {accuracy:.2f}%\n\n")
        
    #     file.write("Detailed comparison:\n")
    #     for i in range(len(original_decisions)):
    #         file.write(f"Entry {i}: Original={original_decisions[i]}, Predicted={predicted_decisions[i]}, " + 
    #                   f"{'Correct' if original_decisions[i] == predicted_decisions[i] else 'Incorrect'}\n")
        
    #     file.write("\n=== MATRIX FILES ===\n")
    #     file.write(f"Original matrix (CSV): {matrix_files['original_csv']}\n")
    #     file.write(f"Predicted matrix (CSV): {matrix_files['predicted_csv']}\n")
    #     file.write(f"Original matrix (TXT): {matrix_files['original_txt']}\n")
    #     file.write(f"Predicted matrix (TXT): {matrix_files['predicted_txt']}\n")
    #     file.write(f"Original matrix (JSON): {matrix_files['original_json']}\n")
    #     file.write(f"Predicted matrix (JSON): {matrix_files['predicted_json']}\n")
    
    # print(f"Results written to {results_path}")
    print(f"Original matrix written to {matrix_files['original_txt']}")
    print(f"Predicted matrix written to {matrix_files['predicted_txt']}")

if __name__ == "__main__":
    main()
    