import json


new=['a','b','e','f','g','j']


try:
    with open(f'rede.json', 'r') as file:

        old_list = json.load(file)
        print(old_list)

    nn =[]
    for u in new:

        if u not in old_list:
            nn.append(u)
    
    with open(f'rede.json', 'w') as file:

        json.dump(nn, file)

        


except:
    with open(f'rede.json', 'w') as file:

        json.dump(new, file)