# Authors: MiniMax-M2.1🧙‍♂️, perplexity.ai🧙‍♂️, scillidan🤡
# Usage: python src_tabfile_text_format.py <input_file> <output_file>

import os
import sys
import re
import ast
from html import unescape
from collections import Counter

# Replace control characters
CONTROL_CHARS_RE = re.compile(r"[\x00-\x1F]")


def remove_control_chars(text: str) -> str:
    return CONTROL_CHARS_RE.sub("", text)


glossary_webfont_greek = [
    ("'a`", "ἄ"),
    ("'a~", "ἂ"),
    ("'a^", "ἆ"),
    ('"a`', "ἄ"),
    ('"a~', "ἂ"),
    ('"a~', "ἃ"),
    ("a`,", "ᾴ"),
    ("'a`,", "ᾄ"),
    ("i:^", "ῗ"),
    ("i:`", "ῒ"),
    ("'a", "ἀ"),
    ('"a', "ἁ"),
    ("a`", "ά"),
    ("a~", "ὰ"),
    ("a^", "ᾶ"),
    ("i:", "ϊ"),
]


def match_chars(text):
    for pattern, replacement in glossary_webfont_greek:
        text = text.replace(pattern, replacement)
    return text


glossary_webfont_symbol = {
    r"<\?/": "⸮",
    r"<aacute/": "á",
    r"<acir/": "â",
    r"<acr/": "ă",
    r"<adot/": "ȧ",
    r"<ae/": "æ",
    r"<AE/": "Æ",
    r"<aemac/": "ǣ",
    r"<agrave/": "à",
    r"<alpha/": "α",
    r"<amac/": "ā",
    r"<aring/": "å",
    r"<asl/": "a",
    r"<atil/": "ã",
    r"<aum/": "ä",
    r"<Aum/": "Ä",
    r"<beta/": "β",
    r"<bprime/": "˝",
    r"<Cced/": "Ç",
    r"<cced/": "ç",
    r"<chi/": "χ",
    r"<cre/": "˘",
    r"<deg/": "°",
    r"<delta/": "δ",
    r"<divide/": "÷",
    r"<dsdot/": "ḍ",
    r"<Eacute/": "É",
    r"<eacute/": "é",
    r"<ecir/": "ê",
    r"<ecr/": "ĕ",
    r"<edh/": "ð",
    r"<egrave/": "è",
    r"<emac/": "ē",
    r"<epsilon/": "ε",
    r"<esl/": "e",
    r"<eta/": "η",
    r"<eum/": "ë",
    r"<flat/": "♭",
    r"<gamma/": "γ",
    r"<hand/": "☞",
    r"<iacute/": "í",
    r"<icir/": "î",
    r"<icr/": "ĭ",
    r"<igrave/": "ì",
    r"<imac/": "ī",
    r"<iota/": "ι",
    r"<isl/": "i",
    r"<ium/": "ï",
    r"<kappa/": "κ",
    r"<lambda/": "λ",
    r"<ldquo/": "“",
    r"<lsquo/": "’",
    r"<middot/": "•",
    r"<mu/": "μ",
    r"<ndot/": "ṅ",
    r"<nsdot/": "ṇ",
    r"<nsm/": "ṉ",
    r"<ntil/": "ñ",
    r"<Ntil/": "Ñ",
    r"<nu/": "ν",
    r"<oacute/": "ó",
    r"<ocar/": "ǒ",
    r"<ocir/": "ô",
    r"<ocr/": "ŏ",
    r"<OE/": "Œ",
    r"<oe/": "œ",
    r"<oemac/": "ōē",
    r"<ograve/": "ò",
    r"<omac/": "ō",
    r"<omega/": "ω",
    r"<omicron/": "ο",
    r"<osl/": "o",
    r"<oum/": "ö",
    r"<Oum/": "Ö",
    r"<phi/": "φ",
    r"<pi/": "π",
    r"<pound/": "£",
    r"<prime/": "´",
    r"<psi/": "ψ",
    r"<rdquo/": "”",
    r"<rho/": "ρ",
    r"<root/": "√",
    r"<rsdot/": "ṛ",
    r"<sec/": "˝",
    r"<sect/": "§",
    r"<segno/": "𝄉",
    r"<sharp/": "♯",
    r"<sigma/": "σ",
    r"<tau/": "τ",
    r"<th/": "th",
    r"<theta/": "θ",
    r"<thorn/": "þ",
    r"<tsdot/": "ṭ",
    r"<uacute/": "ú",
    r"<ucir/": "û",
    r"<ucr/": "ŭ",
    r"<ugrave/": "ù",
    r"<umac/": "ū",
    r"<upsilon/": "υ",
    r"<uring/": "ů",
    r"<usl/": "u",
    r"<uum/": "ü",
    r"<Uum/": "Ü",
    r"<xi/": "ξ",
    r"<ymac/": "ȳ",
    r"<yogh/": "ȝ",
    r"<yum/": "ÿ",
    r"<zeta/": "ζ",
    r"—": "--",
}


def match_symbols(text):
    for pattern, replacement in glossary_webfont_symbol.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


glossary_undefined = {
    r"<nbsp/": " ",
    r"<or/": "or",
    r"<and/": "and",
    r"<bar/": '"horizontal bar"',
    r"<colbreak/": '"column break"',
    r"<colret/": '"column return"',
    r"<downslur/": '"down slur"',
    r"<upslur/": '"up slur"',
    r"<dele/": '<span class="mirror">d</span>',
    r"<ounceap/": "℥ ",
    r"<asterism/": "⁂",
    r"<dagger/": "†",
    r"<iques/": "¿",
    r"<mdash/": "—",
    r"<para/": "¶",
    r"<ai/": "aɪ",
    r"<ait/": "ậ",
    r"<eit/": "ệ",
    r"<etil/": "ẽ",
    r"<hsdot/": "ḥ",
    r"<lsdot/": "ḷ",
    r"<mdot/": "ṃ",
    r"<msdot/": "ṃ",
    r"<ncir/": "n̂",
    r"<oocr/": "ŏŏ",
    r"<oomac/": "ōō",
    r"<udd/": "ʌ",
    r"<usdot/": "ụ",
    r"<ycr/": "y̆",
    r"<zdot/": "ż",
    r"<zsdot/": "ẕ",
    r"<schwa/": "ə",
    r"<cacute/": "ć",
    r"<ccar/": "č",
    r"<csdot/": "c̣",
    r"<add/": "‿",
    r"<asper/": "῾",
    r"<breve/": "˘",
    r"<umlaut/": "¨",
    r"<ffllig/": "ﬀ",
    r"<filig/": "ﬁ",
    r"<fllig/": "ﬂ",
    r"<crev/": "Ↄ",
    r"<digamma/": "ϝ",
    r"<sigmat/": "ς",
    r"<dot/": ".",
    r"<gt/": ">",
    r"<lt/": "<",
    r"<lbrace2/": "{",
    r"<rbrace2/": "}",
    r"<cuberoot/": "∛",
    r"<integral2l/": "∫",
    r"<min/": "'",
    r"<nabla/": "∇",
    r"<times/": "×",
    r"<natural/": "♮",
    r"<pause/": "𝄐",
    r"<rarr/": "→",
    r"<leo/": "♌",
    r"<libra/": "♎",
    r"<pisces/": "♓",
    r"<sagittarius/": "♐",
    r"<scorpio/": "♏",
    r"<taurus/": "♉",
    r"<virgo/": "♍",
    r"<aquarius/": "♒",
    r"<aries/": "♈",
    r"<cancer/": "♋",
    r"<capricorn/": "♑",
    r"<sun/": "☉",
    r"<jupiter/": "♃",
    r"<mercury/": "☿",
    r"<male/": "♂",
    r"<astascending/": "☊",
    r"<astdescending/": "☋",
}


def match_undefined(text):
    for pattern, replacement in glossary_undefined.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def match_symbols_frac(text):
    def frac_to_unicode(match):
        content = match.group(1)
        if "x" not in content:
            if len(content) == 1:
                num = "1"
                den = content
            elif len(content) == 2:
                num = content[0]
                den = content[1]
            else:
                num = content[:-2]
                den = content[-2:]
        else:
            parts = content.split("x")
            num = parts[0]
            den = parts[-1]
        if num and den:
            return f"{sup_to_unicode(num)}⁄{sub_to_unicode(den)}"
        elif den:
            return f"¹⁄{sub_to_unicode(den)}"
        return "0"

    def sup_to_unicode(n):
        sup_map = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        return str(n).translate(sup_map)

    def sub_to_unicode(n):
        sub_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return str(n).translate(sub_map)

    return re.sub(r"<frac([0-9x]+)/", frac_to_unicode, text, flags=re.IGNORECASE)


def match_tags(text):
    text = re.sub(
        r"<point\[(\d{1,2}(?:\.\d)?)\]>(.*?)</point\[\1\]>",
        r"<small>(point\1.)</small> \2",
        text,
        flags=re.DOTALL,
    )

    text = re.sub(r"</p>\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"<p>\s*(\d+)\.\.", r"\1. <br>", text)
    text = re.sub(r"<p>\s*", "<br>", text)
    text = re.sub(r"<b><b>(.*?)</b></b>", r"<b>\1</b>", text, flags=re.DOTALL)

    text = re.sub(r"<!([^>]*?)!>", "", text, flags=re.DOTALL)
    text = re.sub(r"<--([^>]*)-->", "", text, flags=re.DOTALL)
    text = re.sub(r"<nul>(.*?)</nul>", "", text, flags=re.DOTALL)

    text = re.sub(r"<pos>(.*?)</pos>", r"<small>(\1)</small>", text, flags=re.DOTALL)
    text = re.sub(r"<mhw>\{\s*(.*?)\s*\}</mhw>", r"[\1]", text, flags=re.DOTALL)
    text = re.sub(r"<mstypec>(.*?)</mstypec>", r"[\1]", text, flags=re.DOTALL)
    text = re.sub(r"<qau>(.*?)</qau>", r"[\1]", text, flags=re.DOTALL)
    text = re.sub(r"<pr>\((.*?)\)</pr>", r"(\1)", text, flags=re.DOTALL)
    text = re.sub(
        r"\[<source>(.*?)</source>\]",
        r"<small>[\1]</small>",
        text,
        flags=re.DOTALL,
    )

    rules = {
        "quotes": [
            "altname",
            "altnpluf",
            "antiquetype",
            "blacklettertype",
            "boldfacetype",
            "bourgeoistype",
            "boxtype",
            "clarendontype",
            "englishtype",
            "extendedtype",
            "frenchelzevirtype",
            "germantype",
            "gothictype",
            "greatprimertype",
            "hwf",
            "longprimertype",
            "miniontype",
            "nonpareiltype",
            "oldenglishtype",
            "oldstyletype",
            "pearltype",
            "picatype",
            "ptcl",
            "q",
            "sansserif",
            "scripttype",
            "smpicatype",
            "subtypes",
            "tr",
            "tran",
            "typewritertype",
            "universbold",
            "xlati",
        ],
        "plain": [
            "as",
            "au",
            "cas",
            "cd",
            "cd2",
            "chform",
            "chformi",
            "chname",
            "chreact",
            "city",
            "company",
            "corpn",
            "country",
            "cs",
            "date",
            "datey",
            "def",
            "def2",
            "edi",
            "ent",
            "epos",
            "ety",
            "exp",
            "fexp",
            "fract",
            "fu",
            "funct",
            "geog",
            "hw",
            "mathex",
            "method",
            "methodfor",
            "mord",
            "musfig",
            "nmorph",
            "org",
            "perf",
            "persfn",
            "person",
            "plain",
            "plu",
            "pr",
            "pre",
            "qex",
            "qpers",
            "qperson",
            "ratio",
            "refs",
            "river",
            "root",
            "sc",
            "sd",
            "see",
            "sing",
            "sn",
            "specif",
            "state",
            "tt",
            "unit",
            "usage",
            "vertical",
            "vinc",
            "vmorph",
            "w16ns",
            "wf",
            "wns",
            "it",
        ],
        "bold": [
            "abbr",
            "adjf",
            "amorph",
            "col",
            "conjf",
            "decf",
            "h1",
            "h2",
            "plw",
            "singf",
            "singw",
            "spn",
            "b",
            "bold",
        ],
        "blockquote": ["bio", "biography"],
        "italic": [
            "altsp",
            "asp",
            "booki",
            "centered",
            "colp",
            "ecol",
            "figcap",
            "figtitle",
            "film",
            "gen",
            "grk",
            "i",
            "it",
            "itran",
            "itrans",
            "jour",
            "markp",
            "mcol",
            "pluf",
            "publ",
            "ship",
            "title",
            "tradename",
            "ver",
        ],
        "small": [
            "comm",
            "contxt",
            "ex",
            "examp",
            "figref",
            "figure",
            "fld",
            "fr",
            "illu",
            "illust",
            "img",
            "iref",
            "mark",
            "note",
            "syn",
            "uex",
            "wnote",
            "wordforms",
            "xex",
        ],
        "small_space": [
            "rj",
        ],
        "blue": [
            "ant",
            "er",
            "grp",
            "headword",
            "hypen",
            "intensi",
            "inv",
            "isa",
            "ref",
            "sig",
            "simto",
            "stype",
            "stypec",
        ],
        "green": [
            "branchof",
            "causedby",
            "causedbyp",
            "causes",
            "causesp",
            "class",
            "cnvto",
            "colf",
            "compof",
            "conseq",
            "consof",
            "contains",
            "contr",
            "corr",
            "cp",
            "cref",
            "divof",
            "emits",
            "ets",
            "etsep",
            "fam",
            "hascons",
            "kingdom",
            "member",
            "members",
            "membof",
            "ord",
            "part",
            "partof",
            "parts",
            "phylum",
            "prod",
            "prodby",
            "prodmac",
            "prodp",
            "recipr",
            "sfield",
            "stage",
            "stageof",
            "subclass",
            "subfam",
            "subord",
            "suborder",
            "subphylum",
            "usedby",
            "usedfor",
            "uses",
            "var",
            "varn",
        ],
    }

    def apply_rules(category, tags, prefix="", suffix="", html_tag=None):
        nonlocal text
        for tag in tags:
            pattern = rf"<{tag}>(.*?)</{tag}>"
            if html_tag:
                repl = rf"<{html_tag}>\1</{html_tag}>"
            elif prefix or suffix:
                repl = rf"{prefix}\1{suffix}"
            else:
                repl = r"\1"
            text = re.sub(pattern, repl, text, flags=re.DOTALL)

    apply_rules("quotes", rules["quotes"], '"', '"')
    apply_rules("plain", rules["plain"])
    apply_rules("bold", rules["bold"], html_tag="b")
    apply_rules("blockquote", rules["blockquote"], "<blockquote>", "</blockquote>")
    apply_rules("italic", rules["italic"], html_tag="i")
    apply_rules("small", rules["small"], "<small>", "</small>")
    apply_rules("small_space", rules["small_space"], " <small>", "</small>")
    apply_rules("blue", rules["blue"], '<span style="color:blue;">', "</span>")
    apply_rules("green", rules["green"], '<span style="color:green;">', "</span>")

    return text.strip()


def match_other(text):
    text = re.sub(
        r"<(/?)(sub)(s?)(>|\\s+[^>]*>)", r"<\1sub\4", text, flags=re.IGNORECASE
    )
    text = re.sub(
        r"<(/?)(sup)([rs]?)(>|\\s+[^>]*>)", r"<\1sup\4", text, flags=re.IGNORECASE
    )
    text = re.sub(r" <sn>1", "<br><sn>1", text, flags=re.IGNORECASE)
    text = re.sub(r"<br/", "<br>", text, flags=re.IGNORECASE)
    text = re.sub(r"<br>", "<br> ", text)
    text = re.sub(r"<br\s*/?>", "<br>", text, flags=re.IGNORECASE)
    text = re.sub(
        r"<br\s*/?\s*>\s*\[\s*<source>\s*(.*?)\s*</source>\s*\]\s*</p>",
        r" <small>[\1]</small>",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(r">\s*--\s*<col>", r"><br><col>", text, flags=re.IGNORECASE)
    text = re.sub(r">\s*--\s*<mcol>", r"><br><mcol>", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>\s*--\s*", r"</cd><br>", text, flags=re.IGNORECASE)
    return text.strip()


def match_clear(text):
    text = re.sub(r"</p>(?!\s*<[^p])", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"(\S)\s*\n+\s*(\S)", r"\1 \2", text)

    text = re.sub(r"</p>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<b><b>(.*?)</b></b>", r"<b>\1</b>", text, flags=re.DOTALL)
    text = re.sub(r"\s+<br>", "<br>", text)

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"<br\s*/?>\s*<br\s*/?>+", "<br>", text, flags=re.IGNORECASE)
    return text.strip()


def process_definition(text):
    if not text.strip():
        return "[empty definition]"
    text = remove_control_chars(text)
    text = unescape(text)

    text = match_other(text)
    text = match_symbols(text)
    text = match_symbols_frac(text)
    text = match_undefined(text)
    text = match_chars(text)
    text = match_tags(text)
    text = match_clear(text)
    return text


def parse_entries_raw(full_text):
    # GCIDE entry parsing
    lines = full_text.splitlines(keepends=True)
    ent_line_indices = []
    ent_words = []

    ent_line_pattern = re.compile(r"^<p><ent>([^<]+?)</ent><br/?", re.IGNORECASE)

    for idx, line in enumerate(lines):
        m = ent_line_pattern.match(line)
        if m:
            ent_line_indices.append(idx)
            ent_words.append(m.group(1).strip())

    print(f"Found {len(ent_line_indices)} entry headers")

    if not ent_line_indices:
        return []

    entries = []
    for i, (start_idx, word) in enumerate(zip(ent_line_indices, ent_words)):
        end_idx = (
            ent_line_indices[i + 1] if i + 1 < len(ent_line_indices) else len(lines)
        )

        # Content after <br/ in current line
        line = lines[start_idx]
        br_pos = line.find("<br/")
        first_def_part = line[br_pos + len("<br/") :].strip() if br_pos >= 0 else ""

        # Subsequent lines
        rest_def_parts = " ".join(
            line.strip() for line in lines[start_idx + 1 : end_idx]
        )

        raw_def = (first_def_part + rest_def_parts).strip()
        entries.append((word, raw_def))

    return entries


def check_tags(output_file, log_file):
    with open(output_file, "r", encoding="utf-8") as f:
        text = f.read()

    defined_prefixes = set()
    for glossary in [glossary_webfont_symbol, glossary_undefined]:
        for key in glossary:
            if key.startswith("<") and key.endswith("/"):
                prefix = key[1:-1].lower()
                defined_prefixes.add(prefix)

    prefix_pattern = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)/")
    unmapped = Counter()
    for match in prefix_pattern.finditer(text):
        prefix = match.group(1).lower()
        if prefix not in defined_prefixes:
            unmapped[prefix] += 1

    with open(log_file, "w", encoding="utf-8") as log:
        log.write("Missing tags:\n")
        for prefix, count in sorted(unmapped.items(), key=lambda x: (-x[1], x[0])):
            log.write(f"<{prefix}/>\t{count}\n")

        log.write(f"\nTotal missing: {len(unmapped)} types")
        log.write(f"\nGlossary covers: {len(defined_prefixes)} prefixes")


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print("Reading file...")
    with open(input_file, "r", encoding="utf-8") as f:
        full_text = f.read()

    print("Parsing entries...")
    entries = parse_entries_raw(full_text)

    print("Processing definitions (this will take a while)...")
    results = []
    for i, (word, raw_def) in enumerate(entries):
        definition = process_definition(raw_def)
        results.append(f"{word}\t{definition}")

        # Progress display
        if (i + 1) % 10000 == 0:
            print(f"Processed {i + 1}/{len(entries)} entries...")

    print("Writing output file...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"✅ Done! Processed {len(results)} entries in total")

    filename = os.path.splitext(os.path.basename(output_file))[0]
    check_log = filename + "_check_tags.log"
    check_tags(output_file, check_log)


if __name__ == "__main__":
    main()
