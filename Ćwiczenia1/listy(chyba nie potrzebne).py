# Czy to miało być zadaniem????

list = [1,2,3,4,5]

for num in list:
    print(num)

for i in range(len(list)):
    print("Tab[{i}] = {list[i]}")

list2 = {
    'Pierwsze': 1, 
    'Drugie': 2, 
    'Trzecie': 3, 
    'Prawda': True}

for key in list2:
    print(f"Hash[{key}] = {list2[key]}")
