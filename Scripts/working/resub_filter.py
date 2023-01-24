import re

def strictfilter(str2filter, str2remove):
    return re.sub(rf'{str2remove}', '', str2filter)

def softfilter(str2filter, str2remove):
    return re.sub(rf'{str2remove}', '', str2filter, flags=re.IGNORECASE)


filter_text = strictfilter("This is bob", "This is ")
print(filter_text)

soft_filter_text = softfilter("This is bob", "this is ")
print(soft_filter_text)