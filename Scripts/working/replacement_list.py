def dict_replace(string, replacements):
    # Use a dictionary to replace specific words instead of re.sub
    for word, replacement in replacements.items():
        string = string.replace(word, replacement)
    return string

replacements = {
    "a cartoon": "a drawing",
    "word": "test",
    "cat": "dog"
}