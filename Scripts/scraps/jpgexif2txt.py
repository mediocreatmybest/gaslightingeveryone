import exifread

# Open the image file
file = open('image.jpg', 'rb')

# Return Exif tags
tags = exifread.process_file(file)

for tag in tags.items():
  print(tag)

for tag in tags.values():
  print(tag)

# Open a file to write the metadata
with open('image_metadata.txt', 'w') as f:
  for tag in tags.keys():
    # Write the tag name and value to the file
    f.write(f"{tag:25}: {tags[tag]}\n")

# Close the image file
file.close()

