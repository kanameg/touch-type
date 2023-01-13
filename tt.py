#! /usr/bin/env python
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
DEFAULT_TYPE_KEY = 's'
TYPE_LOG_NAME = "touch_type.csv"
RESULT_LOG_NAME = "touch_result.csv"

# -------------------------------------------------------------------
# parse and get command options
# -------------------------------------------------------------------
argp = argparse.ArgumentParser(description='default')
argp.add_argument('-n', '--num', help='number of practice types')
args = argp.parse_args()
if args.num:
    type_num = int(args.num)
else:
    type_num = DEFAULT_TYPE_NUM

# 練習文字の読み込み
with open('alphabet.json', 'r') as f:
    test_chars_dict = json.load(f)
    test_chars = list(test_chars_dict.keys())


def header_print(type_num):
    """
    """
    print("-"*80)
    print(f"touch typing practice ({type_num} charactors)")
    print("-"*80)

while True:
    header_print(type_num)
    print("Press space to strat, press 'Q' to end.")
    command_key = readchar.readkey()

    if command_key == ' ':
        match_num = 0
        miss_num = 0
        today = date.today()
        with open(TYPE_LOG_NAME, 'a') as f:
            writer = csv.writer(f)

            time_start = time.time() # 時間計測開始
            for i in range(type_num):
                test_char = random.choice(test_chars)
                answer_key = test_chars_dict[test_char]
                print(f"{test_char}")
                print('--> ', end="")

                input_key = readchar.readkey()

                print("")
                if answer_key == input_key:
                    COLOR = GREEN
                    mark = "o"
                    match_num = match_num + 1
                else:
                    COLOR = RED
                    mark = "x"
                    miss_num = miss_num + 1
                print('input key is ' +  f"{input_key}" + COLOR + f" ({mark})" + END )
                now_time = datetime.now().strftime("%H:%M:%S")
                writer.writerow([today, now_time, i, answer_key, input_key, mark])            

        time_end = time.time() # 計測終了
        time_type = time_end - time_start

        match_rate = match_num / type_num
        miss_rate = miss_num / type_num
        print("-"*80)
        print("number of correct types: " + GREEN + f"{match_num}" + f" ({match_rate*100}%)" + END)
        print("number of miss types:    " + RED + f"{miss_num}" + f" ({miss_rate*100}%)" + END)
        print("time: " + f"{time_type:.2f} sec" + f"   type speed: {type_num/time_type:.2f} char/sec")
        print("-"*80)
        with open(RESULT_LOG_NAME, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([today, now_time, type_num, match_num, miss_num, time_type, type_num/time_type])

    elif command_key == 'q' or command_key == 'Q':
        break
