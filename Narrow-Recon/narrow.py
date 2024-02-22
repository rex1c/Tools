import os
import time


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
    os.system("echo '127.0.0.1 {}' >> /etc/hosts".format(localhost))
    os.system("echo '{}' | gospider --other-source --include-subs --subs --quiet | sort -u |  grep -Eiv '\.(css|js|jpg|jpeg|png|svg|img|gif|exe|apk|mp4|flv|pdf|doc|ogv|webm|wmv|webp|mov|mp3|m4a|m4p|ppt|pptx|scss|tif|tiff|ttf|otf|woff|woff2|bmp|ico|eot|htc|swf|rtf|image|rf)' >> gospider.txt".format(s))
    os.system("sed -i  '/127.0.0.1/d' /etc/hosts")
    os.system("cat gospider.txt gau.txt | sort -u >> passive.narrow.txt")
    # Filter passive links by status code
    os.system("httpx -silent -l passive.narrow.txt -mc 200,301,302,303,304,403 -o passive.narrow")
    

    
    # Start Active Crawling
    os.system('scrapy runspider crawl.py -a start_urls="{}" -o crawl.csv -t csv'.format(s))
    os.system("tail -n +2 crawl.csv | sort -u |  grep -Eiv '\.(css|jpg|jpeg|png|svg|img|gif|exe|apk|mp4|flv|pdf|doc|ogv|webm|wmv|webp|mov|mp3|m4a|m4p|ppt|pptx|scss|tif|tiff|ttf|otf|woff|woff2|bmp|ico|eot|htc|swf|rtf|image|rf)' >> crawl.txt")
    os.system("cat passive.narrow crawl.txt | sort -u >> flink.txt")
    # Link Finder (JS)
    file = open("flink.txt", "r")
    flink_domains = file.readlines()
    for links in flink_domains :
        link = links[:-1]
        os.system("python3 linkfinder.py -i {} -d -o cli | sort -u | grep -Eiv '\.(css|jpg|jpeg|png|svg|img|gif|exe|apk|mp4|flv|pdf|doc|ogv|webm|wmv|webp|mov|mp3|m4a|m4p|ppt|pptx|scss|tif|tiff|ttf|otf|woff|woff2|bmp|ico|eot|htc|swf|rtf|image|rf)' >> linkfinder.txt".format(link))
        time.sleep(0.70710678118)
    
    # Filter Links (Link Finder)  
    linkfinder_file = open("linkfinder.txt" , "r")
    linkfinder_domains = linkfinder_file.readlines()
    link_filtered = []
    pure_link = []
    for flinks in linkfinder_domains:
        flink = flinks[:-1]
        if flink[:4] == "http" or flink[0] == "/":
            link_filtered.append(flink)
        else:
            pass

    for l in link_filtered:
        if l[0] == "h" and l.find(s) != -1 :
            pure_link.append(l)
        
        elif l[0] == "/":
            pure_link.append(s+l)

        else:
            pass
    
    final = open("final.txt" , "w")
    for final_link in pure_link:
        final.writelines(final_link+"\n")
    final.close()


# Clean Dir
os.system("cat flink.txt final.txt | sort -u >> active.narrow")
os.system("rm -rf *.txt")
os.system("rm -rf *.csv")
os.system("rm -rf __pycache__")




# Grab All Links
os.system("cat active.narrow passive.narrow | sort -u >> links.narrow")
# Extract Parameter (Magic Parameter)
os.system("python3 magicparam.py | sort -u >> parameters.narrow")
