# Helpers
header = "=" * 80
emptyline = ""
print(header)

# Dict
dict = { }
print(f"{type(dict)}: {dict}")
print(emptyline)

# List
list = []
print(f"{type(list)}: {list}")

list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = list1 + list2
print(f"{type(list1)}: {list3}")
print(emptyline)

reversed_list = list3[::-1]
print(f"{type(reversed_list)}: {reversed_list}")

# Tuple
tuple = ()
print(f"{type(tuple)}: {tuple}")
print(emptyline)

# Set
set = set()
print(f"{type(set)}: {set}")
print(emptyline)

