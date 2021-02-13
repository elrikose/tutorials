
# Helpers
header = "=" * 80
emptyline = ""
print(header)

def emptyfunc():
  print(f"emptyfunc()")

def singlefunc(param):
  print(f"singlefunc({param})")

if __name__ == "__main__":
  emptyfunc()
  singlefunc(1)
  singlefunc(['123', '456', '789'])
  singlefunc({'a':'123', 'b':'456', 'c':'789'})

