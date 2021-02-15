
# Helpers
header = "=" * 80
emptyline = ""
print(header)

# String reverse
str = "Always look on the bright side of life."
str2 = str[::-1]
print(f"Reverse: {str} ==> {str2}")
print(emptyline)

# String lower/upper
lower = str.lower()
upper = str.upper()
print(f"Lower: {str} ==> {lower}")
print(f"Upper: {str} ==> {upper}")
print(emptyline)

# String find index
index = str.find("bright")
print(f"Position: {index}")
print(emptyline)

# Remove string from string
str2 = str.replace("bright", "")
print(f"Remove string: {str}")
print(f"Remove string: {str2}")
print(emptyline)

# Single versus double quotes
single = 'Monty'
double = "Python"
single_inside_double = "'Monty' Python"
double_inside_single = 'Monty "Python"'
single_inside_single = '\'Monty\' Python'
double_inside_double = "Monty \"Python\""
print(f"Single: {single}")
print(f"Double: {double}")
print(f"Single in double: {single_inside_double}")
print(f"Double in single: {double_inside_single}")
print(emptyline)
print(f"Single in single: {single_inside_single}")
print(f"Double in double: {double_inside_double}")
print(emptyline)

# Split / Join
list = str.split()
print(list)
str2 = ' '.join(list)
print(str2)
print(emptyline)