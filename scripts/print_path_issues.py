import json

with open("cells_dump.json", "r") as f:
    cells = json.load(f)

grid = {(c["x"], c["y"]): c for c in cells}

outer_and_edge = {
    (False, True, False, True): (0, 0),   # TL outer
    (False, True, True, True):  (1, 0),   # T edge
    (False, True, True, False): (2, 0),   # TR outer
    (True, True, False, True):  (0, 1),   # L edge
    (True, True, True, True):   'center_or_inner',
    (True, True, True, False):  (2, 1),   # R edge
    (True, False, False, True): (0, 2),   # BL outer
    (True, False, True, True):  (1, 2),   # B edge
    (True, False, True, False): (2, 2),   # BR outer
}

s_cells = [c for c in cells if c["source_id"] == 13]
for c in s_cells:
    x, y = c["x"], c["y"]
    ax, ay = c["atlas_x"], c["atlas_y"]
    
    n_up = grid.get((x, y-1), {}).get("source_id") == 13
    n_down = grid.get((x, y+1), {}).get("source_id") == 13
    n_left = grid.get((x-1, y), {}).get("source_id") == 13
    n_right = grid.get((x+1, y), {}).get("source_id") == 13
    
    cardinals = (n_up, n_down, n_left, n_right)
    
    if cardinals not in outer_and_edge:
        print(f"PATH NARROW/UNUSUAL at ({x:2d},{y:2d}) curr=({ax},{ay}): cardinals N={n_up} S={n_down} W={n_left} E={n_right}")
    else:
        rule = outer_and_edge[cardinals]
        if rule == 'center_or_inner':
            nw = grid.get((x-1, y-1), {}).get("source_id") == 13
            ne = grid.get((x+1, y-1), {}).get("source_id") == 13
            sw = grid.get((x-1, y+1), {}).get("source_id") == 13
            se = grid.get((x+1, y+1), {}).get("source_id") == 13
            missing = [d for d, m in [('SE', se), ('SW', sw), ('NE', ne), ('NW', nw)] if not m]
            if len(missing) == 0:
                if (ax, ay) not in [(1,1), (0,5), (1,5), (2,5)]:
                    print(f"PATH GLITCH at ({x:2d},{y:2d}) curr=({ax},{ay}): should be center")
            elif len(missing) == 1:
                exp = {'SE': (0,3), 'SW': (1,3), 'NE': (0,4), 'NW': (1,4)}[missing[0]]
                if (ax, ay) != exp:
                    print(f"PATH GLITCH CORNER at ({x:2d},{y:2d}) curr=({ax},{ay}): missing diag {missing[0]}, should be {exp}")
            else:
                print(f"PATH MULTI-DIAG CORNER at ({x:2d},{y:2d}) curr=({ax},{ay}): missing diags {missing}")
        else:
            if (ax, ay) != rule:
                print(f"PATH GLITCH EDGE/CORNER at ({x:2d},{y:2d}) curr=({ax},{ay}): should be {rule}")
