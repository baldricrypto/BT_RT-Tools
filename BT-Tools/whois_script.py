# Script to whois a large number of domains. 
# Ensure that your list of domains is saved in a text file on seperate lines, in your current working directory. Ensure it is called domain_list.txt
# Will create an output file containing the response for each domain 

import subprocess
import threading
import logging


print("Finding whois.exe")
whois_directory = subprocess.run("where /r C:\ whois.exe", capture_output=True)
whois_directory = str(whois_directory.stdout, encoding='utf-8')
whois_directory = whois_directory.strip()
print("whois.exe found")

print("""
=============
Reading domain names
=============
""")

domains = []
with open("domain_list.txt", "r") as f: # Call text file domain_list.txt
    for line in f.readlines():
        domains.append(line.strip())

print("""
=============
Starting threading process
=============
""")

def thread_func(domain):
    with open("whois_output.txt", "a") as f:
        output = subprocess.run(f"{whois_directory} -v {domain}", capture_output=True)
        f.write(f"{domain}\n\n=====================================================================================\n\n{str(output.stdout, encoding='utf-8', errors='namereplace')}\n\n =====================================================================================\n\n")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    threads = list()
    for index,domain in enumerate(domains):
        logging.info("Main  : create and start thread %d.", index)
        x = threading.Thread(target=thread_func, args=(domain))
        threads.append(index)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        logging.info("Main    : thread %d done", index)

print("""
=============
All threads completed results output to whois_output.txt
=============
""")
 