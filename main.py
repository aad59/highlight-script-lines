import pymupdf 
from get_lines import get_character_lines

FILE_PATH = "vera_stark.pdf"

def highlight_lines(character: str, file_name: str):
    # open document
    doc = pymupdf.open(file_name)
    # get paged lines
    lines = get_character_lines(character=character, file_name=file_name)
    page_num = 0

    # iterate through pages
    for page in doc:
        # get all strings to search for on the page
        matches = lines[page_num]
        # iterate through match strings
        for match in matches:
            # highlight all lines containing the given text
            to_highlight = page.search_for(match)
            start = to_highlight[0].tl
            stop = to_highlight[-1].br 
            page.add_highlight_annot(start=start, stop=stop)
        # continue to next page
        page_num += 1
    # save to new file
    doc.save(character.replace(".", "").lower()+".pdf")


if __name__ == "__main__":
    highlight_lines(character="GLORIA.", file_name=FILE_PATH)