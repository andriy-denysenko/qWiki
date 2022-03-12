import re

# Declare a dictionary to contain html tag to re mappings
tag_map = {}

# Headers: 1 to 6 #'s
for i in range(1, 7):
	tag_map[f"<h{i}>"] = [re.compile("^(" + ("#" * i) + r"\s+(?P<text>.*))$")]

# TODO: change order of closing tags
# All bold and italic: ***
tag_map["<strong><em>"] = [re.compile(r"(\*{3}(?P<text>.*?)\*{3})")]

# Bold: ** and __
tag_map["<strong>"] = [
    re.compile(r"((?<!\*)\*{2}(?!\*)(?P<text>.*?)(?<!\*)\*{2}(?!\*))"),
    re.compile(r"(_{2}(?P<text2>.*?)_{2})")
]

# Italic: * and _
tag_map["<em>"] = [
    re.compile(r"((?<!\*)\*{1}?(?!\*)(?P<text>.*?)(?<!\*)\*{1}(?!\*))"),
    re.compile(r"((?<!_)_{1}(?!_)(?P<text2>.*?)(?<!_)_{1}(?!_))")
]

# Strikethrough: ** and __
tag_map["<strike>"] = [re.compile(r"((?<!~)~{2}(?!~)(?P<text>.*?)(?<!~)~{2}(?!~))")]

# TODO: links
# TODO: marked lists
# TODO: paragraphs at start and after blank lines

s = """Should be a paragraph with _italic_ and *italic*. The second sentence has **bold** and __bold__.

Should start a paragraph with ***bold and italic***.

Should start a paragraph with **bold and _nested italic_**. The second sentence has _italic with **nested bold**_.
This is a new line but not a ~~paragraph~~.

# H1
## H2
### H3
#### H4
##### H5
###### H6

Should be a paragraph"""

def parse(md_str):
    out_html = ""
    paragraph_opened = False
    lines = md_str.split("\n")
    prev_line = None
    for line in lines:
        print(f"Line: '{line}'")
        if line != "" and line[0] in ["#", "*", "-"]:
            print(f"This is a header or a list item, not starting a paragraph.")
            paragraph_opened = False
        else:
            print(f"This is text")
            if line == "" and paragraph_opened:
                print(f"This is an empty line and paragraph has been opened.\n<<<Closing the paragraph.")
                out_html += "</p>\n"
                paragraph_opened = False
                prev_line = line
                print()
                continue

            print(f"prev_line = '{prev_line}'")

            if prev_line is None or prev_line == "":
                print(f">>>Starting a paragraph")
                out_html += '<p dir="auto">\n'
                paragraph_opened = True           

        for tag in tag_map:
            rxs = tag_map[tag]
            for rx in rxs:
                found = False
                # TODO: walk through the string with ungreedy patterns
                # TODO: matching and replacing one by one using positions
                matches = rx.findall(line)
                for match in matches:
                    text = ""
                    text_to_replace = ""
                    if len(match) > 0:
                        found = True

                        if type(match) is str:
                            text = match

                        else:
                            text_to_replace = match[0]
                            for result in match:
                                if result != "" and result != text_to_replace:
                                    text = result
                                    break
                        print(f"text = '{text}'")

                        closing_tag = ""

                        if tag == "<strong><em>":
                            closing_tag = "</em></strong>"
                        else:
                            closing_tag = tag.replace("<", "</")

                        line = line.replace(text_to_replace, f"{tag}{text}{closing_tag}")
                        #end for
        prev_line = line
        # Append the processed line
        out_html += line + "\n"
        print()

    # Close a paragraph if opened
    if paragraph_opened:
        out_html += "</p>"

    return out_html

if __name__ == '__main__':
    file = open("tmp.txt", "w")
    file.write(parse(s))
    file.close()
    file = open("tmp.txt", "r")
    print(file.read())