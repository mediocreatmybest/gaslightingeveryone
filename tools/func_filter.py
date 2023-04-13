import re

def strictfilter(textstring, string2remove):
    """ Simple Regex filter that does not ignore character case"""
    return re.sub(rf'{string2remove}', '', textstring)

def softfilter(textstring, string2remove):
    """ Simple regex filter that ignores character case """
    return re.sub(rf'{string2remove}', '', textstring, flags=re.I)

def filterspacing(textstring):
    """ Long easy to read filter, not unlike easy read filtering """
    textstring = re.sub(rf' - ', ' ', textstring)
    textstring = re.sub(rf'- ', ' ', textstring)
    textstring = re.sub(rf' -', ' ', textstring)
    textstring = re.sub(rf'-', ' ', textstring)
    textstring = re.sub(rf' – ', ' ', textstring)
    textstring = re.sub(rf'–', ' ', textstring)
    textstring = re.sub(rf' ; ', ' ', textstring)
    textstring = re.sub(rf'; ', ' ', textstring)
    textstring = re.sub(rf' ;', ' ', textstring)
    textstring = re.sub(rf';', ' ', textstring)
    textstring = re.sub(r'\|', ' ', textstring)
    textstring = re.sub(r' +', ' ', textstring)
    textstring = re.sub(r' +', ' ', textstring)
    textstring = re.sub(r', , ', ', ', textstring)
    textstring = re.sub(r', , ', ', ', textstring)
    textstring = re.sub(r',+', ',', textstring)
    textstring = re.sub(r', +', ', ', textstring)
    textstring = re.sub(r' , +', ', ', textstring)
    return (textstring)

# or maybe a group them together

def filter_spacing(textstring):
    """ Simple filtering on bad spacing from plain text """
    textstring = re.sub(r'[-–;|.~]+', ' ', textstring)
    textstring = re.sub(r'[ ]+', ' ', textstring)
    textstring = re.sub(r', , ', ', ', textstring)
    textstring = re.sub(r', , ', ', ', textstring)
    textstring = re.sub(r',+', ',', textstring)
    textstring = re.sub(r', +', ', ', textstring)
    textstring = re.sub(r' , +', ', ', textstring)
    textstring = textstring.strip()
    textstring = textstring.strip(',')
    textstring = textstring.strip(' ,')
    textstring = textstring.strip(', ')
    return (textstring)

def filter_urls(textstring):
    """ Magic regex to remove URLS from plain text """
    return (re.sub(r'\b(https?):\/\/([-A-Z0-9.]+)(\/[-A-Z0-9+&@#\/%=~_|!:,.;]*)?(\?[A-Z0-9+&@#\/%=~_|!:,.;]*)?','', textstring, flags=re.I))