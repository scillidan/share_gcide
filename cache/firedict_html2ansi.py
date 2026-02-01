# Authors: GPT-4o mini🧙‍♂️, scillidan🤡
# Usage: python file.py <input_file> <output_file>

import sys
import re

def process_text(text):
    # Replace <br /> with newline
    text = re.sub(r'<br\s*/?>', '\n', text)

    # Replace <small>...</small> with dim (ANSI 2m) around inner text
    text = re.sub(r'<small>(.*?)</small>', r'\033[2m\1\033[0m', text, flags=re.DOTALL)

    # Replace <b> and styled <b style="color: #00b"> with bold and blue
    text = re.sub(r'<b\s+style="color:\s*#00b"\s*>', '\033[1m\033[34m', text)
    text = text.replace('<b>', '\033[1m')
    text = text.replace('</b>', '\033[0m')

    # Replace <span style="color: #..."> for some color codes
    def span_color(match):
        color = match.group(1).lower()
        mapping = {
            '#33a': '\033[34m',
            '#33f': '\033[34m',
            '#a00': '\033[31m',
            '#8b4513': '\033[31m',
        }
        return mapping.get(color, '')

    text = re.sub(r'<span style="color:\s*(#[0-9a-f]+)">', span_color, text)
    text = text.replace('</span>', '\033[0m')

    # Replace <i> tags, optionally styled
    text = re.sub(r'<i\s+style="color:\s*#a00"\s*>', '\033[3m\033[31m', text)
    text = re.sub(r'<i\s+style="color:\s*#33f"\s*>', '\033[3m\033[34m', text)
    text = text.replace('<i>', '\033[3m')
    text = text.replace('</i>', '\033[0m')

    return text

def main():
	if len(sys.argv) != 3:
		print("Usage: python cli.py input output")
		sys.exit(1)
	input_file = sys.argv[1]
	output_file = sys.argv[2]

	with open(input_file, "r", encoding="utf-8") as f:
		content = f.read()

	processed = process_text(content)

	with open(output_file, "w", encoding="utf-8") as f:
		f.write(processed)

if __name__ == "__main__":
	main()
