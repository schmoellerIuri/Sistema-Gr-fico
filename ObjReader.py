def GetObjectFromFile(filePath):
    vertices = []
    with open(filePath, 'r') as file:
        for line in file:
            if (line.startswith('v ')):
                split = line.split(' ')[1:]
                if len(split) > 2: return None

                x, y = split[0], split[1]
                vertices.append((float(x), float(y)))

    return vertices