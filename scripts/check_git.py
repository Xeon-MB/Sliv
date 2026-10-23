import subprocess

out = subprocess.run(['git', 'show', 'HEAD~1:scenes/game.tscn'], capture_output=True, text=True, errors='ignore')
print("returncode:", out.returncode)
for line in out.stdout.splitlines():
    if 'tile_map_data' in line:
        print("Found line length:", len(line))
        break
