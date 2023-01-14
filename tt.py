#!/usr/bin/env python
import argparse
import csv
from datetime import datetime, date
import json
from pprint import pprint
import random
import readchar
import time

RED = '\033[31m'
GREEN = '\033[32m'
END = '\033[0m'

DEFAULT_TYPE_NUM = 20

TYPE_LOG_NAME = "touch_type.csv"
RESULT_LOG_NAME = "touch_result.csv"


# -------------------------------------------------------------------
# define fuctions
# -------------------------------------------------------------------
def print_header(typing_num):
    """
    """
    print("-"*80)
    print(f"Touch Typing Practice ({typing_num} charactors)")
    print("-"*80)


def print_result(typing_num, match_num, miss_num, typing_time):
    """
    """
    match_rate = match_num / typing_num
    miss_rate = miss_num / typing_num

    print("-"*80)
    print("number of correct types: " + GREEN + f"{match_num}" + f" ({match_rate*100}%)" + END)
    print("number of miss types:    " + RED + f"{miss_num}" + f" ({miss_rate*100}%)" + END)
    print("time: " + f"{typing_time:.2f} sec" + f"   type speed: {typing_num/typing_time:.2f} char/sec")
    print("-"*80)


def write_typing(num, answer, input):
    """
    """
    now_date = date.today()
    now_time = datetime.now().strftime("%H:%M:%S")

    with open(TYPE_LOG_NAME, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([now_date, now_time, num, answer, input, answer==input])
    

def write_result(typing_num, match_num, miss_num, typing_time):
    """
    """
    now_date = date.today()
    now_time = datetime.now().strftime("%H:%M:%S")

    with open(RESULT_LOG_NAME, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([now_date, now_time, typing_num, match_num, miss_num, typing_time, typing_num/typing_time])



# -------------------------------------------------------------------
# parse and get command options
# -------------------------------------------------------------------
argp = argparse.ArgumentParser(description='default')
argp.add_argument('-n', '--num', help='number of practice typing')
args = argp.parse_args()
if args.num:
    typing_num = int(args.num)
else:
    typing_num = DEFAULT_TYPE_NUM


# 練習文字の読み込み
with open('alphabet.json', 'r') as f:
    test_chars_dict = json.load(f)
    test_chars = list(test_chars_dict.keys())


while True:
    print_header(typing_num)
    print("Press space to strat, press 'Q' to end.")
    command_key = readchar.readkey()

    if command_key == ' ':
        match_num = 0
        miss_num = 0

        typing_start_time = time.time() # 時間計測開始
        for i in range(typing_num):
            test_char = random.choice(test_chars)
            answer_key = test_chars_dict[test_char]
            print(f"{test_char}")
            print('--> ', end="")

            input_key = readchar.readkey()

            print("")
            if answer_key == input_key:
                COLOR = GREEN
                mark = "O"
                match_num = match_num + 1
            else:
                COLOR = RED
                mark = "X"
                miss_num = miss_num + 1
            
            print('input key is ' +  f"{input_key}" + COLOR + f" ({mark})" + END )
            write_typing(i, answer_key, input_key)

        typing_end_time = time.time() # 時間計測終了
        typing_time = typing_end_time - typing_start_time # タイピング時間
        
        print_result(typing_num, match_num, miss_num, typing_time)
        write_result(typing_num, match_num, miss_num, typing_time)

    elif command_key == 'q' or command_key == 'Q':
        break
