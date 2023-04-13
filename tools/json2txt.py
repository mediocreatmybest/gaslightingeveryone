import json
import re
import argparse

from pathlib import Path
from func import json_extract, list2String # Local function script
from tqdm import tqdm

# Create the arg parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--captiondir', type=str,
 help='Image directory to caption', metavar='c:\images', required=True)
# Add arguments to disable unwanted data
parser.add_argument('--disable-title', action='store_true',
 help='Set this option to disable Title', required=False)
parser.add_argument('--disable-desc', action='store_true',
 help='Set this option to disable descriptions', required=False)
parser.add_argument('--disable-altdesc', action='store_true',
 help='Set this option to alt disable descriptions', required=False)
parser.add_argument('--disable-tags', action='store_true',
 help='Set this option to disable tags', required=False)
parser.add_argument('--disable-url', action='store_true',
 help='Set this option to disable urls', required=False)
parser.add_argument('--remove-hash', action='store_true',
 help='Set this option to filter hash symbol from tags', required=False)
parser.add_argument('--disable-exif', action='store_true',
 help='Set this option to disable exif data', required=False)
parser.add_argument('--append', action='store_true',
 help='Set this option to append the files to prevent overwriting', required=False)

# Add debug option to help disable save and prints out useful variables
parser.add_argument('--debug', action='store_true',
 help='Disables Saving files, prints output locations', required=False)

# Parse the argument
cmd_args = parser.parse_args()

# Sets the Image and json directory from arguments
# Warning: this deletes the previous caption file

image_captions_path = Path(rf"{cmd_args.captiondir}")
image_captions_appended_file = "appended_captions.txt"
seperator = ", "

# Find all JSON files in the directory
json_files = list(image_captions_path.glob('**/*.json'))

for json_file in tqdm(json_files, desc="Creating txt files", unit="json2txts"):
    jsonfile = json_file.as_posix()
    image_captions_single_file_base_dir = json_file.parent.as_posix()
    # remove 1st extension
    image_captions_single_file_base_name = json_file.stem
    # remove the 2nd extension
    image_captions_single_file = json_file.with_suffix('').stem
    # Load json file with Path.
    data = json.loads(json_file.read_text(encoding='UTF-8'))


    # Define our json search with json_extract function
    iso = json_extract(data, 'iso')
    focal_length = json_extract(data, 'focal_length')
    model = json_extract(data, 'model')
    aperture = json_extract(data, 'aperture')
    shutter_speed = json_extract(data, 'shutter_speed')
    # Some predefined locations for camera info at 500px

    camera_info = data.get('camera_info', {})
    if camera_info is not None:
        camera_info = camera_info.get('friendly_name', "")
    else:
        camera_info = ""

    lens_info = data.get('lens_info', {})
    if lens_info is not None:
        lens_info = lens_info.get('friendly_name', "")
    else:
        lens_info = ""

    # Cludge json data together even if it isn't listed as exif
    # Check if value actually has useful data, there has to be a better way to do this...
    cludge_camera_data = []

    if camera_info:
        cludge_camera_info = (camera_info)
        cludge_camera_data.append(cludge_camera_info)

    if lens_info:
        cludge_lens_info = (lens_info)
        cludge_camera_data.append(cludge_lens_info)

    if iso:
        if iso[0]:
            cludge_iso = "ISO: " + str(iso[0])
            if cludge_iso != "ISO: ":
                cludge_camera_data.append(cludge_iso)

    if focal_length:
        if focal_length[0]:
            cludge_focal_length = "Focal Length: " + str(focal_length[0]) + "mm"
            if cludge_focal_length != "Focal Length: mm":
                cludge_camera_data.append(cludge_focal_length)

    if model:
        if model[0]:
            cludge_model = "Model is " + str(model[0])
            if cludge_model != "Model is ":
                cludge_camera_data.append(cludge_model)

    if aperture:
        if aperture[0]:
            cludge_aperture = "Aperture: ƒ/" + str(aperture[0])
            if cludge_aperture != "Aperture: ƒ/":
                cludge_camera_data.append(cludge_aperture)

    if shutter_speed:
        if shutter_speed[0]:
            cludge_shutter = "Shutter speed: " +str(shutter_speed[0])
            if cludge_shutter != "Shutter speed: ":
                cludge_camera_data.append(cludge_shutter)

    # Some basic checks if data exists in json data that we don't want to search for via nested search
    # Assign json category to variable, hopefully this makes it easier to select known json data structures.
    if "category" in data:
        json_category = (data['category'])
    else:
        json_category = ""
    # Global fields
    if "title" in data:
        title = (data['title'])
    else:
        title = ""
    if "description" in data:
        desc = (data['description'])
    else:
        desc = ""
    if "alt_description" in data:
        alt_desc = (data['alt_description'])
    else:
        alt_desc = ""
    if "tags" in data:
        tags = (data['tags'])
    else:
        tags = ""
    if "location" in data:
        locationlist = []
        city = json_extract(data, 'city')
        country = json_extract(data, 'country')
        for val in city:
            if val != None:
                locationlist.append(val)
        for val in country:
            if val != None:
                locationlist.append(val)
        location = list2String(locationlist)
    else:
        location = ""
    if "username" in data:
        username = (data['username'])
    else:
        username = ""
    # Reddit
    if "subreddit_name_prefixed" in data:
        subreddit = str(data['subreddit_name_prefixed'])
    else:
        subreddit = ""
    #Deviantart
    if "da_category" in data:
        da_category = (data['da_category'])
    else:
        da_category = ""
    # Artstation
    if json_category == "artstation":
        #as_full_name = json_extract(data, 'full_name')
        as_full_name = data['user']['full_name']
        as_username = json_extract(data, 'username')
        as_software = []
        as_software_list = data['software_items']
        for idx in as_software_list:
            as_software.append(idx['name'])
        as_categories = []
        as_categories_list = (data['categories'])
        for idx in as_categories_list:
            as_categories.append(idx['name'])
        as_mediums = []
        as_mediums_list = (data['mediums'])
        for idx in as_mediums_list:
            as_mediums.append(idx['name'])

    else:
        as_full_name = ""
        as_username = ""
        as_software = ""
        as_categories = ""
        as_mediums = ""

    # Catch null or nothing values
    if desc is None:
        desc = ""
    if title is None:
        title = ""
    if alt_desc is None:
        alt_desc = ""


    # Clear data if command line data if flagged as disabled
    if cmd_args.disable_exif is True:
        cludge_camera_data = []
    if cmd_args.disable_title is True:
        title = ""
    if cmd_args.disable_desc is True:
        desc = ""
    if cmd_args.disable_altdesc is True:
        alt_desc = ""
    if cmd_args.disable_tags is True:
        tags = ""


    # Remove URL if command line args demand it
    # Move this before other symbol filtering
    if cmd_args.disable_url is True:
    # Remove URLs? Not sure how this magic works.
        title = re.sub(r'\b(https?):\/\/([-A-Z0-9.]+)(\/[-A-Z0-9+&@#\/%=~_|!:,.;]*)?(\?[A-Z0-9+&@#\/%=~_|!:,.;]*)?','', title, flags=re.I)
        desc = re.sub(r'\b(https?):\/\/([-A-Z0-9.]+)(\/[-A-Z0-9+&@#\/%=~_|!:,.;]*)?(\?[A-Z0-9+&@#\/%=~_|!:,.;]*)?','', desc, flags=re.I)

    # Simple filtering, move me somewhere else...maybe into a function please mr creator... existance is pain
    # Remove text, html href links, and new lines
    exclusionList = ['<.*>','^^','www.','.com','.org','.net','http://','https://','|','&nbsp;','&amp','&gt','"','PROCESS INFO','SOURCE INFO','IMAGE INFO','\n']
    #exclusionList = ''
    exclusions = '|'.join(exclusionList)
    desc = re.sub(exclusions, '', desc)
    title = re.sub(exclusions, '', title)
    # Some additional HTML tags and move some symbols around
    desc = re.sub(r';', ', ', desc)
    title = re.sub(r';', ', ', title)
    # remove explicit :wiki: word, unable to get this to work any other way
    desc = re.sub(r'\:wiki\:', ' ', desc)
    title = re.sub(r'\:wiki\:', ' ', title)
    # remove triple and double dots
    desc = re.sub(r'\.\.\.', ' ', desc)
    title = re.sub(r'\.\.\.', ' ', title)
    desc = re.sub(r'\.\.', ' ', desc)
    title = re.sub(r'\.\.', ' ', title)
    # Change any " ~ " to simple space
    desc = re.sub(r' ~ ', ' ', desc)
    title = re.sub(r' ~ ', ' ', title)
    # Change any " - " to simple space
    desc = re.sub(r' - ', ' ', desc)
    title = re.sub(r' - ', ' ', title)
    # remove some additional symbols
    desc = re.sub(r'[\[\]\#!~?\=\(\)*.:-]', '', desc)
    title = re.sub(r'[\[\]\#!~?\=\(\)*.:-]', '', title)
    # If we leave behind any double spaces, change them to single space.
    desc = re.sub(r', , ', ', ', desc)
    title = re.sub(r', , ', ', ', title)
    desc = re.sub(r',+', ',', desc)
    title = re.sub(r',+', ', ', title)
    desc = re.sub(r' +', ' ', desc)
    title = re.sub(r' +', ' ', title)

    # Final removal of all non-standard characters that break strings being selected, uncomment if needed.
    # desc = re.sub(r"[^-/().&' \w]|_", '', desc)
    # title = re.sub(r"[^-/().&' \w]|_", '', title)

    # move string into new variable to get camera cludge into output
    final_cludge_camera_data = list2String(cludge_camera_data)

    # move string into new variable to get tags into output
    final_tags_string = list2String(tags)

    # filter hash symbol if flagged in command arg
    if cmd_args.remove_hash is True:
        final_tags_string = re.sub(r'#', '', final_tags_string)

    # Make it easier on final output, append only existing results to a list
    appended_output = []

    if title != "":
        title = title.strip(', ')
        appended_output.append(title.strip())

    if desc != "":
        desc = desc.strip(', ')
        appended_output.append(desc.strip())

    if alt_desc != "":
        alt_desc = alt_desc.strip(', ')
        appended_output.append(alt_desc.strip())

    if location != "":
        appended_output.append(location.strip())

    if final_cludge_camera_data != "":
        appended_output.append(final_cludge_camera_data.strip())

    if subreddit != "":
        appended_output.append(subreddit.strip())

    if da_category != "":
        appended_output.append(da_category)

    if username != "":
        appended_output.append(username)

    # Artstation append

    # AS Software as a caption
    if len(as_software):
        as_software_str = 'Created with '
        as_software_str = as_software_str + list2String(as_software)
        appended_output.append(as_software_str)

    if len(as_categories):
        appended_output.append(list2String(as_categories))

    if len(as_mediums):
        appended_output.append(list2String(as_mediums))

    if as_full_name != "":
        appended_output.append(as_full_name)

    if as_username != "":
        appended_output.append(as_username[0])

    if tags != "":
        appended_output.append(final_tags_string.strip())

    return_appended_output = list2String(appended_output)

    # Trailing comma, please leave.
    return_appended_output = return_appended_output.strip(', ')

    # Folder and File locations
    single_files = Path(image_captions_single_file_base_dir, image_captions_single_file + ".txt")
    appended_file = Path(image_captions_path, image_captions_appended_file)
    # Appended file contents
    # Convert Path to string
    fullpath = str(Path(image_captions_single_file_base_dir, image_captions_single_file_base_name))
    appended_contents = fullpath + seperator + return_appended_output + "\n"

    # Debug print file name and locations
    if cmd_args.debug is True:
        print(single_files)
        print(appended_contents)

    # Check if debug is enabled to disable saving
    if cmd_args.debug is True:
        savefiles = False
    else:
        savefiles = True

    # Set write flag to overwrite
    writeflag = 'w'

    # Set append if cmd is flagged
    if cmd_args.append is True:
        writeflag = 'a'

    if cmd_args.debug is True:
        print('writeflag is: ', writeflag)

    # Create new file and overwrite if exists
    if savefiles is True:
        with open(single_files, f'{writeflag}', encoding='UTF-8') as f:
            f.write(return_appended_output)

        with open(appended_file, 'a', encoding='UTF-8') as fa:
            fa.write(appended_contents)