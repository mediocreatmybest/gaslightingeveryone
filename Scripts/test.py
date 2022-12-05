import argparse


#https://towardsdatascience.com/a-simple-guide-to-command-line-arguments-with-argparse-6824c30ab1c3
#https://docs.python.org/3/library/argparse.html



# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--downloader', type=str, choices=['gallery-dl', 'yt-dlp'], required=False)
parser.add_argument('--type', type=str, choices=['url', 'file'], required=False)
parser.add_argument('--txtmode', type=str, choices=['csv', 'plain'], required=False)
parser.add_argument('--sourcelist', type=str, required=True)
parser.add_argument('--directory', type=str, required=True)

# Parse the argument
cmd_args = parser.parse_args()
# Print "Hello" + the user input argument

if cmd_args.downloader == None: 
    print('Program type not selected, defaulting to gallery-dl')
    cmd_args.downloader = 'gallery-dl'
print('program selected is:', cmd_args.downloader)
print('program type is:', cmd_args.type)
print('program mode is:', cmd_args.txtmode)
print('program sourcelist is:', cmd_args.sourcelist)

gallery_extract_path = f'--directory {cmd_args.directory}'
ytdlp_dl_path = f'--output {cmd_args.directory}'

print(gallery_extract_path)
print(ytdlp_dl_path)