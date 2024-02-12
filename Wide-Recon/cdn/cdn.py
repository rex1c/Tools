import os

# Name Resulotion
# find *.subs files
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
        out = os.popen("cut-cdn -i {} -silent".format(i)).read()
        if out != '':
            cdn.writelines('{} [{}]\n'.format(i , out[:out.find('\n')]))


os.system("rm *.subs")

