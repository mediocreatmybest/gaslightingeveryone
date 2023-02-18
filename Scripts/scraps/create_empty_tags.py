import os
import glob

# Director
image_dir = '/home/beepboop/images'

# jpgs with glob
image_files = glob.glob(os.path.join(image_dir, '*.jpg'))

# Loop the loop
for image_file in image_files:
    # Get the base file name without the extension
    base_name = os.path.splitext(os.path.basename(image_file))[0]

    # Create text file with the same base name extension
    text_file = os.path.join(image_dir, base_name + '.tags')
    with open(text_file, 'w') as f:
        pass  # create empty file

    print(f"Beep Boop! Created text file {text_file}")
