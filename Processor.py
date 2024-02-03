import tkinter as tk
from tkinter import scrolledtext


def NaiveSM(Pattern, PatternLen, Text, TextLen):
    """Naive String Matching Algorithm"""
    indices = []
    for j in range(TextLen - PatternLen + 1):
        # Searching
        i = 0
        while i < PatternLen and Pattern[i] == Text[i + j]:
            i += 1
        if i == PatternLen:
            indices.append((j, j + PatternLen))
    return indices

def last(s):
    """Return the rightmost index of each character in the string."""
    last_index = {}
    for i, char in enumerate(s):
        last_index[char] = i
    return last_index

def BoyerMoore(Pattern, PatternLen, Text, TextLen):
    """Boyer-Moore Matching Algorithm"""
    last_index_dict = last(Pattern)
    indices = []
    s = 0
    while s <= TextLen - PatternLen:
        j = PatternLen - 1
        while j >= 0 and Text[j+s] == Pattern[j]:
            j = j - 1
        if j < 0:
            indices.append((s, s + PatternLen))
            s = s + 1
        else:
            k = last_index_dict.get(Text[j + s], -1)
            s = s + max(j - k, 1)
    return indices




def search_pattern():
    pattern = pattern_entry.get()
    text = text_area.get("1.0", tk.END)

    # Clear previous highlights
    text_area.tag_remove("highlight", "1.0", tk.END)

    matches = BoyerMoore(pattern, len(pattern), text, len(text))
    result_label.config(text=f"Pattern found at indices: {[match[0] for match in matches]}")

    # Highlight matches
    for match in matches:
        start, end = match
        text_area.tag_add("highlight", f"1.{start}", f"1.{end}")

    # Apply the tag configuration
    text_area.tag_config("highlight", background="yellow")


# Create the main window
root = tk.Tk()
root.title("Word Processor")

# Create UI elements
pattern_label = tk.Label(root, text="Enter Pattern:")
pattern_entry = tk.Entry(root)
search_button = tk.Button(root, text="Search", command=search_pattern)
text_area = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
result_label = tk.Label(root, text="Results will be displayed here.")

# Place UI elements in the window
pattern_label.pack(pady=5)
pattern_entry.pack(pady=5)
search_button.pack(pady=5)
text_area.pack(pady=10)
result_label.pack(pady=5)

# Start the GUI event loop
root.mainloop()
