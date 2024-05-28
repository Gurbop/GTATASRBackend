friends={'bob':['joe','billy','shaggy'], 'shaggy':['joe','billy'],'sigma':['joe','alpha'],'joe':['poopy'],'billy':[],'alpha':[],'poopy':[]}
visited=set()

level = ['bob']
result = []
levels=[]
while level:
    levels.append(level.copy())
    current_node = level.pop(0)

    if current_node not in visited:
        visited.add(current_node)
        result.append(current_node)

        for neighbor in friends[current_node]:
            if neighbor not in visited:
                level.append(neighbor)
    
print(result)
print(levels)
