import os
import re

base_dir = "/Users/michaljalbrzykowski/Szwalnia ISABELL - Claude Code"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix CSS links
    content = re.sub(r'href="\.\./\.\./style\.css"', 'href="/style.css"', content)
    content = re.sub(r'href="\.\./style\.css"', 'href="/style.css"', content)
    content = re.sub(r'href="style\.css"', 'href="/style.css"', content)

    # Fix Assets links
    content = re.sub(r'src="\.\./\.\./assets/', 'src="/assets/', content)
    content = re.sub(r'src="\.\./assets/', 'src="/assets/', content)
    content = re.sub(r'src="assets/', 'src="/assets/', content)

    # Fix HTML links that still point to index.html
    content = re.sub(r'href="\.\./uslugi/([^/]+)/index\.html"', r'href="/uslugi/\1"', content)
    content = re.sub(r'href="\.\./szwalnia-([^/]+)/index\.html"', r'href="/szwalnia-\1"', content)
    content = re.sub(r'href="\.\./([^/]+)/index\.html"', r'href="/\1"', content)
    
    # Generic index.html removals (if any left)
    content = re.sub(r'/index\.html"', '"', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            process_file(os.path.join(root, f))

print("Completed processing all HTML files.")
