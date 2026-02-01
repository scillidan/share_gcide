# Usage: python file.py <input_file> <output_file>

import sys
import re

def convert(input_file, output_file):
    replacements = {
        "<br>": r"\n",
        '<span style="color:green;">': "\033[32m",
        '<span style="color:blue;">': "\033[34m",
        "</span>": "\033[0m",
        "<b>": "\033[1m",
        "</b>": "\033[22m",
        "<i>": "\033[3m",
        "</i>": "\033[23m",
        "<small>": "\033[2m",
        "</small>": "\033[0m",
        "<sup>": "\033[38;5;143m",
        "</sup>": "\033[0m",
        "<sub>": "\033[38;5;143m",
        "</sub>": "\033[0m",
        "<blockquote>": "    ",
        "</blockquote>": "",
        '<span class="mirror">d</span>': "d",
    }

    def convert_link(match):
        a_tag = match.group(1)
        text_inner = match.group(2)
        return f"\033[4;34m{text_inner}\033[0m"

    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:

        for line in f_in:
            if '\t' not in line:
                # Skip lines that aren't properly formatted (not tab-separated)
                continue

            parts = line.strip().split('\t', 1)
            if len(parts) < 2:
                continue

            word = parts[0]
            meaning = parts[1]

            for html, ansi in replacements.items():
                meaning = meaning.replace(html, ansi)

            meaning = re.sub(r'<a\s+href="([^"]*)">([^<]*)</a>', convert_link, meaning)

            f_out.write(f"{word}\t{meaning}\n")

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert(input_file, output_file)
    print(f"Conversion completed: {input_file} to {output_file}")

if __name__ == '__main__':
    main()