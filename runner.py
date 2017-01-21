from pdb import set_trace as debugger

big_map = {}
seen_users = set()

def process_line(line):
    words = line.split()
    end_bracket = words[0].index('>')
    if end_bracket == -1:
        end_bracket = 5
    date = ' '.join((words[0][end_bracket+1:], words[1], words[2]))
    if 'oct' in date.lower():
        return
    hour_date = '_'.join((words[0][end_bracket+1:], words[1], words[2][:2]))
    place = words[3]
    mac = words[8]
    try:
        bldg = place[0:place.index('-')]
    except ValueError:
        return
    key = '_'.join((hour_date, bldg))
    user_key = '_'.join((hour_date, mac))
    if user_key in seen_users:
        return
    seen_users.add(user_key)
    if key in seen_users:
        return
    if key in big_map:
        big_map[key] += 1
    else:
        big_map[key] = 1
    # print "date:", date
    # print "hour_date:", hour_date
    # print "key:", key
    # print ""

for i in range(1, 2):
    line_num = 0
    #Input files look like this: forjohndata1.txt
    with open(''.join(('forjohndata', str(i), '.txt'))) as fl:
        for line in iter(fl.readline, ''):
            #Check progress
            if line_num % 100000 == 0:
                print "line_num:", line_num
            line_num += 1
            print "ln:", line
            
            process_line(line)
    #Output data looks like this: output1.txt
    with open(''.join(('output', str(i), '.txt')), 'w') as out:
        for key in sorted(big_map.iterkeys()):
            out.write(' '.join((str(key), ":", str(big_map[key]), '\n')))

