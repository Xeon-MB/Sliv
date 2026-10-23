import json
import subprocess

out = subprocess.run(['git', 'show', 'HEAD~1:scenes/game.tscn'], capture_output=True, text=True, errors='ignore')
with open('game_prev_temp.tscn', 'w', encoding='utf-8') as f:
    f.write(out.stdout)
