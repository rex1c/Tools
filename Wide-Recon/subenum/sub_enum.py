import os




def subdomain_enumertaion():
    file = open('domains' , "r")
    domain_lst = file.readlines()
    file.close()
    for i in domain_lst:
        i = i[:-1]
        # crtsh subs
        os.system('./crt.sh {} | grep -v "*" | sort -u >> {}.sub.crtsh'.format(i,i))
        
        # subfinder subs
        os.system(" subfinder -d {} -all -silent -o {}.sub.subfinder".format(i,i))
        
        # abusedb subs
        abuse_db_cmd = """ curl -s https://www.abuseipdb.com/whois/{} -H "user-agent: firefox" -b "abuseipdb_session=eyJpdiI6IlhhMDl5SEtCN3RhT29rXC9KU2JqeEtRPT0iLCJ2YWx1ZSI6IlwvdkJ0WHIza1FRQmFmK05lSkZnUGtDbTFpYVZ6MzFPOWh4WFB1NUVHb0hDc0dTM3ZINGJzM1Zaem5FcVA1dFNNIiwibWFjIjoiNTM3OWE4ODczNjg2ZWE4NTM0ZmYwNGQ4NDI2NDczNjBlNzE0ZjcxYjRkODI1ZmU1NzY5YjM2YWE2MDYxYzAzMCJ9" | grep -E '<li>\w.*</li>' | sed -E 's/<\/?li>//g' >> {}.sub.abus.name""".format(i,i)
        os.system(abuse_db_cmd)
        f = open("{}.sub.abus.name".format(i) , "r")
        sub_name = f.readlines()
        f.close()
        for subname in sub_name :
            os.system(" echo {}.{} >> {}.sub.abus".format(subname[:-1],i,i))
        
        # combine all 
        os.system(" cat {}.sub.subfinder {}.sub.crtsh {}.sub.abus| sort -u >> {}.sub.providers.txt".format(i,i,i,i))
        os.system("rm {}.sub.abus.name {}.sub.subfinder {}.sub.crtsh {}.sub.abus".format(i,i,i,i))
        # making static wordlist
        wordlist = open("sub.merged.txt" , "w")
        with open('sub.merged', 'r') as f:
            for line in f:
                wordlist.writelines(f'{line.strip()}.{i}\n')
        wordlist.close()
        # start DNS brute-force
        # static 
        os.system(" shuffledns -list sub.merged.txt -d {} -r ./resolver -mode resolve -t 30 -silent -o {}.sub.static.txt".format(i,i))
        # dynamic  
        os.system(" cat {}.sub.providers.txt | dnsgen -w words.merged - | tee {}.sub.dnsgen.txt".format(i,i))
        os.system(" altdns -i {}.sub.providers.txt -w words.merged -o {}.sub.altdns.txt".format(i,i))
        os.system(" cat {}.sub.altdns.txt {}.sub.dnsgen.txt | sort -u >> {}.sub.combined.txt".format(i,i,i))
        os.system(" shuffledns -list {}.sub.combined.txt -d {} -r ./resolver -mode resolve -t 30 -silent -o {}.sub.dynamic.txt".format(i,i,i))
        os.system(" cat {}.sub.providers.txt {}.sub.static.txt {}.sub.dynamic.txt | sort -u >> {}.subs".format(i,i,i,i))
        os.system(" rm *.txt ")


# Name Resulotion & CDN Filteration 
def name_resultion():
    os.system("cut-cdn -ua")
    files = []

    for file in os.listdir('.'):
        if file.endswith('.subs'):
            files.append(file)

    # access *.subs files
    for subs in files:
        os.system("cat {} | dnsx -silent | sort -u >> {}".format(subs, subs[:subs.find('.subs')]+'.res'))

    # CDN Filteration
    files = []

    for f in os.listdir('.'):
        if f.endswith('.res'):
            files.append(f)

    # read *.res files
    for res in files:
        resolved = open(res , 'r')
        domain_lst = resolved.readlines()
        resolved.close()
        cdn = open(res[:res.find('.res')]+'.cdn' , 'w')
        for i in domain_lst:
            i = i[:-1]
            dnsx = os.popen("echo {} |  dnsx -resp-only -silent".format(i)).read()
            dnsx = dnsx.split('\n')
            out = os.popen("cut-cdn -i {} -silent".format(dnsx[0])).read()
            if out != '':
                cdn.writelines('{} [{}]\n'.format(i , dnsx[0]))


    os.system("rm *.subs")


subdomain_enumertaion()
name_resultion()
name_resultion()
name_resultion()
