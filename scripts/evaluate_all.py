import json

with open("cells_dump.json", "r") as f:
    cells = json.load(f)

grid = {(c["x"], c["y"]): c for c in cells}

# Standard 3x3 cardinal neighbor mapping:
# (North, South, West, East) -> (atlas_x, atlas_y)
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

# For inner corners (when all 4 cardinals are present):
# SE missing -> (0, 3)
# SW missing -> (1, 3)
# NE missing -> (0, 4)
# NW missing -> (1, 4)
# Note for Beach (5x3):
# SE missing -> (3, 0)
# SW missing -> (4, 0)
# NE missing -> (3, 1)
# NW missing -> (4, 1)

def evaluate_source(sid, name, has_inner_3x6=True, beach_inner=False):
    s_cells = [c for c in cells if c["source_id"] == sid]
    print(f"\n================ {name} (source {sid}) - {len(s_cells)} cells ================")
    
    issues = []
    for c in s_cells:
        x, y = c["x"], c["y"]
        ax, ay = c["atlas_x"], c["atlas_y"]
        
        n_up = grid.get((x, y-1), {}).get("source_id") == sid
        n_down = grid.get((x, y+1), {}).get("source_id") == sid
        n_left = grid.get((x-1, y), {}).get("source_id") == sid
        n_right = grid.get((x+1, y), {}).get("source_id") == sid
        
        cardinals = (n_up, n_down, n_left, n_right)
        
        if cardinals not in outer_and_edge:
            issues.append((x, y, cardinals, (ax, ay), f"narrow/unsupported cardinals: {cardinals}"))
            continue
            
        rule = outer_and_edge[cardinals]
        if rule == 'center_or_inner':
            nw = grid.get((x-1, y-1), {}).get("source_id") == sid
            ne = grid.get((x+1, y-1), {}).get("source_id") == sid
            sw = grid.get((x-1, y+1), {}).get("source_id") == sid
            se = grid.get((x+1, y+1), {}).get("source_id") == sid
            
            missing_diags = []
            if not se: missing_diags.append('SE')
            if not sw: missing_diags.append('SW')
            if not ne: missing_diags.append('NE')
            if not nw: missing_diags.append('NW')
            
            if len(missing_diags) == 0:
                # pure center
                # can be (1, 1) or row 5
                valid = [(1, 1)]
                if has_inner_3x6:
                    valid += [(0, 5), (1, 5), (2, 5)]
                if (ax, ay) not in valid:
                    issues.append((x, y, cardinals, (ax, ay), f"expected center {valid}, got ({ax},{ay})"))
            elif len(missing_diags) == 1:
                # single inner corner
                diag = missing_diags[0]
                if has_inner_3x6:
                    expected_corner = {'SE': (0, 3), 'SW': (1, 3), 'NE': (0, 4), 'NW': (1, 4)}[diag]
                elif beach_inner:
                    expected_corner = {'SE': (3, 0), 'SW': (4, 0), 'NE': (3, 1), 'NW': (4, 1)}[diag]
                else:
                    expected_corner = (1, 1)
                
                if (ax, ay) != expected_corner:
                    issues.append((x, y, cardinals, (ax, ay), f"inner corner missing {diag}: expected {expected_corner}, got ({ax},{ay})"))
            else:
                # multiple missing diagonals
                issues.append((x, y, cardinals, (ax, ay), f"multiple missing diagonals {missing_diags}, got ({ax},{ay})"))
        else:
            if (ax, ay) != rule:
                issues.append((x, y, cardinals, (ax, ay), f"expected {rule}, got ({ax},{ay})"))
    
    print(f"Total issues found: {len(issues)}")
    for iss in issues[:30]:
        print(f"  ({iss[0]:2d},{iss[1]:2d}) curr=({iss[3][0]},{iss[3][1]}): {iss[4]}")
    if len(issues) > 30:
        print(f"  ... and {len(issues)-30} more")

evaluate_source(13, "Path", has_inner_3x6=True)
evaluate_source(8, "Cliff", has_inner_3x6=True)
evaluate_source(15, "Water", has_inner_3x6=True)
evaluate_source(9, "Beach", has_inner_3x6=False, beach_inner=True)
evaluate_source(10, "FarmLand", has_inner_3x6=False)
