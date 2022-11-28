import os
import subprocess
from pathlib import Path

#configure download path 
image_captions_path = Path(r"c:\images")

#URL filters for supported websites (reddit, etc.)
reddit_top_all = '/top/?t=all'
reddit_top_month = '/top/?t=month'

subprocess.run(['gallery-dl', '--download-archive archivedata.txt', '--write-metadata','--sleep 2-4','--range 1-300','r:https:url.com/raw/text',])
subprocess.run(['gallery-dl', '--download-archive archivedata.txt', '--write-metadata','--sleep 2-4','r:https:url.com/raw/text',])