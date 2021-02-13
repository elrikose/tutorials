import argparse

# Example invocations
#   python3 args.py -h
#   python3 args.py 1
#   python3 args.py 1
#   python3 args.py 1 2
#   python3 args.py 1 2 3 red 1
#   python3 args.py -a0 1 2 3 red 1
#   python3 args.py -a1 1 1 2 3 red 1
#   python3 args.py -a2 yes 1 2 3 red 1
#   python3 args.py -a0 -a1 5 -a2 yes 1 2 3 red 1

# HT: https://medium.com/swlh/python-argparse-by-example-a530eb55ced9

def argstester(*args, **kwargs):
  print(f"args  : {args}")
  print(f"kwargs: {kwargs}")

if __name__ == "__main__":
  # Parse arguments
  parser = argparse.ArgumentParser(description='argparser')

  # Cast the input to string, int or float type 
  parser.add_argument(dest='string', type=str, help="A string argument", nargs='?')
  parser.add_argument(dest='int', type=int, help="An integer argument", nargs='?')
  parser.add_argument(dest='float', type=float, help="A float argument", nargs='?')

  # Validate that the input is in specified list
  parser.add_argument(dest='choice', choices=['red', 'green', 'blue'], nargs='?')

  # Optional positional argument (length 0 or 1)
  parser.add_argument(dest='optional', nargs='?')

  # Boolean flag (does not accept input data), with default value
  parser.add_argument('-a0', action="store_true", default=False)

  # Cast input to integer, with a default value
  parser.add_argument('-a1', type=int, default=1)

  # Provide long form name as well (maps to 'argument2' not 'a2')
  parser.add_argument('-a2', '--argument2', type=str, default="2")

  # Make argument mandatory
  # parser.add_argument('-a4', required=True)

  # Retur the input via different parameter name
  parser.add_argument('-a4', '--argument4', dest='my_arg')

  args = parser.parse_args()

  argstester(args.string, args.int, args.float, args.choice, args.optional, args.a0, args.a1, args.argument2, test='123', test2='456')
