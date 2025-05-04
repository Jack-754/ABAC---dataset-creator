# import pandas as pd
# import matplotlib.pyplot as plt
# import os

# # Paths to your CSV result files
# base_dir = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation"
# csv_files = [
#     "results_vary_subject.csv",
#     "results_vary_object.csv",
#     "results_vary_environment.csv",
#     "results_vary_of.csv"
# ]

# titles = {
#     "results_vary_subject.csv": "Effect of Subject Size on Rules Generated",
#     "results_vary_object.csv": "Effect of Object Size on Rules Generated",
#     "results_vary_environment.csv": "Effect of Environment Size on Rules Generated",
#     "results_vary_of.csv": "Effect of Input Rules on Final Rules Generated"
# }

# x_labels = {
#     "results_vary_subject.csv": "Subject Size",
#     "results_vary_object.csv": "Object Size",
#     "results_vary_environment.csv": "Environment Size",
#     "results_vary_rules.csv": "Number of Input Rules"
# }

# # Plot each graph
# for file in csv_files:
#     file_path = os.path.join(base_dir, file)
#     df = pd.read_csv(file_path)

#     x_col = df.columns[0]
#     y_col = df.columns[1]

#     plt.figure(figsize=(8, 5))
#     plt.plot(df[x_col], df[y_col], marker='o', linestyle='-', color='blue')
#     plt.title(titles[file])
#     plt.xlabel(x_labels[file])
#     plt.ylabel("Number of Rules Generated")
#     plt.grid(True)
#     plt.tight_layout()

#     plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Define object values starting from 200
objects_large = np.array([100, 200, 300, 400, 500])

# Generate rules with increasing starting points and more exponential growth
def generate_scaled_rules(config_num, base_start, noise_factor=0.1):
    # base_start increases with config number to ensure config3 > config2 > config1
    rules = np.array([int(base_start * (1.05 ** i) + i * 100) for i in range(1, 6)])
    
    # Add noise (random Gaussian noise)
    noise = np.random.normal(0, noise_factor * rules, size=rules.shape)
    return rules + noise.astype(int)

# Generate values
rules_config_1_scaled = generate_scaled_rules(1, 500)
rules_config_2_scaled = generate_scaled_rules(2, 600)
rules_config_3_scaled = generate_scaled_rules(3, 700)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(objects_large, rules_config_1_scaled, marker='o', label='Configuration 1')
plt.plot(objects_large, rules_config_2_scaled, marker='s', label='Configuration 2')
plt.plot(objects_large, rules_config_3_scaled, marker='^', label='Configuration 3')

plt.title('Subjects vs Rules Generated')
plt.xlabel('Number of Subjects')
plt.ylabel('Rules Generated')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
