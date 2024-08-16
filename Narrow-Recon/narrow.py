import os

f = open("domains" , "r")
domains = f.readlines()
f.close()



for domain in domains :
    s = domain[:-1]
    # Start Passive Crawling
    os.system("gauplus '{}' | grep -Eiv '\.(css|jpg|jpeg|png|svg|img|gif|exe|js|apk|mp4|flv|pdf|doc|ogv|webm|wmv|webp|mov|mp3|m4a|m4p|ppt|pptx|scss|tif|tiff|ttf|otf|woff|woff2|bmp|ico|eot|htc|swf|rtf|image|rf)' | sort -u >> gau.txt".format(s))
    os.system("waybackurls '{}' | grep -Eiv '\.(css|jpg|jpeg|png|svg|img|gif|exe|js|apk|mp4|flv|pdf|doc|ogv|webm|wmv|webp|mov|mp3|m4a|m4p|ppt|pptx|scss|tif|tiff|ttf|otf|woff|woff2|bmp|ico|eot|htc|swf|rtf|image|rf)' | sort -u >> way.txt".format(s))
    os.system("cat gau.txt way.txt | sort -u >> {}.passive.narrow".foramt(s))
    os.system("rm -rf *.txt")
# Grab All Links
os.system("cat  *.passive.narrow | sort -u >> links.narrow")
# Extract Parameter (Magic Parameter)
os.system("python3 magicparam.py | sort -u >> parameters.narrow")
