import random

def randomized_list(num_items):
  list = set()

  for i in range(num_items): 
    rand_num = None

    # Make sure there are no conflicts
    while ((rand_num == None) or (rand_num in list)):
      rand_num = int(random.random() * num_items)

    list.add(rand_num)
  return list


if __name__ == "__main__":
  list = randomized_list(100)
  print (list)
  sorted_list = sorted(list)
  print (sorted_list)

