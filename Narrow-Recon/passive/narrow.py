import os

f = open("domains" , "r")
domains = f.readlines()
f.close()



for domain in domains :
    s = domain[:-1]
    # Start Passive Crawling
    os.system("gauplus '{}' | grep -Eiv '\.(css|jpg|jpeg|png|svg|img|gif|exe|js|apk|mp4|flv|pdf|doc|ogv|webm|wmv|webp|mov|mp3|m4a|m4p|ppt|pptx|scss|tif|tiff|ttf|otf|woff|woff2|bmp|ico|eot|htc|swf|rtf|image|rf)' | sort -u >> gau.txt".format(s))
    os.system("waybackurls '{}' | grep -Eiv '\.(css|jpg|jpeg|png|svg|img|gif|exe|js|apk|mp4|flv|pdf|doc|ogv|webm|wmv|webp|mov|mp3|m4a|m4p|ppt|pptx|scss|tif|tiff|ttf|otf|woff|woff2|bmp|ico|eot|htc|swf|rtf|image|rf)' | sort -u >> way.txt".format(s))
    os.system("cat gau.txt way.txt | sort -u >> {}.passive.narrow".format(s))
    os.system("rm -rf *.txt")
# Grab All Links
os.system("cat  *.passive.narrow | sort -u >> all_links.narrow")
os.system("cat  all_links.narrow | httpx -silent -fc 400,401,402,403,404,405,406,500,501,502,503,504,505,506 >> links.narrow")
# Extract Parameter (Magic Parameter)
os.system("cat all_links.narrow | unfurl keys | sort -u >> url_params.txt")
os.system("python3 magicparam.py | sort -u >> magicparams.txt")
os.system("cat *.txt | sort -u >> params.narrow")
os.system("rm -rf *.txt")
