import time
import math
import sys
import re
import os
from calc_stock import tranfer_stock_data_to_param

stock_data_path = './stock_data/'
strategy_path = './strategy/buy/'

RET_SUCCESS = 0
RET_INVALID_IN = 1
RET_FAILED = 2
RET_LAST_RECORD = 3
RET_0_CONDITION = 4
RET_INVALID_IDX = 0xffff

     
g_stock_records = []

#date
t = []
#open
o = []
#high
h = []
#low
l = []
#close
c = []
#volune
v = []
#updown_flag
f = []
#boday
b = []
#upper_line
u = []
#down_line
d = []
#percent
p = []

def sum(array):
    sum = 0
    for each in array:
        sum = sum + each
    return sum

def avg(array):
    if 0 == len(array):
        return 0
    return sum(array)/len(array)
    
def run_strategy(strategy_condition_list):
    if 0 == len(strategy_condition_list):
        return RET_FAILED
    global g_stock_records
    global t #date
    global o #open
    global h #high
    global l #low
    global c #close
    global v #volune
    global f #updown_flag
    global b #boday
    global u #upper_line
    global d #down_line
    global p #percent
    for condition in strategy_condition_list:
        try:
            eval_code = compile(condition, '', 'eval')
            ret = eval(eval_code)
        except:
            print condition + ' is invlid!!!'
            return RET_FAILED
        if ret != True:
            return RET_FAILED
    return RET_SUCCESS

def get_strategy_context(strategy_file):
    try:
        strategy_file_path = strategy_path + strategy_file + '.txt'
        flh = open(strategy_file_path, 'rb')
    except:
        print 'strategy file can not open %s'  %(strategy_file_path)
    
    strategy_con = []
    for eachline in flh:
        if '#' != eachline[0]:
            ms = re.match('^([\w\W]+)\r*\n*', eachline)
            if ms is not None:
                strategy_con.append(ms.group(1))
    flh.close()
    return strategy_con
            
def strategy_main(argv):
    #python strategy.py  startegy(1)  days(5)
    if 3 != len(argv):
        return
    strategy_name = argv[1]
    period_days = int(argv[2])
    file_list = os.listdir(stock_data_path)
    for stock_file in file_list:
        file_name = stock_data_path + stock_file
        global g_stock_records
        global t #date
        global o #open
        global h #high
        global l #low
        global c #close
        global v #volune
        global f #updown_flag
        global b #boday
        global u #upper_line
        global d #down_line
        global p #percent
        g_stock_records = tranfer_stock_data_to_param(file_name, period_days)
        t = []
        o = []
        h = []
        l = []
        c = []
        v = []
        f = []
        b = []
        u = []
        d = []
        p = []
        for i in range(len(g_stock_records)):
            t.append(g_stock_records[i][0])
            o.append(g_stock_records[i][1])
            h.append(g_stock_records[i][2])
            l.append(g_stock_records[i][3])
            c.append(g_stock_records[i][4])
            v.append(g_stock_records[i][5])
            f.append(g_stock_records[i][6])
            b.append(g_stock_records[i][7])
            u.append(g_stock_records[i][8])
            d.append(g_stock_records[i][9])
            p.append(g_stock_records[i][10])
        strategy_condition_list = get_strategy_context(strategy_name)
        print stock_file
        res = run_strategy(strategy_condition_list)
        if res == RET_SUCCESS:
            print stock_file + ' match successfully'
            stock_file_list = stock_file.split('.')
            fp = open(stock_file_list[0] + '_' + t[0] + '_s' + strategy_name + '.xls', 'w')
            fp.write('date\topen\thigh\tlow\tclose\tvolume\tupdown_flag\tbody_line\tupper_line\tdown_line\tpercent\n')
            for every_record in g_stock_records:
                out_string = ''
                for item in every_record:
                    out_string = out_string + str(item) + '\t'
                out_string = out_string + '\n'
                fp.write(out_string)
            fp.close()


if __name__ == '__main__':
    print 'The strategy run'
    print 'e.g, python strategy.py  strategy(1)  days(5)'
    
    strategy_main(sys.argv)
