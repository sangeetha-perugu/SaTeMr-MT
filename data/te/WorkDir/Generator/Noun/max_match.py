import os.path

# List of strings
strings = ["apple", "appletree", "application", "apricot"]

# Find the longest common prefix
prefix = os.path.commonprefix(strings)

print(prefix)