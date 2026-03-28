import os
import re

base_dir = "/Users/michaljalbrzykowski/Szwalnia ISABELL - Claude Code"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replacing 16:00 with 15:00 globally
    content = content.replace("8:00–16:00", "8:00–15:00")
    content = content.replace("do 16:00", "do 15:00")
    content = content.replace("16:00", "15:00")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            process_file(os.path.join(root, f))

print("Global hours update completed.")
