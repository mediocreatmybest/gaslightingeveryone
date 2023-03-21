import json
import re
# Load JSON
with open('input.json') as f:
    data = json.load(f)
# input
selected_subcategories = input("Enter a comma-separated list of subcategories to include: ").split(",")
# get values
subcategories_values = [data["mediums"].get(subcategory, []) for subcategory in selected_subcategories]
# format function
def format_caption(key, value):
    return f"{key.title()}: {value}"

# write to file
with open('output.txt', 'w') as f:
    # Enumerate each subcat (can't get this working)
    for i, subcategory_values in enumerate(subcategories_values):
        key = selected_subcategories[i]
        caption = format_caption(key, subcategory_values)
        print(caption)
        f.write(caption)