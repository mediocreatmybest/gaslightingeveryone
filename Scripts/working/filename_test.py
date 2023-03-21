import os
from func import walk_path_plus

def create_captions(file_path, ext="txt", force=False, debug=False, encoding="utf-8"):
    """ Create captions with each file, we are ignore filtering, this can be done in the main() """
    base_name, _ = os.path.splitext(os.path.basename(file_path))
    caption_file_path = os.path.join(os.path.dirname(file_path), f"{base_name}.{ext}")

    if os.path.exists(caption_file_path) and not force:
        if debug:
            print(f"Caption file already exists for {file_path}: {caption_file_path}")
        # File exists, return True and exit
        return True
    # Try open file and write base name, print error if debug is enabled
    try:
        with open(caption_file_path, 'w', encoding=encoding) as f:
            f.write(base_name)
    except Exception as e:
        if debug:
            print(f"Error creating caption file for {file_path}: {str(e)}")
        return False

    if debug:
        print(f"Caption file created for {file_path}: {caption_file_path}")

    return True

# Director
image_dir = 'c:\\images'

# Images
image_files = walk_path_plus(image_dir, ext_filter=['.jpg', '.jpeg', '.png', '.bmp'], recursive=True)

# Loop the loop
for image_file in image_files:
    create_captions(image_files, ext="txt", force=False, debug=True)
