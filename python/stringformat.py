# Helpers
header = "=" * 80
emptyline = ""
print(header)

# F-String 
fstring = f"F-String (>= Python 3.6)"
print(fstring)
name = "Barča"
age = 13
str1 = f"{{name}} = {name}"
str2 = f"{{age}} = {age}"
print(str1)
print(str2)
print(emptyline)

# Formatted String 
print("Formatted Strings ( < 3.6 )")
str1 = "Var replacement: {{name}} = {name} {{age}} = {age}".format(name = name, age = age)
str2 = "Num replacement: {{0}} = {0}, {{1}} = {1}".format(name,age)
str3 = "Brace replacement: {{}} =  {}, {{}} = {}".format(name,age)
print(str1)
print(str2)
print(str3)
print(emptyline)

# Tuple replacement (2+)
print("Tuple Replacement")
str1 = "Name: %s, Age: %d" % (name, age)
print(str1)