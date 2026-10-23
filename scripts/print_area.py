import json
with open('cells_dump.json') as f:
    cells = json.load(f)
grid = {(c['x'], c['y']): c for c in cells}
source_names = {8: 'Cliff', 9: 'Beach', 10: 'Farm', 11: 'Grass', 12: 'PathMid', 13: 'Path', 14: 'WaterMid', 15: 'Water'}

def print_area(x1, y1, x2, y2):
    print(f"=== Area ({x1},{y1}) to ({x2},{y2}) ===")
    for y in range(y1, y2 + 1):
        line = []
        for x in range(x1, x2 + 1):
            c = grid.get((x, y))
            if c:
                name = source_names.get(c['source_id'], str(c['source_id']))
                line.append(f"{name:>5}({c['atlas_x']},{c['atlas_y']})")
            else:
                line.append("   empty   ")
        print(f"{y:3d}: " + " ".join(line))

print_area(-8, -12, 5, -5)
