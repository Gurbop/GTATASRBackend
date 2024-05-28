friends={'bob':['joe','billy','shaggy'], 'shaggy':['joe','billy'],'sigma':['joe','alpha'],'joe':['poopy'],'billy':[],'alpha':[],'poopy':[]}

visited = set()
level = ['bob']
result = []
levels = []
node_levels = {'bob': 0}  # Dictionary to store levels of each node

current_level = 0

while level:
    next_level = []
    levels.append(level.copy())

    while level:
        current_node = level.pop(0)

        if current_node not in visited:
            visited.add(current_node)
            result.append(current_node)

            for neighbor in friends[current_node]:
                if neighbor not in visited and neighbor not in next_level:
                    next_level.append(neighbor)
                    node_levels[neighbor] = current_level + 1  # Set level of neighbor

    level = next_level
    current_level += 1

print("BFS Traversal:", result)
print("Levels:", levels)
print("Node Levels:", node_levels)
