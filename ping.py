# 2022-03-20    ERSN    v.1.0   Ping
# 2022-03-22    ERSN    v.1.1   Added check if os is windows/linus to alter command.
#                               The core ping command sp.Popen() changed to sp.check_output() in attempt to avoid CMD windows to open shortly for each ping.
# 2022-03-23    ERSN    v.1.2   Added socket and IP address validation to user input. Added small delay between pings.
# 2022-03-24    ERSN    v.1.3   check_output will fail occasionally so try/except added to hopefully avoid unwanted stop of ping sequence.

#import os
from datetime import datetime, timedelta
import time
import subprocess as sp
import threading as th
import platform as pf
import socket

class Ping:

    def __init__(self, ip_list_str, ping_delay, stop_n_pings, stop_n_hours, save_path):

        self.ip_list_str = ip_list_str
        self.ping_delay = ping_delay
        self.stop_n_pings = stop_n_pings
        self.stop_n_hours = stop_n_hours
        self.save_path = save_path

        if self.ping_delay < 5:
            self.ping_delay = 5
        elif self.ping_delay > 3600:
            self.ping_delay = 3600
        if self.stop_n_pings < 0:
            self.stop_n_pings = 0
        if self.stop_n_hours < 0:
            self.stop_n_hours = 0

        self.start_date = datetime.today()
        self.start_date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        self.end_date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        
        self.ping_sequence_active = 0
        self.n_pings_total = 0
        self.stop_date = datetime.now() + timedelta(hours=self.stop_n_hours)

        self.ip_list_str_split = self.ip_list_str.split(',')
        self.ip_list = []
        for ip in self.ip_list_str_split:
            self.ip_list.append(ip)
        
        self.platform_specific_param =  '-n' if pf.system().lower()=='windows' else '-c'

        #self.print_data()
    
    def print_data(self):
        print('self.ip_list_str', self.ip_list_str)
        print('self.ping_delay', self.ping_delay)
        print('self.stop_n_pings', self.stop_n_pings)
        print('self.stop_n_hours', self.stop_n_hours)
        print('self.save_path', self.save_path)
        print('self.start_date', self.start_date)
        print('self.start_date_str', self.start_date_str)
        print('self.end_date_str', self.end_date_str)
        print('self.ping_sequence_active', self.ping_sequence_active)
        print('self.n_pings_total', self.n_pings_total)
        print('self.stop_date', self.stop_date)
        print('self.ip_list', self.ip_list)
        print('self.platform_specific_param', self.platform_specific_param)

    def valid_ip(self, address):
        try: 
            socket.inet_aton(address)
            return True
        except:
            return False

    def ping(self):

        self.n_pings_total += 1
        txt_list = []

        for ip in self.ip_list:
            
            if self.valid_ip(ip) == True:
                # valid IP

                # 1 ping method
                '''response = os.popen(f"ping -n 1 -w 2 {ip}").read()
                ping_data_str_1_line = response.replace("\n", " ")
                ping_data_str_1_line = ping_data_str_1_line.replace('Ping statistics',';Ping statistics').replace(',Approximate',';Approximate')'''

                # 2 ping method
                '''response = sp.Popen(f"ping -n 1 -w 2 {ip}", stdout=sp.PIPE)
                ping_data_bytes = response.communicate()[0]
                ping_data_str = ping_data_bytes.decode('utf-8')
                ping_data_str_1_line = "".join(ping_data_str.splitlines()).replace('Ping statistics',';Ping statistics').replace(',Approximate',';Approximate')'''

                # 3 ping method
                command = ['ping', self.platform_specific_param, '1 -w 2', ip]
                #  check_output will fail occasionally so try/except added to hopefully avoid unwanted stop of ping sequence
                try:
                    ping_data_bytes = sp.check_output(command, shell=False)
                    ping_data_str = ping_data_bytes.decode('utf-8')
                    ping_data_str_1_line = "".join(ping_data_str.splitlines()).replace('Ping statistics',';Ping statistics').replace(',Approximate',';Approximate')
                except:
                    ping_data_str_1_line = "Ping command failed."
                
                txt = ''
                txt += ip + ';'
                txt += str(self.n_pings_total) + ';'
                txt += datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ';'
                txt += str(ping_data_str_1_line) + '\n'
                
                txt_list.append(txt)
            
            else:
                # invalid IP
                txt = ''
                txt += ip + ';'
                txt += str(self.n_pings_total) + ';'
                txt += datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ';'
                txt += 'Invalid IP' + '\n'
                txt_list.append(txt)
            
            if len(self.ip_list) > 1:
                time.sleep(0.5) # wait half a second between pings for multiple IP adresses

        return txt_list
    
    def start_ping_sequence(self):

        self.n_pings_total = 0
        self.ping_sequence_active = True
        self.start_date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

        if self.save_path != '':
            path = self.save_path + '/ping sekvens fra ' + self.start_date_str +'.csv'
            if self.n_pings_total == 0:
                f1 = open(path, 'a')
                f1.write('IP;Ping nummer;Dato;Ping svar;Ping pakker;Ping tider \n')
                f1.close()

        def go():
            while self.ping_sequence_active == True:

                txt_1 = self.ping()
                for x in range(len(txt_1)):
                    f1 = open(path, 'a')
                    f1.write(txt_1[x])
                    f1.close()
                
                if self.n_pings_total >= self.stop_n_pings and self.stop_n_pings != 0:
                    self.stop_ping_sequence()
                if datetime.today() > self.stop_date and self.stop_n_hours != 0:
                    self.stop_ping_sequence()

                if self.ping_sequence_active == True:
                    time.sleep(self.ping_delay)
        
        if self.save_path != '' and len(self.ip_list) >= 1:
            th.Thread(target=go).start()
    
    def stop_ping_sequence(self):
        self.ping_sequence_active = False
        self.n_pings_total = 0
        self.end_date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')