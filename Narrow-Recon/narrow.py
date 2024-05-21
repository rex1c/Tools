import os

f = open("domains" , "r")
domains = f.readlines()
f.close()



for domain in domains :
    s = domain[:-1]
    if s[:5] == "https":
        localhost = s[8:]
    else:
        localhost = s[7:]
    # Start Passive Crawling
    os.system("gau '{}' | grep -Eiv '\.(css|jpg|jpeg|png|svg|img|gif|exe|js|apk|mp4|flv|pdf|doc|ogv|webm|wmv|webp|mov|mp3|m4a|m4p|ppt|pptx|scss|tif|tiff|ttf|otf|woff|woff2|bmp|ico|eot|htc|swf|rtf|image|rf)' | sort -u >> gau.txt".format(s))
    os.system("waybackurls '{}' | grep -Eiv '\.(css|jpg|jpeg|png|svg|img|gif|exe|js|apk|mp4|flv|pdf|doc|ogv|webm|wmv|webp|mov|mp3|m4a|m4p|ppt|pptx|scss|tif|tiff|ttf|otf|woff|woff2|bmp|ico|eot|htc|swf|rtf|image|rf)' | sort -u >> way.txt".format(s))
    os.system("echo '127.0.0.1 {}' >> /etc/hosts".format(localhost))
    os.system("echo '{}' | gospider --other-source --include-subs --subs --quiet | sort -u |  grep -Eiv '\.(css|js|jpg|jpeg|png|svg|img|gif|exe|apk|mp4|flv|pdf|doc|ogv|webm|wmv|webp|mov|mp3|m4a|m4p|ppt|pptx|scss|tif|tiff|ttf|otf|woff|woff2|bmp|ico|eot|htc|swf|rtf|image|rf)' >> gospider.txt".format(s))
    os.system("sed -i  '/127.0.0.1/d' /etc/hosts")
    os.system("cat gospider.txt gau.txt way.txt | sort -u >> passive.narrow.txt")
    # Filter passive links by status code
    os.system("httpx -silent -l passive.narrow.txt -mc 200,301,302,303,304,403 -o {}.passive.narrow".format(localhost))
    os.system("rm *.txt")    



# Grab All Links
os.system("cat  *.passive.narrow | sort -u >> links.narrow")
# Extract Parameter (Magic Parameter)
os.system("python3 magicparam.py | sort -u >> parameters.narrow")
