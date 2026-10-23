import json
from PIL import Image

with open("cells_dump.json", "r") as f:
    cells = json.load(f)

min_x = min(c['x'] for c in cells) # -34
min_y = min(c['y'] for c in cells) # -24

full_map = Image.open("map_rendered.png")

def save_crop(name, x1, y1, x2, y2, scale=2):
    px1 = (x1 - min_x) * 16
    py1 = (y1 - min_y) * 16
    px2 = (x2 - min_x + 1) * 16
    py2 = (y2 - min_y + 1) * 16
    cropped = full_map.crop((px1, py1, px2, py2))
    if scale > 1:
        cropped = cropped.resize((cropped.width * scale, cropped.height * scale), Image.NEAREST)
    cropped.save(name)
    print(f"Saved {name}: ({x1},{y1}) to ({x2},{y2}), pixel size {cropped.size}")

save_crop("crop_top_path.png", -6, -23, 6, -10)
save_crop("crop_comp1.png", -22, -16, -2, -7)
save_crop("crop_comp2.png", 16, -18, 27, -11)
save_crop("crop_comp3.png", -8, -11, 2, -5)
save_crop("crop_diagonal_path.png", 6, 3, 17, 17)
save_crop("crop_farmland.png", -28, -9, -15, 10)
