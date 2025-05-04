import re

def parse_file(file_content):
    """Parse the ABAC policy file to extract user attributes, resource attributes, and rules."""
    lines = file_content.split('\n')
    
    user_attributes = {}
    resource_attributes = {}
    rules = []
    
    for line in lines:
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        # Parse user attributes
        user_match = re.match(r'userAttrib\((\w+),\s*(.*)\)', line)
        if user_match:
            user_id = user_match.group(1)
            attrs_str = user_match.group(2)
            
            # Extract attribute-value pairs
            attrs = {}
            attrs_parts = re.findall(r'(\w+)=(\{[^}]*\}|\w+)', attrs_str)
            for attr, val in attrs_parts:
                # Handle sets like {oncology pediatrics}
                if val.startswith('{') and val.endswith('}'):
                    val = val[1:-1].split()
                attrs[attr] = val
            
            user_attributes[user_id] = attrs
            continue
        
        # Parse resource attributes
        resource_match = re.match(r'resourceAttrib\((\w+),\s*(.*)\)', line)
        if resource_match:
            resource_id = resource_match.group(1)
            attrs_str = resource_match.group(2)
            
            # Extract attribute-value pairs
            attrs = {}
            attrs_parts = re.findall(r'(\w+)=(\{[^}]*\}|\w+)', attrs_str)
            for attr, val in attrs_parts:
                # Handle sets like {oncology}
                if val.startswith('{') and val.endswith('}'):
                    val = val[1:-1].split()
                attrs[attr] = val
            
            resource_attributes[resource_id] = attrs
            continue
        
        # Parse rules
        rule_match = re.match(r'rule\((.*?);\s*(.*?);\s*\{(.*?)\};\s*(.*?)\)', line)
        if rule_match:
            user_cond = rule_match.group(1).strip()
            res_cond = rule_match.group(2).strip()
            action = rule_match.group(3).strip()
            constraint = rule_match.group(4).strip()
            
            rules.append({
                'user_condition': user_cond,
                'resource_condition': res_cond,
                'action': action,
                'constraint': constraint
            })
    
    return user_attributes, resource_attributes, rules

def check_user_condition(user_attrs, condition):
    """Check if user attributes satisfy the condition."""
    if not condition:
        return True
    
    # Handle position in {nurse} condition
    position_match = re.search(r'position\s+in\s+\{(.*?)\}', condition)
    if position_match:
        positions = position_match.group(1).split()
        if 'position' not in user_attrs or user_attrs['position'] not in positions:
            return False
    
    return True

def check_resource_condition(res_attrs, condition):
    """Check if resource attributes satisfy the condition."""
    if not condition:
        return True
    
    conditions = condition.split(',')
    for cond in conditions:
        cond = cond.strip()
        
        # Handle type in {HRitem} condition
        type_match = re.search(r'type\s+in\s+\{(.*?)\}', cond)
        if type_match:
            types = type_match.group(1).split()
            if 'type' not in res_attrs or res_attrs['type'] not in types:
                return False
        
        # Handle topics supseteqln {{nursing}} condition
        topics_match = re.search(r'topics\s+supseteqln\s+\{\{(.*?)\}\}', cond)
        if topics_match:
            required_topic = topics_match.group(1)
            if 'topics' not in res_attrs:
                return False
            if isinstance(res_attrs['topics'], list):
                if required_topic not in res_attrs['topics']:
                    return False
            else:
                if required_topic != res_attrs['topics']:
                    return False
    
    return True

def check_constraint(user_id, user_attrs, res_attrs, constraint):
    """Check if the user-resource pair satisfies the constraint."""
    # Handle ward=ward constraint
    if constraint == 'ward=ward':
        if 'ward' not in user_attrs or 'ward' not in res_attrs:
            return False
        return user_attrs['ward'] == res_attrs['ward']
    
    # Handle teams ] treatingTeam constraint
    elif constraint == 'teams ] treatingTeam':
        if 'teams' not in user_attrs or 'treatingTeam' not in res_attrs:
            return False
        if isinstance(user_attrs['teams'], list):
            return res_attrs['treatingTeam'] in user_attrs['teams']
        return user_attrs['teams'] == res_attrs['treatingTeam']
    
    # Handle uid=patient constraint
    elif constraint == 'uid=patient':
        if 'patient' not in res_attrs:
            return False
        return user_id == res_attrs['patient']
    
    # Handle agentFor ] patient constraint
    elif constraint == 'agentFor ] patient':
        if 'agentFor' not in user_attrs or 'patient' not in res_attrs:
            return False
        if isinstance(user_attrs['agentFor'], list):
            return res_attrs['patient'] in user_attrs['agentFor']
        return user_attrs['agentFor'] == res_attrs['patient']
    
    # Handle uid=author constraint
    elif constraint == 'uid=author':
        if 'author' not in res_attrs:
            return False
        return user_id == res_attrs['author']
    
    # Handle specialties > topics, teams ] treatingTeam constraint
    elif constraint == 'specialties > topics, teams ] treatingTeam':
        if 'specialties' not in user_attrs or 'topics' not in res_attrs or 'teams' not in user_attrs or 'treatingTeam' not in res_attrs:
            return False
        
        # Check if any specialty matches any topic
        specialties = user_attrs['specialties'] if isinstance(user_attrs['specialties'], list) else [user_attrs['specialties']]
        topics = res_attrs['topics'] if isinstance(res_attrs['topics'], list) else [res_attrs['topics']]
        
        specialty_match = any(spec in topics for spec in specialties)
        
        # Check if treating team is in user's teams
        teams = user_attrs['teams'] if isinstance(user_attrs['teams'], list) else [user_attrs['teams']]
        team_match = res_attrs['treatingTeam'] in teams
        
        return specialty_match and team_match
    
    return False

def evaluate_rule(user_id, user_attrs, res_attrs, action, rule):
    """Evaluate if a rule applies for a given user, resource, and action."""
    # Check user condition
    if not check_user_condition(user_attrs, rule['user_condition']):
        return False
    
    # Check resource condition
    if not check_resource_condition(res_attrs, rule['resource_condition']):
        return False
    
    # Check if the action matches
    if action != rule['action']:
        return False
    
    # Check constraint
    if not check_constraint(user_id, user_attrs, res_attrs, rule['constraint']):
        return False
    
    return True

def generate_access_decisions(user_attributes, resource_attributes, rules):
    """Generate access decisions for all user-resource-action combinations."""
    actions = ['read', 'addItem', 'addNote']
    results = []
    
    for user_id, user_attrs in user_attributes.items():
        for res_id, res_attrs in resource_attributes.items():
            for action in actions:
                # Initialize access decision as 0 (denied)
                access_decision = 0
                
                # Check all rules
                for rule in rules:
                    if evaluate_rule(user_id, user_attrs, res_attrs, action, rule):
                        access_decision = 1
                        break
                
                # Create attribute dictionary for this combination
                attrs = {
                    'user': user_id,
                    'resource': res_id,
                    'action': action
                }
                
                # Add user attributes with prefix
                for attr, val in user_attrs.items():
                    if isinstance(val, list):
                        attrs[f'user_{attr}'] = ','.join(val)
                    else:
                        attrs[f'user_{attr}'] = val
                
                # Add resource attributes with prefix
                for attr, val in res_attrs.items():
                    if isinstance(val, list):
                        attrs[f'resource_{attr}'] = ','.join(val)
                    else:
                        attrs[f'resource_{attr}'] = val
                
                # Add access decision
                attrs['access_decision'] = access_decision
                
                results.append(attrs)
    
    return results

def format_output(results):
    """Format results into the required output format."""
    output_lines = []
    
    for result in results:
        # Extract access_decision
        access_decision = result.pop('access_decision')
        
        # Format the remaining attributes
        attrs_str = ', '.join([f"{attr} = {val}" for attr, val in result.items()])
        
        # Add access_decision at the end
        output_line = f"{attrs_str}, access_decision = {access_decision}"
        output_lines.append(output_line)
    
    return '\n'.join(output_lines)

def convert_abac_to_required_format(file_content):
    """Convert ABAC policy to required format."""
    user_attributes, resource_attributes, rules = parse_file(file_content)
    access_decisions = generate_access_decisions(user_attributes, resource_attributes, rules)
    output = format_output(access_decisions)
    return output

# Example usage
def main():
    # Read the file content
    with open(r'C:\Users\Sathya\OneDrive\Desktop\BTP\spring_sem\stollers_dataset\healthcare.abac', 'r') as f:
        file_content = f.read()
    
    # Convert to required format
    output = convert_abac_to_required_format(file_content)
    
    # Write the output to a file
    with open('temp_healthcare_access_decisions.txt', 'w') as f:
        f.write(output)
    
    print(f"Conversion complete. Output written to healthcare_access_decisions.txt")
    # print(f"Generated {output.count(chr(10)) + 1} access decision entries")

if __name__ == "__main__":
    main()