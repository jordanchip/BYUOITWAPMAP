from pdb import set_trace as debugger
from datetime import timedelta, datetime
import csv

big_map = {}
global prev_user
prev_user = ""
minute_split = 60
global bad_dates
bad_dates = 0

def add_lat_long():
    with open('buildingGPS.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bl = row['BLDG']
            if bl not in big_map:
                big_map[bl] = [0 for x in xrange((MINUTES_IN_WEEK)/minute_split+2)]
            big_map[row['BLDG']][0] = row['lat']
            big_map[row['BLDG']][1] = row['lon']

def is_association(line):
    return 'association response' in line

def process_line(line):
    global bad_dates
    global prev_user
    words = line.split()

    #The end bracket is where the date begins
    end_bracket = words[0].index('>')
    if end_bracket == -1:
        end_bracket = 5

    bldg_indx = 3
    #Get date in format MMM_DD_HH_mm__ss
    if 'T' in words[0]:
        #ISO
        #Everything shifts
        bldg_indx = 1
        tmp_split = words[0][end_bracket+1:].split('T')
        date_split = map(int, tmp_split[0].split('-'))
        if '.' in tmp_split[1]:
            time_split = map(int, tmp_split[1][:tmp_split[1].index('.')].split(':'))
        else:
            time_split = map(int, tmp_split[1].split(':'))
        date = datetime(year=date_split[0], month=date_split[1], day=date_split[2],
                        hour=time_split[0], minute=time_split[1])
    else:
        date = ' '.join((words[0][end_bracket+1:], words[1], words[2]))
        if 'Nov' not in words[0]:
            return
        #This is only for november
        time_split = words[2].split(':')
        date = datetime(year=2016, month=11, day=int(words[1]), hour=int(time_split[0]), minute=int(time_split[1]))

    indx = date-datetime(year=2016, month=11, day=13)
    if indx.total_seconds() < 0:
        return
    indx = int(indx.total_seconds()/60/minute_split)
    #     place = words[3]
    #     mac = words[8]

    #     #Some buildings don't have the '-'
    #     try:
    #         bldg = place[0:place.index('-')]
    try:
        bldg = words[bldg_indx][0:words[bldg_indx].index('-')]
    except:
        #This is a wierd format
        return

    if bldg not in big_map:
        #Create a list, with 2 spots for the lat/long, followed
        #by a column for each subsection of time division we have made
        MINUTES_IN_WEEK = 60*24*7
        big_map[bldg] = [0 for x in xrange((MINUTES_IN_WEEK)/minute_split+2)]

    big_map[bldg][indx+2] += 1

    # try:
    #     date = ' '.join((words[0][end_bracket+1:], words[1], words[2]))
    #     if len(date) > 8:
    #         #Its in ISO format
    #         pass

    #     #Get rid of nasty october logs
    #     if 'oct' in date.lower():
    #         return

    #     #Get another date that we will use for our key as MM_DD_HH
    #     time_parts = map(int,words[2].split(':'))

    #     base_hour = str(time_parts[0]-(minute_split-1)/60)
    #     base_minute = str(time_parts[1]-time_parts[1]%minute_split)
    #     cleaned_time = ' '.join((base_hour,base_minute))

    #     hour_date = ' '.join((words[0][end_bracket+1:], words[1], cleaned_time))
    #     place = words[3]
    #     mac = words[8]

    #     #Some buildings don't have the '-'
    #     try:
    #         bldg = place[0:place.index('-')]
    #     except ValueError:
    #         return
    #     key = ' '.join((hour_date, bldg))
    #     user_key = ' '.join((hour_date, mac))

    #     #Don't let more than one user enter in a log per second
    #     if user_key == prev_user:
    #         return
    #     prev_user = user_key
        
    #     if key in big_map:
    #         big_map[key] += 1
    #     else:
    #         big_map[key] = 1
    # except Exception as e:
    #     bad_dates += 1
    #     debugger()
    #     return

csv_output = False

for i in range(7, 8):
    print "FILE: {}".format(i)
    line_num = 0
    #Input files look like this: forjohndata1.txt
    with open(''.join(('forjohndata', str(i), '.txt'))) as fl:
        for line in iter(fl.readline, ''):
            #Check progress
            if line_num % 100000 == 0:
                print "line_num:", line_num
            line_num += 1
            # print "ln:", line
            if is_association(line)
                process_line(line)

# if csv_output:
#     with open(''.join(('output', str(i), '.csv')), 'wb') as out:
#         writer = csv.writer(out)
#         csv_map = []
#         writer.writerows(big_map)

# else:
#     #Output data looks like this: output1.txt
#     with open(''.join(('output', '.txt')), 'w') as out:
#         for key in sorted(big_map.iterkeys()):
#             out.write(' '.join((str(key), ":", str(big_map[key]), '\n')))

print "bad_dates:", bad_dates