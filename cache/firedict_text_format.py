# Authors: GPT-4o mini🧙‍♂️, scillidan🤡
# Usage: python file.py <input_file> <output_file>

import sys
import re

def transform(content: str) -> str:
    content = re.sub(r'(?<=\s)--\s', '<br />', content, flags=re.DOTALL)
    content = re.sub(r'<small>(.*?)</small>', r'--\1', content, flags=re.DOTALL)
    content = re.sub(r'<b style="color: #00b">(.*?)</b>', r'\1', content, flags=re.DOTALL)
    content = re.sub(r'<span\s+style\s*=\s*"color:\s*33a">(.*?)</span>', r'\1', content, flags=re.DOTALL)
    content = re.sub(r'<span\s+style\s*=\s*"color:\s*#a00">(.*?)</span>', r'<i>\1</i>', content, flags=re.DOTALL)
    content = re.sub(r'<i style="color: #a00">(.*?)</i>', r'<i>\1</i>', content, flags=re.DOTALL)
    content = re.sub(r'<span\s+style\s*=\s*"color:\s*#33f">(.*?)</span>', r'<i>\1</i>', content, flags=re.DOTALL)
    content = re.sub(r'<i style="color: #33f">(.*?)</i>', r'<i>\1</i>', content, flags=re.DOTALL)
    content = re.sub(r'^(<br />)+', r'<br />', content, flags=re.DOTALL)
    content = re.sub(r'\n +', '\n', content, flags=re.DOTALL)
    return content

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input.txt> <output.txt>")
        sys.exit(1)
    input_file, output_file = sys.argv[1], sys.argv[2]

    with open(input_file, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    processed = transform(content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed)

if __name__ == '__main__':
    main()