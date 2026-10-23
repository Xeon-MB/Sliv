import json
from PIL import Image

with open("cells_dump.json", "r") as f:
    cells = json.load(f)

min_x = -34
min_y = -24

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

save_crop("crop_lake.png", 5, 8, 30, 26)
save_crop("crop_water_pond_top.png", -25, -20, -10, -12)
save_crop("crop_center_cross.png", -10, -5, 10, 5)
