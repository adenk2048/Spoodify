from collections import defaultdict
r = open('song_history.in')
t = r.readlines()

t = [i.split() for i in t]
t = [[i[0], float(i[1])] for i in t]

count = defaultdict(float)
for i in t:
    count [i[0]] += i[1]

count = dict( sorted(count.items(), key = lambda item: item[1],reverse = True))

for i in count.keys():
    print(i)
    print(count[i],"seconds listened\n")
