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

def highlightWords(file, words_to_highlight, wrapper):
    with open(file, "r") as f:
        contents = f.read()

    result = []
    current_word = ""
    for i, ch in enumerate(contents + "0"):
        if ch.isalpha():
            current_word += ch

        if not ch.isalpha():
            if current_word.lower() in words_to_highlight:
                if contents[i:i + len(wrapper)] != wrapper:
                    current_word = wrapper + current_word.lower() + wrapper

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
            highlightWords(file, words_to_highlight, wrapper)

find_files_to_look_in()
