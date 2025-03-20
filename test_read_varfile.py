import re

def parse_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Use regex to match the variable name and value
            match = re.match(r'(\w+)\s*=\s*"(.*)"', line.strip())
            if match:
                config[match.group(1)] = match.group(2)
    return config

# Path to your config file
config_file = 'config.txt'

# Parse the config file
config = parse_config(config_file)

# Now you can access the variables like this:
var1 = config.get('var1')
var2 = config.get('var2')
var3 = config.get('var3')

# Example usage
print(f"var1: {var1}")
print(f"var2: {var2}")
print(f"var3: {var3}")

# You can now use var1, var2, var3 in your calculations and decisions