# Create your own linked list

```
class node:
    def __init__(self, dataval=None):
        self.value = dataval
        self.nextval = None

class linked_list:
    def __init__(self):
        self.headval = None

    def add(self, node):
        np = headval
        while (np != None):
          np = np.nextval

        np = node

   def print(self):
        printval = self.headval
        while printval is not None:
            print(printval.dataval)
            printval = printval.nextval

list = linked_list()
list.add(node(1))
list.add(node(2))
list.add(node(3))
list.print()
```
class node:
  def __init__(self, value):
    self.value = None
    self.next = None

  def __str__(self):
    return "node"

  def __repr__(self):
    return {"class": "node" }

class linked_list:
  def __init__(self):


  def __str__(self):
    return "linked_list"

  def __repr__(self):
    return {"class": linked_list }
```