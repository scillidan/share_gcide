# Authors: DeepSeek🧙‍♂️, scillidan🤡
# Usage: python file.py <input_file> <output_file>

import sys
import re
from html import unescape

def match_add(text):
    # Add <br> between </div> and <ul>
    text = re.sub(r'</div>\s*<div>\s*<ul>', '</div><br><ul>', text)
    # Add space between </font> and <font ...>
    text = re.sub(r'</font>\s*<font([^>]*)>', r'</font> <font\1>', text)
    return text

def match_replace(text):
    # Replace all variations of <br> tags with <br>
    text = re.sub(r'<br\s*/?>', '<br>', text)
    # Replace with space
    text = text.replace('\xa0', ' ').replace('&nbsp;', ' ')
    return text

def match_convert(text):
    # Convert "<ul><li>item1</li><li>item2</li></ul>" to "- item1<br>- item2"
    def repl(match):
        ul_content = match.group(1)
        items = re.findall(r'<li>(.*?)</li>', ul_content, re.DOTALL)
        cleaned_items = ['- ' + re.sub(r'\s+', ' ', unescape(item.strip())) for item in items]
        return '<br><br>' + '<br>'.join(cleaned_items)
    text = re.sub(r'<ul>(.*?)</ul>', repl, text, flags=re.DOTALL)
    return text

def match_remove(text):
    # Remove <font></font>
    text = re.sub(r'<font[^>]*>', '', text)
    text = re.sub(r'</font>', '', text)
    # Remove <div style:"border...></div>
    pattern = re.compile(r'<div style="border: 1px solid; padding: 5px">(.*)</div>', re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return text

def match_remove_except_allowed_tags(text):
    # Remove all HTML tags except allowed ones: br, b, i, span, sub, sup, blockquote, small, p
    allowed_tags = ['br', 'b', 'i', 'span', 'sub', 'sup', 'blockquote', 'small', 'p']
    # Create pattern to match tags not in allowed list
    tag_pattern = r'<(?!\/?(?:' + '|'.join(allowed_tags) + r')(?:\s[^>]*)?>)[^>]+>'
    return re.sub(tag_pattern, '', text)

def match_other(text):
    # Replace repeated <br> with single <br>
    text = re.sub(r'(<br>\s*)+', '<br>', text)
    # Replace multiple spaces with single space
    text = re.sub(r' {2,}', ' ', text)
    # Replace / with ", "
    text = re.sub(r'\s*/\s*', ', ', text)
    return text

def replace_symbols(text):
    symbols = {
        '<?/': '⸮',
        '<aacute/': 'á',
        '<acir/': 'â',
        '<acr/': 'ă',
        '<adot/': 'ȧ',
        '<ae/': 'æ',
        '<AE/': 'Æ',
        '<aemac/': 'ǣ',
        '<agrave/': 'à',
        '<amac/': 'ā',
        '<aring/': 'å',
        '<atil/': 'ã',
        '<aum/': 'ä',
        '<Aum/': 'Ä',
        '<bprime/': '˝',
        '<Cced/': 'Ç',
        '<cced/': 'ç',
        '<cre/': '˘',
        '<deg/': '°',
        '<divide/': '÷',
        '<dsdot/': 'ḍ',
        '<Eacute/': 'É',
        '<eacute/': 'é',
        '<ecir/': 'ê',
        '<ecr/': 'ĕ',
        '<edh/': 'ð',
        '<egrave/': 'è',
        '<emac/': 'ē',
        '<eum/': 'ë',
        '<flat/': '♭',
        '<frac12/': '½',
        '<frac13/': '⅓',
        '<frac14/': '¼',
        '<frac23/': '⅔',
        '<hand/': '☞',
        '<iacute/': 'í',
        '<icir/': 'î',
        '<icr/': 'ĭ',
        '<igrave/': 'ì',
        '<imac/': 'ī',
        '<ium/': 'ï',
        '<ldquo/': '“',
        '<lsquo/': '‘',
        '<middot/': '•',
        '<ndot/': 'ṅ',
        '<nsdot/': 'ṇ',
        '<nsm/': 'ṉ',
        '<ntil/': 'ñ',
        '<Ntil/': 'Ñ',
        '<oacute/': 'ó',
        '<ocar/': 'ǒ',
        '<ocir/': 'ô',
        '<ocr/': 'ŏ',
        '<OE/': 'Œ',
        '<oe/': 'œ',
        '<oemac/': 'ōē',
        '<ograve/': 'ò',
        '<omac/': 'ō',
        '<oum/': 'ö',
        '<Oum/': 'Ö',
        '<pound/': '£',
        '<prime/': '´',
        '<rdquo/': '”',
        '<root/': '√',
        '<rsdot/': 'ṛ',
        '<sec/': '˝',
        '<sect/': '§',
        '<segno/': '𝄉',
        '<sharp/': '♯',
        '<th/': 'th',
        '<thorn/': 'þ',
        '<tsdot/': 'ṭ',
        '<uacute/': 'ú',
        '<ucir/': 'û',
        '<ucr/': 'ŭ',
        '<ugrave/': 'ù',
        '<umac/': 'ū',
        '<uum/': 'ü',
        '<Uum/': 'Ü',
        '<ymac/': 'ȳ',
        '<yogh/': 'ȝ',
        '<yum/': 'ÿ',
        '—': '--',
    }

    for old, new in symbols.items():
        text = text.replace(old, new)
    return text

def replace_chars(text):
    char_map = {
        "'a": 'ἀ',
        '"a': 'ἁ',
        'a`': 'ά',
        'a~': 'ὰ',
        'a^': 'ᾶ',
        "'a`": 'ἄ',
        "'a~": 'ἂ',
        "'a^": 'ἆ',
        '"a`': 'ἄ',
        '"a~': 'ἂ',
        '"a~': 'ἃ',
        'a`,': 'ᾴ',
        "'a`,": 'ᾄ',
        'i:': 'ϊ',
        'i:^': 'ῗ',
        'i:`': 'ῒ',
    }

    for old, new in char_map.items():
        text = text.replace(old, new)
    return text

def replace_tags(text):
    # Tags to preserve with their content
    preserve_tags = {
        '<as>$</as>': '$',
        '<au>$</au>': '$',
        '<b>$</b>': '$',
        '<bold>$</bold>': '$',
        '<cas>$</cas>': '$',
        '<chform>$</chform>': '$',
        '<chformi>$</chformi>': '$',
        '<chname>$</chname>': '$',
        '<chreact>$</chreact>': '$',
        '<city>$</city>': '$',
        '<company>$</company>': '$',
        '<corpn>$</corpn>': '$',
        '<country>$</country>': '$',
        '<cs>$</cs>': '$',
        '<date>$</date>': '$',
        '<datey>$</datey>': '$',
        '<edi>$</edi>': '$',
        '<ent>$</ent>': '$',
        '<epos>$</epos>': '$',
        '<ety>$</ety>': '$',
        '<exp>$</exp>': '$',
        '<fexp>$</fexp>': '$',
        '<fract>$</fract>': '$',
        '<fu>$</fu>': '$',
        '<funct>$</funct>': '$',
        '<geog>$</geog>': '$',
        '<hw>$</hw>': '$',
        '<mathex>$</mathex>': '$',
        '<method>$</method>': '$',
        '<methodfor>$</methodfor>': '$',
        '<mord>$</mord>': '$',
        '<musfig>$</musfig>': '$',
        '<nmorph>$</nmorph>': '$',
        '<org>$</org>': '$',
        '<perf>$</perf>': '$',
        '<persfn>$</persfn>': '$',
        '<person>$</person>': '$',
        '<plain>$</plain>': '$',
        '<plu>$</plu>': '$',
        '<pr>$</pr>': '$',
        '<pre>$</pre>': '$',
        '<qex>$</qex>': '$',
        '<qpers>$</qpers>': '$',
        '<qperson>$</qperson>': '$',
        '<ratio>$</ratio>': '$',
        '<refs>$</refs>': '$',
        '<river>$</river>': '$',
        '<root>$</root>': '$',
        '<sc>$</sc>': '$',
        '<see>$</see>': '$',
        '<sing>$</sing>': '$',
        '<sn>$</sn>': '$',
        '<source>$</source>': '$',
        '<state>$</state>': '$',
        '<tt>$</tt>': '$',
        '<unit>$</unit>': '$',
        '<vertical>$</vertical>': '$',
        '<vinc>$</vinc>': '$',
        '<vmorph>$</vmorph>': '$',
        '<w16ns>$</w16ns>': '$',
        '<wf>$</wf>': '$',
        '<wns>$</wns>': '$',
    }

    # Tags to convert to bold
    bold_tags = [
        '<abbr>$</abbr>', '<adjf>$</adjf>', '<amorph>$</amorph>', '<col>$</col>',
        '<conjf>$</conjf>', '<decf>$</decf>', '<h1>$</h1>', '<h2>$</h2>',
        '<plw>$</plw>', '<singw>$</singw>', '<spn>$</spn>'
    ]

    # Tags to convert to line breaks
    br_tags = ['<cd2>$</cd2>', '<cd>$</cd>', '<def2>$</def2>', '<def>$</def>', '<usage>$</usage>']

    # Special cases
    special_cases = {
        '<sd>$</sd>': '<br>- $',
        '<bio>$</bio>': '<br><blockquote>$</blockquote>',
        '<biography>$</biography>': '<br><blockquote>$</blockquote>',
    }

    # Tags to convert to italic
    italic_tags = [
        '<altsp>$</altsp>', '<asp>$</asp>', '<booki>$</booki>', '<centered>$</centered>',
        '<colp>$</colp>', '<ecol>$</ecol>', '<figcap>$</figcap>', '<figtitle>$</figtitle>',
        '<film>$</film>', '<gen>$</gen>', '<grk>$</grk>', '<i>$</i>', '<it>$</it>',
        '<itran>$</itran>', '<itrans>$</itrans>', '<jour>$</jour>', '<mark>$</mark>',
        '<markp>$</markp>', '<mcol>$</mcol>', '<pluf>$</pluf>', '<publ>$</publ>',
        '<ship>$</ship>', '<title>$</title>', '<tradename>$</tradename>', '<ver>$</ver>'
    ]

    # Paragraph tag
    paragraph_tag = '<p>$</p>'

    # Small tags
    small_tags = [
        '<fld>$</fld>', '<comm>$</comm>', '<contxt>$</contxt>', '<ex>$</ex>',
        '<examp>$</examp>', '<figref>$</figref>', '<figure>$</figure>', '<fr>$</fr>',
        '<illu>$</illu>', '<illust>$</illust>', '<img>$</img>', '<iref>$</iref>',
        '<note>$</note>', '<syn>$</syn>', '<uex>$</uex>', '<wnote>$</wnote>',
        '<wordforms>$</wordforms>'
    ]

    # Special small tags with text
    small_text_tags = {
        '<comm>$</comm>': '<small>(comm.)</small> $',
        '<contxt>$</contxt>': '<small>(contxt.)</small> $',
        '<ex>$</ex>': '<small>(ex.)</small> $',
        '<examp>$</examp>': '<small>(examp.)</small> $',
        '<figref>$</figref>': '<small>(figref.)</small> $',
        '<figure>$</figure>': '<small>(figure.)</small> $',
        '<fr>$</fr>': '<small>(fr.)</small> $',
        '<illu>$</illu>': '<small>(illu.)</small> $',
        '<illust>$</illust>': '<small>(illust.)</small> $',
        '<img>$</img>': '<small>(img.)</small> $',
        '<iref>$</iref>': '<small>(iref.)</small> $',
        '<note>$</note>': '<small>(note.)</small> $',
        '<syn>$</syn>': '<small>(syn.)</small> $',
        '<uex>$</uex>': '<small>(uex.)</small> $',
        '<wnote>$</wnote>': '<small>(wnote.)</small> $',
        '<wordforms>$</wordforms>': '<small>(wordforms.)</small> $',
    }

    # Point tags (special case with number)
    point_tag = r'<point(\d+)>\$(.*?)</point\1>'

    # Small italic tags
    small_italic_tags = ['<pos>$</pos>', '<singf>$</singf>', '<specif>$</specif>']

    # Blue span tags
    blue_span_tags = [
        '<ant>$</ant>', '<er>$</er>', '<grp>$</grp>', '<headword>$</headword>',
        '<hypen>$</hypen>', '<intensi>$</intensi>', '<inv>$</inv>', '<isa>$</isa>',
        '<ref>$</ref>', '<sig>$</sig>', '<simto>$</simto>', '<stype>$</stype>',
        '<stypec>$</stypec>'
    ]

    # Green span tags
    green_span_tags = [
        '<branchof>$</branchof>', '<causedby>$</causedby>', '<causedbyp>$</causedbyp>',
        '<causes>$</causes>', '<causesp>$</causesp>', '<class>$</class>', '<cnvto>$</cnvto>',
        '<colf>$</colf>', '<compof>$</compof>', '<conseq>$</conseq>', '<consof>$</consof>',
        '<contains>$</contains>', '<contr>$</contr>', '<corr>$</corr>', '<cp>$</cp>',
        '<cref>$</cref>', '<divof>$</divof>', '<emits>$</emits>', '<ets>$</ets>',
        '<etsep>$</etsep>', '<fam>$</fam>', '<hascons>$</hascons>', '<kingdom>$</kingdom>',
        '<member>$</member>', '<members>$</members>', '<membof>$</membof>', '<ord>$</ord>',
        '<part>$</part>', '<partof>$</partof>', '<parts>$</parts>', '<phylum>$</phylum>',
        '<prod>$</prod>', '<prodby>$</prodby>', '<prodmac>$</prodmac>', '<prodp>$</prodp>',
        '<recipr>$</recipr>', '<sfield>$</sfield>', '<stage>$</stage>', '<stageof>$</stageof>',
        '<subclass>$</subclass>', '<subfam>$</subfam>', '<subord>$</subord>',
        '<suborder>$</suborder>', '<subphylum>$</subphylum>', '<usedby>$</usedby>',
        '<usedfor>$</usedfor>', '<uses>$</uses>', '<var>$</var>', '<varn>$</varn>'
    ]

    # Green italic span tags
    green_italic_tag = '<rj>$</rj>'

    # Subscript and superscript tags
    subscript_tags = ['<sub>$</sub>', '<subs>$</subs>']
    superscript_tags = ['<sup>$</sup>', '<supr>$</supr>', '<sups>$</sups>']

    # Square bracket tags
    square_bracket_tags = ['<mhw>{ $ }</mhw>', '<mstypec>$</mstypec>']

    # Plaintext tag
    plaintext_tag = '<qau>$</qau>'

    # Remove tags
    remove_tags = ['<!$!>', '<--$-->', '<nul>$</nul>']

    # Complex tags (preserve content as-is)
    complex_tags = [
        '<altname>$</altname>', '<altnpluf>$</altnpluf>', '<antiquetype>$</antiquetype>',
        '<blacklettertype>$</blacklettertype>', '<boldfacetype>$</boldfacetype>',
        '<bourgeoistype>$</bourgeoistype>', '<boxtype>$</boxtype>', '<clarendontype>$</clarendontype>',
        '<englishtype>$</englishtype>', '<extendedtype>$</extendedtype>', '<frenchelzevirtype>$</frenchelzevirtype>',
        '<germantype>$</germantype>', '<gothictype>$</gothictype>', '<greatprimertype>$</greatprimertype>',
        '<hwf>$</hwf>', '<longprimertype>$</longprimertype>', '<miniontype>$</miniontype>',
        '<nonpareiltype>$</nonpareiltype>', '<oldenglishtype>$</oldenglishtype>', '<oldstyletype>$</oldstyletype>',
        '<pearltype>$</pearltype>', '<picatype>$</picatype>', '<ptcl>$</ptcl>', '<q>$</q>',
        '<sansserif>$</sansserif>', '<scripttype>$</scripttype>', '<smpicatype>$</smpicatype>',
        '<subtypes>$</subtypes>', '<tr>$</tr>', '<tran>$</tran>', '<typewritertype>$</typewritertype>',
        '<universbold>$</universbold>', '<xlati>$</xlati>'
    ]

    # Process all tags
    tag_categories = [
        (preserve_tags, None),
        (bold_tags, '<b>$</b>'),
        (br_tags, '<br>$'),
        (special_cases, None),
        (italic_tags, '<i>$</i>'),
        ({paragraph_tag: '<p>$</p>'}, None),
        (small_tags, '<small>$</small>'),
        (small_text_tags, None),
        (point_tag, r'<small>(point\1.)</small> \2'),
        (small_italic_tags, '<small><i>$</i></small>'),
        (blue_span_tags, '<span style="color:blue;">$</span>'),
        (green_span_tags, '<span style="color:green;">$</span>'),
        ({green_italic_tag: '<span style="color:green;"><i>$</i></span>'}, None),
        (subscript_tags, '<sub>$</sub>'),
        (superscript_tags, '<sup>$</sup>'),
        (square_bracket_tags, '[$]'),
        ({plaintext_tag: '[plaintext]'}, None),
        (complex_tags, '"$"'),
    ]

    for tags, replacement in tag_categories:
        if isinstance(tags, dict):
            for pattern, repl in tags.items():
                if '$' in pattern:
                    pattern = pattern.replace('$', '(.*?)')
                    if '$' in repl:
                        repl = repl.replace('$', r'\1')
                    text = re.sub(pattern, repl, text, flags=re.DOTALL)
        elif isinstance(tags, list):
            for pattern in tags:
                if '$' in pattern:
                    escaped_pattern = re.escape(pattern).replace(r'\$', r'(.*?)')
                    if replacement and '$' in replacement:
                        repl = replacement.replace('$', r'\1')
                        text = re.sub(escaped_pattern, repl, text, flags=re.DOTALL)
        elif isinstance(tags, str):  # regex pattern
            if '$' in replacement:
                text = re.sub(tags, replacement, text, flags=re.DOTALL)

    # Process remove tags
    for pattern in remove_tags:
        if '$' in pattern:
            escaped_pattern = re.escape(pattern).replace(r'\$', r'.*?')
            text = re.sub(escaped_pattern, '', text, flags=re.DOTALL)

    return text

def format(line: str) -> str:
    if '\t' not in line:
        return line.strip()

    parts = line.split('\t', 1)
    word = parts[0]
    meaning = parts[1].strip()

    # Apply replacements in order
    meaning = match_add(meaning)
    meaning = match_replace(meaning)
    meaning = replace_symbols(meaning)
    meaning = replace_chars(meaning)
    meaning = match_convert(meaning)
    meaning = replace_tags(meaning)
    meaning = match_remove(meaning)
    meaning = match_remove_except_allowed_tags(meaning)
    meaning = match_other(meaning)
    meaning = unescape(meaning)
    meaning = meaning.strip()

    return f"{word}\t{meaning}"

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results = []
    for line in lines:
        formatted_line = format(line)
        if formatted_line:
            results.append(formatted_line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))

    print(f"Processed {len(results)} lines")

if __name__ == '__main__':
    main()