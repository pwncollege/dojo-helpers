import os
from collections import deque

# Change wrapper
wrapper = "`"
# Add paths to ignore
paths_to_ignore = []
# Add files to look in
files_to_look_in = ["DESCRIPTION.md"]
# Add words to highlight
words_to_highlight = ["root", "mv", "rm"]
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


def highlight_words(file):
    with open(file, "r") as f:
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
                if contents[i:i + len(wrapper)] != wrapper:
                    current_word = wrapper + current_word[:len(current_word.strip(chars_to_strip))] + wrapper + current_word[len(current_word.strip(chars_to_strip)):]

            result.append(current_word)
            result.append(ch)
            current_word = ""

    with open(file, "w") as f:
        result.pop()
        f.write("".join(result))


def find_files_to_look_in():
    queue = deque(os.listdir())

    while len(queue):
        file = queue.pop()
        if os.path.abspath(file) in paths_to_ignore:
            continue

        if os.path.isdir(file):
            for temp_file in os.listdir(file):
                queue.append(os.path.join(file, temp_file))

        elif os.path.basename(file) in files_to_look_in:
            highlight_words(file)


find_files_to_look_in()
