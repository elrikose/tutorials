
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

# Split lines
str = "This is line 1\nThis is line 2\nThis is line 3\n"
lines = str.splitlines()
print(f"splitlines: {len(lines)} = {lines}")
lines = str.split("\n")
print(f"split: {len(lines)} = {lines}")

# Whitespace
import string
print(f"Whitespace {string.whitespace}")

"""
capitalize()	Converts the first character to upper case
casefold()	Converts string into lower case
center()	Returns a centered string
count()	Returns the number of times a specified value occurs in a string
encode()	Returns an encoded version of the string
endswith()	Returns true if the string ends with the specified value
find()	Searches the string for a specified value and returns the position of where it was found
format()	Formats specified values in a string
index()	Searches the string for a specified value and returns the position of where it was found
isalnum()	Returns True if all characters in the string are alphanumeric
isalpha()	Returns True if all characters in the string are in the alphabet
isdecimal()	Returns True if all characters in the string are decimals
isdigit()	Returns True if all characters in the string are digits
isidentifier()	Returns True if the string is an identifier
islower()	Returns True if all characters in the string are lower case
isnumeric()	Returns True if all characters in the string are numeric
isprintable()	Returns True if all characters in the string are printable
isspace()	Returns True if all characters in the string are whitespaces
istitle()	Returns True if the string follows the rules of a title
isupper()	Returns True if all characters in the string are upper case
join()	Joins the elements of an iterable to the end of the string
ljust()	Returns a left justified version of the string
lower()	Converts a string into lower case
lstrip()	Returns a left trim version of the string
maketrans()	Returns a translation table to be used in translations
partition()	Returns a tuple where the string is parted into three parts
replace()	Returns a string where a specified value is replaced with a specified value
rfind()	Searches the string for a specified value and returns the last position of where it was found
rindex()	Searches the string for a specified value and returns the last position of where it was found
rjust()	Returns a right justified version of the string
rsplit()	Splits the string at the specified separator, and returns a list
rstrip()	Returns a right trim version of the string
split()	Splits the string at the specified separator, and returns a list
splitlines()	Splits the string at line breaks and returns a list
startswith()	Returns true if the string starts with the specified value
strip()	Returns a trimmed version of the string
title()	Converts the first character of each word to upper case
translate()	Returns a translated string
upper()	Converts a string into upper case
zfill()
"""

"""
def string_sort(str):
  return sorted(str)

def is_permutation(str1, str2):
  return (string_sort(str1) == string_sort(str2))

if __name__ == "__main__":
  str1 = "The quick brown fox jumped over the lazy dog's back"
  str2 = "The quick brown fox jumped."

  if (is_permutation(str1, str1)):
     print("The two strings are equal")
  else:
     print("The two strings are NOT equal")
"""