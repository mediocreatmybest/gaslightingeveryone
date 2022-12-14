import glob
import os

#Gather all txt files
os.chdir(r'C:\Folder')

txtfiles = glob.glob('*.txt')
imagefiles = glob.glob('*.png')

# Open file3 in write mode
with open('text.txt', 'w', encoding="utf8") as outfile:
  
    # Iterate through list
    for textnames in txtfiles:
  
        # Open each file in read mode
        with open(textnames) as infile:
  
            # read the data from file1 and
            # file2 and write it in file3
            outfile.write(infile.read())
  
        # Add '\n' to enter data of file2
        # from next line
        outfile.write("\n")

# Open file3 in write mode
with open('imagefiles.txt', 'w', encoding="utf8") as outfile:
  
    # Iterate through list
    for imagenames in imagefiles:
  
  
        # Add '\n' to enter data of file2
        # from next line
        outfile.write("%s\n" % imagenames)



