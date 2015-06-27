import os 
import time
import math
import sys
import re

#date  open  high  low  close  volume  updown_flag  body_line  upper_line  lower_line  percent

#record = open  high  low  close

def calc_upper_shadow(record):
    open,high,low,close = record
    tmp = max(open, close)
    upper_line = high - tmp
    return upper_line

def calc_lower_shadow(record):
    open,high,low,close = record
    tmp = min(open, close)
    lower_line = tmp - low
    return lower_line

def calc_up_down(record):
    open,high,low,close = record
    if open >= close:
        return 0
    else:
        return 1

def calc_body_line(record):
    open,high,low,close = record
    body_line = max(open, close) -  min(open, close)
    return body_line

def calc_stock_param(record):
    if record == []:
        return []
        
    open,high,low,close = record
    upper_line = calc_upper_shadow(record)
    lower_line = calc_lower_shadow(record)
    updown = calc_up_down(record)
    body_line = calc_body_line(record)
    percent = (body_line/open)*100
    return [updown, body_line, upper_line, lower_line, percent]


def calc_stock_days_param(days_stock_records):
    if 0 == len(days_stock_records):
        return []
        
    out_calc_days_stock_param = []
    #date  open  high  low  close  volume  updown_flag  body_line  upper_line  lower_line  percent
    volume = 0
    record_num = len(days_stock_records)
    time_stamp = days_stock_records[record_num - 1][0]
    open = days_stock_records[record_num -1][1]
    close = days_stock_records[0][4]
    high = days_stock_records[0][2]
    low = days_stock_records[0][3]
    for each_record in days_stock_records:
        if each_record[2] > high:
            high = each_record[2]

        if each_record[3] < low:
            low = each_record[3]
            
        volume = volume + each_record[5]

    record = [open, high, low, close]
    updown, body_line, upper_line, lower_line, percent = calc_stock_param(record)

    out_calc_days_stock_param = [time_stamp, open, high, low, close, volume, updown, body_line, upper_line, lower_line, percent]
    #print out_calc_days_stock_param
    return out_calc_days_stock_param
    
    
def get_history_stock_data_from_csv(file_name):
    try:
        hist = open(file_name, 'rb')
    except:
        print 'open %s failed' %(file_name)
    
    all_stock_history_data = []
    for eachline in hist:
        #Date   Open    High    Low     Close   Volume   Adjust Close
        m = re.match('\d{4}\-\d{2}\-\d{2}\,\d+\.*\d*,\d+\.*\d*,\d+\.*\d*,\d+\.*\d*,(\d+),\d+\.*\d*', eachline)
        if m is not None:
            stock_data = eachline.split(',')
            if int(m.group(1)) == 0:
                continue

            stock_info = ['date', 1.0, 2.0, 3.0, 4.0, 5.0]
            stock_info[0] = stock_data[0]
            for i in range(1,6):
                stock_info[i] = float(stock_data[i])
            all_stock_history_data.append(stock_info)
    hist.close()
    return all_stock_history_data

def tranfer_stock_data_to_param(file_name, days_num):
    all_stock_history_data = get_history_stock_data_from_csv(file_name)
    if [] == all_stock_history_data:
        return []
    
    stock_record_set = []
    count = 0
    out_param_set = []
    for each_record in all_stock_history_data:
        if count == days_num:
            param = calc_stock_days_param(stock_record_set)
            if [] != param:
                out_param_set.append(param)
            stock_record_set = []
            stock_record_set.append(each_record)
            count = 1
        else:
            stock_record_set.append(each_record)
            count = count + 1
    return out_param_set
    
if __name__ == "__main__":
    print 'This calculate k param test'
    file_name = '600000.csv'
    info = tranfer_stock_data_to_param(file_name, 2)
    
    for e in info:
        print e