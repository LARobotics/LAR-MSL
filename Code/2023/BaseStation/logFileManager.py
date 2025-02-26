import re
from datetime import datetime
import pyperclip as pc


name = "./../Jogos/N_Toulon Semi.log"
# name = "./logs/2023_09/23_02-48-09.log"
# name = "./logs/2024_01/15_11-00-55.log"

# Print first line
with open(name) as f:
    first_line = next(f)
    first_line = first_line.replace(" - ", ';')
    first_line = first_line.replace(" | ", ';')
    first_line = first_line.replace('\n', '')
    first_line = first_line.split(';')
    print('First line:', first_line)
    # first_line[0] = "17:45:37"
    init_time = datetime.strptime(first_line[0], '%H:%M:%S')

    
send_count = 0
receive_count = 0
last_timestamp = None
send_1, send_2, send_3, send_4, send_5 = 0, 0, 0, 0, 0
receive_1, receive_2, receive_3, receive_4, receive_5 = 0, 0, 0, 0, 0
a = 0

with open(name) as f:
    for line in f:
        if a == 0:
            a = 1
        else:    
            line = line.replace(" - ", ';')
            line = line.replace(" | ", ';')
            line = line.replace('\n', '')
            line = line.split(';')
            # timestamp, command = line.split(' - ')
            timestamp = datetime.strptime(line[0], '%H:%M:%S')
            
            # timestamp, command = line.split(' - ')  
            if 'S' in line[3]:
                send_count += 1
                if '1' in line[2]:
                    send_1 += 1
                elif '2' in line[2]:
                    send_2 += 1
                elif '3' in line[2]:
                    send_3 += 1
                elif '4' in line[2]:
                    send_4 += 1
                elif '5' in line[2]:
                    send_5 += 1
            elif 'R' in line[3]:
                receive_count += 1
                if '1' in line[2]:
                    receive_1 += 1
                elif '2' in line[2]:
                    receive_2 += 1
                elif '3' in line[2]:
                    receive_3 += 1
                elif '4' in line[2]:
                    receive_4 += 1
                elif '5' in line[2]:
                    receive_5 += 1
                
            # if last_timestamp:
            #     time_diff = (timestamp - last_timestamp).total_seconds()
            #     print(f'{send_count/time_diff:.2f} S commands/sec') 
            #     print(f'{receive_count/time_diff:.2f} R commands/sec')
                
            last_timestamp = timestamp
      
# Print last line  
with open(name) as f:
    last_line = ''
    for line in f:
        last_line = line
        
    last_line = last_line.replace(" - ", ';')
    last_line = last_line.replace(" | ", ';')
    last_line = last_line.replace('\n', '')
    last_line = last_line.split(';')
    print('last_line:', last_line)
    
    final_time = datetime.strptime(last_line[0], '%H:%M:%S')

total_time = final_time - init_time
print(f'Seconds: {total_time.total_seconds()}')
print(f'Total S commands: {send_count}') 
print(f'Total S commands rate: {send_count/total_time.total_seconds()}') 
sent = [send_1, send_2, send_3, send_4, send_5]
for i, a in enumerate(sent):
    print(f'robot number {i+1} | {a} sent commands | {a/total_time.total_seconds()} Commands per second') 


print(f'Total R commands: {receive_count}')
print(f'Total R commands rate: {receive_count/total_time.total_seconds()}')
recv = [receive_1, receive_2, receive_3, receive_4, receive_5]
for i, a in enumerate(recv):
    print(f'robot number {i+1} | {a} recieved commands | {a/total_time.total_seconds()} Commands per second') 

a = f"{total_time.total_seconds()}\t{send_1}\t{send_2}\t{send_3}\t{send_4}\t{send_5}\t{receive_1}\t{receive_2}\t{receive_3}\t{receive_4}\t{receive_5}\t"
pc.copy(a)