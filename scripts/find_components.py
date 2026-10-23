import json

with open("cells_dump.json", "r") as f:
    cells = json.load(f)

grid = {(c["x"], c["y"]): c for c in cells}

# Let's inspect where paths exist:
path_coords = set(k for k, v in grid.items() if v["source_id"] == 13)

# Find connected components of paths:
components = []
visited = set()

for pt in path_coords:
    if pt in visited:
        continue
    comp = []
    queue = [pt]
    visited.add(pt)
    while queue:
        curr = queue.pop(0)
        comp.append(curr)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nbr = (curr[0] + dx, curr[1] + dy)
            if nbr in path_coords and nbr not in visited:
                visited.add(nbr)
                queue.append(nbr)
    components.append(comp)

print(f"Total path components: {len(components)}")
for i, comp in enumerate(components):
    min_x = min(x for x, y in comp)
    max_x = max(x for x, y in comp)
    min_y = min(y for x, y in comp)
    max_y = max(y for x, y in comp)
    print(f"Component {i}: {len(comp)} cells, bounds ({min_x},{min_y}) to ({max_x},{max_y})")
