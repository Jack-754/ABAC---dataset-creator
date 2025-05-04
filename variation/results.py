import subprocess
import re
import os

# Parameters to vary
parameters = {
    "Enter size of Subject": [100, 150, 200, 250, 300, 350, 400, 450, 500, 550],
    "Enter size of Object": [200, 250, 300, 350, 400, 450, 500, 550, 600, 650],
    "Enter size of Environment": [4, 8, 12, 16, 20, 24, 28, 32, 36, 40],
    "Enter number of attributes for each Subject": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30],
    "Enter number of attributes for each Object": [4, 8, 12, 16, 20, 24, 28, 32, 36, 40],
    "Enter number of attributes for each Environment": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30],
    "Enter the number of rules": [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
}

template_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\input_template.txt"
input_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\input.txt"
rules_path = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation\rules.txt"
base_dir = r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\variation"

for param, values in parameters.items():
    results = []
    print(f"Varying parameter: {param}")
    for value in values:
        # Read and modify template
        with open(template_path, "r") as f:
            content = f.read()

        content = re.sub(rf"{re.escape(param)}\s*:\s*.*", f"{param} : {value}", content)

        with open(input_path, "w") as f:
            f.write(content)

        # Run pipeline
        subprocess.run(["python", os.path.join(base_dir, "input.py")])
        subprocess.run(["python", os.path.join(base_dir, "gen.py")])
        subprocess.run(["python", os.path.join(base_dir, "policy_mining.py")])

        # Count rules
        with open(rules_path, "r") as f:
            rule_count = sum(1 for line in f if line.strip())

        results.append((value, rule_count))

    # Save results
    file_safe_param = param.split()[3].lower()  # e.g., subject/object/environment/etc.
    output_csv = os.path.join(base_dir, f"results_vary_{file_safe_param}.csv")
    with open(output_csv, "w") as f:
        f.write(f"{file_safe_param},RulesGenerated\n")
        for value, count in results:
            f.write(f"{value},{count}\n")

    print(f"Saved results to {output_csv}")
