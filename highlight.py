import os
from collections import deque

# Change wrapper
wrapper = "`"
# Add paths to ignore
paths_to_ignore = []
# Add files to look in
files_to_look_in = ["DESCRIPTION.md"]
# Add words to highlight
words_to_highlight = []
# Add wrappers (start and end) to ignore (e.g. "```console": "```")
wrappers_to_ignore = {
    "```console": "```",
}
# Add chars to strip (e.g. we want to match both `root` and `root.`, add `.` to the string chars_to_strip
# NOTE: make sure to have the stripped version in words_to_highlighted
chars_to_strip = "."
# Add word separators (e.g. " " if you want the program to check for matches on every space)
# NOTE: if you have a character as a word separator that also appears in one of the words_to_highlight,
# then the word will NOT be highlighted (so if we have "." and "root.", "root." will not be highlighted)
word_separators = [" ", "\n"]
# Choose whether you want to build words_to_highlight by searching for already highlighted words
search_for_highlighted_words = True
# Choose how many times a word has to be highlighted before it gets added to words_to_highlight in get_highlighted_words
# NOTE: only works when search_for_highlighted_words is True
minimum_instances_of_highlighted_word = 1

if search_for_highlighted_words:
    word_count = {}
    temp_words_to_highlight = set()


def highlight_words(current_file):
    with open(current_file, "r") as f:
        contents = f.read()

    result = []
    current_word = ""
    wrapping = None
    for i, ch in enumerate(contents + "0"):
        if wrapping:
            if contents[i:i + len(wrappers_to_ignore[wrapping])] == wrappers_to_ignore[wrapping]:
                wrapping = None

        for key, value in wrappers_to_ignore.items():
            if contents[i:i + len(key)] == key:
                wrapping = key

        if ch not in word_separators and i < len(contents):
            current_word += ch

        else:
            if current_word.strip(chars_to_strip) in words_to_highlight and not wrapping:
                current_word = (wrapper + current_word[:len(current_word.strip(chars_to_strip))]
                                + wrapper + current_word[len(current_word.strip(chars_to_strip)):])

            result.append(current_word)
            result.append(ch)
            current_word = ""

    with open(current_file, "w") as f:
        result.pop()
        f.write("".join(result))


def get_highlighted_words(current_file):
    with open(current_file, "r") as f:
        contents = f.read()

    contents += "0"
    wrapping = None
    word_to_highlight = ""
    i = 1
    while i < len(contents):
        if wrapping:
            if contents[i - len(wrapping):i] == wrapping and not contents[i].isalpha():
                wrapping = None

            i += 1
            continue

        if len(word_to_highlight) > 0:
            if contents[i:i + len(wrapper)] == wrapper:
                if word_to_highlight in word_count:
                    word_count[word_to_highlight] += 1
                else:
                    word_count[word_to_highlight] = 1

                if word_count[word_to_highlight] >= minimum_instances_of_highlighted_word:
                    temp_words_to_highlight.add(word_to_highlight)

                word_to_highlight = ""
                i += len(wrapper) + 1
                continue

            word_to_highlight += contents[i]

        if contents[i - len(wrapper):i] == wrapper:
            if not wrapping:
                for wrapper_to_ignore, key in wrappers_to_ignore.items():
                    if contents[i - 1:len(wrapper_to_ignore)] == wrapper_to_ignore:
                        wrapping = key

                if wrapping:
                    continue

            word_to_highlight += contents[i]

        i += 1


def find_files_to_look_in():
    queue = deque(os.listdir())
    files = []

    while len(queue):
        current_file = queue.pop()
        if os.path.abspath(current_file) in paths_to_ignore:
            continue

        if os.path.isdir(current_file):
            for temp_file in os.listdir(current_file):
                queue.append(os.path.join(current_file, temp_file))

        elif os.path.basename(current_file) in files_to_look_in:
            if search_for_highlighted_words:
                get_highlighted_words(current_file)
                files.append(current_file)
            else:
                highlight_words(current_file)

    return files


files_found = find_files_to_look_in()


if search_for_highlighted_words:
    words_to_highlight = list(temp_words_to_highlight)
    for file in files_found:
        highlight_words(file)
