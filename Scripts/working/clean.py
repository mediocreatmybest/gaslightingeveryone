def sanitize_text_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        contents = f.read()
    lines = contents.split('\n')
    for i, line in enumerate(lines):
        line = line.replace('  ', ' ')
        line = line.replace(',,', ',')
        line = line.replace(', ,', ',')
        lines[i] = line
    sanitized_contents = '\n'.join(lines)
    with open(file_name, 'w') as f:
        f.write(sanitized_contents)

from pathlib import Path

out_file = Path(r"c:\output\test.txt")

sanitize_text_file(out_file)