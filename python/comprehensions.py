list = [1, 2, 3, 5, 7, 11]

# list comprehension
squared_list = [x**2 for x in list]
print(squared_list) # output: [1, 4, 9, 25, 49, 121]

# list comprehension with conditional
squared_list = [x**2 for x in list if x < 10]
print(squared_list) # output: [1, 4, 9, 25, 49]


# dict comprehension
squared_dict = {x:x**2 for x in list} 
print(squared_dict) # output: {1: 1, 2: 4, 3: 9, 5: 25, 7: 49, 11: 121}

# dict comprehension with conditional
squared_dict = {x:x**2 for x in list if x < 10}
print(squared_dict) # output: {1: 1, 2: 4, 3: 9, 5: 25, 7: 49}


# Join two lists by zip
list1 = [1, 2, 3, 4, 5, 6]
list2 = [7, 8, 9, 10, 11, 12]

added_list = [x+y for (x, y) in zip(list1, list2)]
multiplied_list = [x*y for (x, y) in zip(list1, list2)]

print(added_list) # output: [8, 10, 12, 14, 16, 18]
print(multiplied_list) # output: [7, 16, 27, 40, 55, 72]