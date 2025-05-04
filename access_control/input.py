import configparser

def write_config_file(n1, n2, n3, n4, n5, n6, subject_attributes, object_attributes, environment_attributes, N):
    config = configparser.ConfigParser()
    
    config['NUMBERS'] = {
        'n1': str(n1), 'n2': str(n2), 'n3': str(n3),
        'n4': str(n4), 'n5': str(n5), 'n6': str(n6)
    }
    
    config['SUBJECT_ATTRIBUTES'] = {'values': ','.join(map(str, subject_attributes))}
    config['OBJECT_ATTRIBUTES'] = {'values': ','.join(map(str, object_attributes))}
    config['ENVIRONMENT_ATTRIBUTES'] = {'values': ','.join(map(str, environment_attributes))}

    config['RULES'] = {'N': str(N)}
    
    with open(r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\access_control\config.ini", 'w') as configfile:
        config.write(configfile)

def read_input_file():
    with open(r"C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\access_control\input.txt", "r") as file:
        lines = file.readlines()
        return lines

def extract_value_after_colon(line):
    return line.split(":")[1].strip()

def read_attributes(lines):
    n1, n2, n3 = map(int, [extract_value_after_colon(line) for line in lines[:3]])
    
    n4, n5, n6 = map(int, [extract_value_after_colon(line) for line in lines[4:7]])
    
    return n1, n2, n3, n4, n5, n6

def read_n4_attributes(lines, n4):
    values = list(map(int, extract_value_after_colon(lines[8]).split(", ")))
    if len(values) != n4:
        raise ValueError(f"Expected {n4} values for Subject Attributes, but got {len(values)}")
    return values

def read_n5_attributes(lines, n5):
    values = list(map(int, extract_value_after_colon(lines[9]).split(", ")))
    if len(values) != n5:
        raise ValueError(f"Expected {n5} values for Object Attributes, but got {len(values)}")
    return values

def read_n6_attributes(lines, n6):
    values = list(map(int, extract_value_after_colon(lines[10]).split(", ")))
    if len(values) != n6:
        raise ValueError(f"Expected {n6} values for Environment Attributes, but got {len(values)}")
    return values

def read_no_of_rules(lines):
    N = int(extract_value_after_colon(lines[12]))
    return N


if __name__ == "__main__":
    lines = read_input_file()
    
    n1, n2, n3, n4, n5, n6 = read_attributes(lines)

    subject_attributes = read_n4_attributes(lines, n4)
    object_attributes = read_n5_attributes(lines, n5)
    environment_attributes = read_n6_attributes(lines, n6)

    N = read_no_of_rules(lines)

    write_config_file(n1, n2, n3, n4, n5, n6, subject_attributes, object_attributes, environment_attributes, N)
