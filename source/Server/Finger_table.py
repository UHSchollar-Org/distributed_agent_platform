# The class FingerTable is responsible for managing the finger table of each node.
m = 7


class FingerTable:
    # The __init__ fucntion is used to initialize the table with values when
    # a new node joins the ring.
    def __init__(self, my_id):
        self.table = []
        for i in range(m):
            x = pow(2, i)
            entry = (my_id + x) % pow(2, m)
            node = None
            self.table.append([entry, node])

    def print(self):
        # The print function is used to print the finger table of a node.
        for index, entry in enumerate(self.table):
            if entry[1] is None:
                print(
                    "Entry: ",
                    index,
                    " Interval start: ",
                    entry[0],
                    " Successor: ",
                    "None",
                )
            else:
                print(
                    "Entry: ",
                    index,
                    " Interval start: ",
                    entry[0],
                    " Successor: ",
                    entry[1].id,
                )
