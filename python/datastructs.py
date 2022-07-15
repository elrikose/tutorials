# Helpers
header = "=" * 80
emptyline = ""
print(header)

# Dict
dict = { }
print(f"{type(dict)}: {dict}")

dict.update({ "1": 1, "2": 2})
print(f"add 1 and 2: {dict}")

dict["3"] = 3
dict["4"] = 4
print(f"add 3 and 4: {dict}")

dict.clear()
print(f"clear: {dict}")
print(emptyline)

# List
list = []
print(f"{type(list)}: {list}")

list1 = [1, 2, 3]
print(f"list1: {list1}")

list2 = [4, 5, 6]
print(f"list2: {list2}")

list3 = list1 + list2
print(f"add list1 and list2: {list3}")

# Values are strings on purpose
list3.append("7")
print(f"append 7: {list3}")

list3.remove("7")
print(f"remove 7: {list3}")

list3.insert(6, "7")
print(f"insert 7 at 6: {list3}")

list1.extend(list2)
print(f"extend list2: {list1}")

index = list1.index(5)
print(f"5 is at index: {index}")

list1.extend(list3)
print(f"extend list3: {list1}")

list1.pop(0)
print(f"pop 0: {list1}")

list1.clear()
print(f"clear(): {list1}")

reversed_list = list3[::-1]
print(f"reversed_list: {reversed_list}")
print(emptyline)

# Tuple
empty_tuple = ()
print(f"{type(empty_tuple)}: {empty_tuple}")

tup = ('1', '2', '3')
print(f"{type(tup)}: {tup}")

num_threes = tup.count('3')
print(f"count() of '3': {num_threes}")

index_of_three = tup.index('3')
print(f"index() of '3': {index_of_three}")

print(emptyline)


# Set
set = set()
print(f"{type(set)}: {set}")

set.add(1)
print(f"ad: {set}") # output: {1}

set.update([1, 2, 3])
print(f"update: {set}") # output: {1, 2, 3}

set.update({4, 5, 6})
print(f"update 2: {set}") # output: {1, 2, 3, 4, 5, 6}

set.clear()
print(f"clear(): {set}")

print(f"{set.issuperset({1, 2, 3})}") # output: True
print(f"{set.issuperset({1, 2, 10})}") # output: False

is_subset = {1, 2, 3}.issubset(set)
print(f"issubset(): {is_subset}") # output: True
is_subset = {1, 2, 10}.issubset(set)
print(f"issubset(): {is_subset}") # output: False



print(emptyline)

def group_by_owners(files):
    dict = {}
    for (key, value) in files.items():
        if value in dict:
            list = dict[value]
            print(list)
            list.append(key)
            dict[value] = list
        else:
            dict[value] = [ key ]
    return dict

files = {
    'Input.txt': 'Randy',
    'Code.py': 'Stan',
    'Output.txt': 'Randy'
}
print(group_by_owners(files))
