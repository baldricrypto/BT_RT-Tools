# Script to whois a large number of domains. 
# Ensure that your list of domains is saved in a text file on seperate lines, in your current working directory. Ensure it is called domain_list.txt
# Will create an output file containing the response for each domain 
# You will encounter some errors, for certain domains, this is due to being unable to decode the output into utf-8 - likely due to foreign languages etc.

# Currently the risk scores are not accurate if the date is in a different format to that which today's date is retrieved.
# The parsing function needs more work as it is pulling out extra data. 

import subprocess
import threading
import logging
import sys, getopt
import time
import os
from datetime import datetime
import dateutil
import dateutil.relativedelta

class domain:
    def __init__(self, domain_name, creation_date, risk_score) -> None:
        self.domain_name = domain_name
        self.creation_date = creation_date
        self.risk_score = risk_score
    def __str__(self) -> str:
        return (f"{self.domain_name}:{self.creation_date}:Risk Score = {self.risk_score}")
    
def help():
    return print(
"""
whois_script.py <flags> -i <input_file>

-i --input= : Input file, in line seperated txt format.
-t --text : Output pure whois data to a text file.
-a --all : View all domains and creation dates.
-r --risk : View domains of high risk, risk score is determined ONLY on how old the domain is nothing else, your own investigations should make final conclusion. 
        Risk score descriptions:
            0 - Very Low: Risk is very low as domain is over 10 years old.
            1 - Low: Risk is Low due to domain being over 5 years old
            2 - Medium: Risk is Medium due to domain being less than 5 years old but older than one year
            3 - High: Risk is high due to domain being less than 1 year old but older than 6 months
            4 - Very High: Risk is Very high due to domain being under 6 months old but older than 1 month
            5 - Extreme: Risk is extreme due to domain being less than 1 month old
-f --find : Find whois.exe location.
-h --help : Show help menu.
-w --web : Web version using requests module - coming soon.
"""
)

def find_whois_exe():
    print("Finding whois.exe")
    global whois_directory
    whois_directory = subprocess.run("where /r C:\ whois.exe", capture_output=True)
    whois_directory = str(whois_directory.stdout, encoding='utf-8')
    whois_directory = whois_directory.strip()
    print("whois.exe found")
    return whois_directory

def read_domain_list(input_file):
    global domain_dictionary
    print('Reading domain list')
    domain_dictionary = []
    with open(str(input_file), "r") as f:
        for line in f.readlines():
            domain_dictionary.append(line.strip())
    print('Domain list successfully read')
    return domain_dictionary

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MAY NEED RE JIGGING AFTER CHANGING TO A CLASS BASED PROGRAM
def output_all_data_to_text_file(domain,index):
    with open("whois_output.txt", "a") as f:
        output = subprocess.run(f"{whois_directory} -v {domain}", capture_output=True)
        f.write(f"{domain}\n\n=====================================================================================\n\n{str(output.stdout, encoding='utf-8', errors='namereplace')}\n\n =====================================================================================\n\n")
        #logging.info("Main    : thread %d done", index)

def output_all_data_to_text_file_thread_function():
    print('Running text output option, this includes a fresh whois run, please wait. :) ')
    threads = list()
    for index,domain in enumerate(domain_dictionary):
        #logging.info("Main  : create and start thread %d.", index)
        x = threading.Thread(target=output_all_data_to_text_file, args=(domain,index))
        threads.append(index)
        x.start()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

holder = {}

def whois_function(domain_to_whois,index):
    #print('Starting class creation')
    created_keywords = ['Created', 'created', 'Creation',  'creation', 'Registered', 'registered', '[Created on]', '[Registered Date]', ]
    domain_keywords = ['domain:', 'Domain:', 'Domain Name:', 'Domain name:']
    domain_name_for_class = ''
    creation_date_for_class = ''
    domain_name_for_key = ''

    output = subprocess.run(f"{whois_directory} -v {domain_to_whois}", capture_output=True)

    output_string = str(output.stdout, encoding='utf-8', errors='ignore')
    output_string_split = output_string.splitlines()

    for line in output_string_split:
        for word in domain_keywords:
            if word in line:
                domain_name_for_class = line.split(':')
                domain_name_for_class = domain_name_for_class[1]
                domain_name_for_key = domain_name_for_class.strip().upper()
        for word in created_keywords:
            if word in line:
                creation_date_for_class = line.split(':')
                try:
                    creation_date_for_class = str(creation_date_for_class[1].split('T')[0])
                except IndexError:
                    print(creation_date_for_class,'<---------------------- INDEXERROR RISEN HERE')
                #print(creation_date_for_class[1])
    if creation_date_for_class == '':
        risk_score = 'Undetermined'
        creation_date_for_class = 'No creation date present in whois data'
    else:
        risk_score = risk_score_generator(creation_date_for_class.strip())
    try:
        holder[domain_name_for_key]  = domain(domain_name=domain_name_for_class.lower().strip(),creation_date=creation_date_for_class.strip(),risk_score=risk_score)
    except IndexError:
        holder[domain_name_for_key]  = domain(domain_name=domain_name_for_class.lower().strip(),creation_date=creation_date_for_class.strip(),risk_score=risk_score)
    print(f'Class created for {holder[domain_name_for_key].domain_name} : {holder[domain_name_for_key].creation_date} : {holder[domain_name_for_key].risk_score}')
    return holder[domain_name_for_key]

def risk_score_generator(creation_date):
    converted_date = ''
    try:
        converted_date = datetime.strptime(str(creation_date), '%Y-%m-%d')
    except ValueError:
        print(creation_date)
    today = datetime.today()
    difference = dateutil.relativedelta.relativedelta(today,converted_date)
    if difference.years > 10:
        risk_score = '0 - Very Low'
    elif difference.years > 5:
        risk_score = '1 - Low'
    elif difference.years > 1 and difference.years < 5:
        risk_score = '2 - Medium'
    elif difference.months > 6:
        risk_score = '3 - High'
    elif difference.months < 6 and difference.months > 1:
        risk_score = '4 - Very High'
    else:
        risk_score = '5 - Extreme'
    return risk_score

def send_domains_from_domain_dictionary_to_who_is_exe_and_parse_results(domain_dictionary):
    print('Starting threads')
    global threads_complete
    threads_complete = False
    threads = list()
    for index,domain in enumerate(domain_dictionary):
        #logging.info("Main  : create and start thread %d.", index)
        x = threading.Thread(target=whois_function, args=(domain,index))
        threads.append(index)
        x.start()
    while threading.active_count() > 1:
        #print('Active threads : ', threading.active_count())
        threads_complete = False
        time.sleep(0.5)
    else:
        threads_complete = True
        return threads_complete

def all_domains_and_creation_dates_function():
    while threads_complete == False:
        time.sleep(1)
        print('Waiting for threads to complete')
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    sorted_holder_dictionary = dict(sorted(holder.items()))
    for key,value in sorted_holder_dictionary.items():
        if key == '':
            print('One or more domains had no whois data sorry, please collaborate with your list to determine which domains\n')
            continue
        print(f"{value.domain_name} : {value.creation_date} : {value.risk_score}")

def risk_domains_function():
    while threads_complete == False:
        time.sleep(1)
        print('Waiting for threads to complete')
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    sorted_holder_dictionary_by_values = sorted(holder.items(), key=lambda x:x[1].risk_score)

    for key,value in sorted_holder_dictionary_by_values:
        if value.risk_score == '5 - Extreme' or value.risk_score == '4 - Very High' or value.risk_score == '3 - High':
            print(f"{value.domain_name} : {value.creation_date} : {value.risk_score}")


    #for key,value in sorted_holder_dictionary_by_values:
    #    if key == '':
    #        print('One or more domains had no whois data sorry, please collaborate with your list to determine which domains\n')
    #        continue
    #    print(f"{value.domain_name} : {value.creation_date} : {value.risk_score}")

def help_flag():
    help()
    sys.exit()

def find_flag():
    find_whois_exe()

def all_flag():
    all_domains_and_creation_dates_function()

def text_flag():
    output_all_data_to_text_file_thread_function()

def risk_flag():
    risk_domains_function()

def web_flag():
    pass

def main(argv):
    input_file = ''
    text_flag_present,all_flag_present,risk_flag_present,find_flag_present,web_flag_present = False,False,False,False,False
    try:
        opts, args = getopt.getopt(argv, "htarfwi:", ['input=','text','all','risk','find','help','web'])
    except getopt.GetoptError:
        help_flag()
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            help_flag()
        elif opt in ('-w', '--web'):
            print('Web functionality to come please be patient :)')
            web_flag_present = True
            sys.exit()
        elif opt in ('-i', '--input'):
            input_file = arg
        elif opt in ('-t', '--text'):
            text_flag_present = True
        elif opt in ('-a', '--all'):
            all_flag_present = True
        elif opt in ('-r', '--risk'):
            risk_flag_present = True
        elif opt in ('-f', '--find'):
            find_flag_present = True
    if risk_flag_present and all_flag_present:
        print('Risk and All flag cannot be used together please choose one :)')
        sys.exit()
    if find_flag_present and web_flag_present:
        print('Web and find flags cannot be use together please choose one :)')
        sys.exit()
    if find_flag_present:
        find_flag()
    if risk_flag_present:
        send_domains_from_domain_dictionary_to_who_is_exe_and_parse_results(read_domain_list(input_file))
        risk_flag()
    elif all_flag_present:
        send_domains_from_domain_dictionary_to_who_is_exe_and_parse_results(read_domain_list(input_file))
        all_flag()
    elif text_flag_present:
        text_flag()
    else:
        print('No output flag detected :)')
        sys.exit()


main(sys.argv[1:])
