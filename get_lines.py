import pymupdf
import re

def get_character_lines(character: str, file_name: str):
    # open file
    doc = pymupdf.open(file_name)

    # maintain dictionary for all lines found per page
    paged_lines = {}
    page_num = 0
    last_speaker = False

    # iterate through all pages in the document
    for page in doc:
        # grab the text and remove page numbers, cut-off words and newline chars
        text = page.get_text()
        text = re.sub(pattern="^[0-9]+", repl="", string=text)
        text = re.sub(pattern="-\n", repl="", string=text)
        text = re.sub(pattern="\n", repl=" ", string=text)
        text = re.sub(pattern="ACT [A-Z]+", repl="", string=text)
        text = re.sub(pattern="Scene [A-Z]+", repl="", string=text)

        # find all line indicators        
        lines = list(re.finditer(pattern="[A-Z]+[\s[A-Z]+]*\.", string=text))

        # keep track of all lines for the character
        character_lines = []

        # if the first line is a continuation from previous page, add to list
        if last_speaker and lines != []:
            character_lines.append(text[:lines[0].span()[0]].strip())

        # iterate through all line indicators
        for i in range(len(lines)):
            # reset boolean value
            last_speaker = False
            line = lines[i]

            # get line indicator
            match = text[line.span()[0]:line.span()[1]]
            
            # if not a line for target character, keep searching
            if match != character:
                continue
            
            # if not at end of page, use next line start as current line stop
            if i != len(lines) - 1:
                character_lines.append(text[line.span()[0]:lines[i+1].span()[0]].strip())
            # if at end of page, use end of page as current line stop
            else:
                last_speaker = True
                character_lines.append(text[line.span()[0]:len(text)].strip())

        # remove any whitespace
        paged_lines[page_num] = [line for line in character_lines if line != "" and line != " " and line != "\n"]
        # continue to next page
        page_num +=1

    return paged_lines