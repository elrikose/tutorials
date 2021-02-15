# decorator function to convert to lowercase
def lowercase(function):
    def wrapper():
        func = function()
        string_lowercase = func.lower()
        return string_lowercase
    return wrapper

# decorator function to split words
def splitter(function):
    def wrapper():
        func = function()
        string_split = func.split()
        return string_split
    return wrapper

@splitter	# this is executed next
@lowercase	# this is executed first
def hello():
    return 'Hello World'

print(hello())