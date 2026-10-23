import subprocess

curr = ""
with open("scenes/game.tscn", "r", encoding="utf-8") as f:
    for line in f:
        if "tile_map_data = PackedByteArray(" in line:
            curr = line.strip()

out = subprocess.run(['git', 'show', 'HEAD~1:scenes/game.tscn'], capture_output=True, text=True, errors='ignore')
prev = ""
for line in out.stdout.splitlines():
    if "tile_map_data = PackedByteArray(" in line:
        prev = line.strip()

print("Curr tile_map_data len:", len(curr))
print("Prev tile_map_data len:", len(prev))
print("Equal?", curr == prev)
