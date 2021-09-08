import requests

#read lines from the file to a list
with open('logs/videolinks.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

#give a name and url to download the mp4
def downloadfile(name,url):
    name=name+".mp4"
    #http get request
    r=requests.get(url)
    print ("****Connected****")

    #open a file with "".mp4
    f=open(name,'wb')
    print ("Donloading.....")

    #download the chunks from the webpage (if it is needed)
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    print ("Done")
    #close and go next
    f.close()

#iterates the loop with indexes, the index is appended to the video_ string to give them all unique names.
for i,j in enumerate(lines):
    downloadfile(("video_"+str(i)), j)
