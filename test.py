adj = [(0,1), (1,2), (2,3)]

neighbors = [u for (u, w) in adj if w == 0]

if len(adj):
    print ("Its work...")

if len(neighbors):
    print("works")
else:
    print("fail")

print(neighbors)