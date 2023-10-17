import os
import re

# Initialize the directory name
dstools_dir = 'dstools'

# Find all the import statements in the original file
with open('dstools.py', 'r') as file:
    content = file.read()

# Regular expressions to match Python import statements
import_pattern = r'^(import .*|from .* import .*)'

# Get all import statements
imports = re.findall(import_pattern, content, re.MULTILINE)

# Write the import statements to each new file
for file_name in os.listdir(dstools_dir):
    with open(os.path.join(dstools_dir, file_name), 'r+') as file:
        file_content = file.read()
        file.seek(0, 0)
        file.write(''.join(imports) + '\n' + file_content)

# Write the import statements to __init__.py
with open(os.path.join(dstools_dir, '__init__.py'), 'w') as file:
    file.writelines(imports)

#print('Import statements have been written to all new files and __init__.py').writelines(extracted_func)
