#import os
from datetime import datetime, timedelta
import time
import subprocess as sp
import threading as th

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
        
        #self.print_data()
    
    def print_data(self):
        print('1 ', self.ip_list_str)
        print('2 ', self.ping_delay)
        print('3 ', self.stop_n_pings)
        print('4 ', self.stop_n_hours)
        print('5 ', self.save_path)
        print('6 ', self.start_date)
        print('7 ', self.start_date_str)
        print('8 ', self.end_date_str)
        print('9 ', self.ping_sequence_active)
        print('10 ', self.n_pings_total)
        print('11', self.stop_date)
        print('12', self.ip_list)

    def ping(self):

        self.n_pings_total += 1
        txt_list = []

        for ip in self.ip_list:

            #response = os.popen(f"ping -n 1 -w 2 {ip}").read()
            response = sp.Popen(f"ping -n 1 -w 2 {ip}", stdout=sp.PIPE)
            ping_data_bytes = response.communicate()[0]
            ping_data_str = ping_data_bytes.decode('utf-8')
            ping_data_str_1_line = "".join(ping_data_str.splitlines()).replace('Ping statistics',';Ping statistics').replace(',Approximate',';Approximate')

            txt = ''
            txt += ip + ';'
            txt += str(self.n_pings_total) + ';'
            txt += datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ';'
            txt += str(ping_data_str_1_line) + '\n'
            
            txt_list.append(txt)

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
                if datetime.today() > self.start_date and self.stop_n_hours != 0:
                    self.stop_ping_sequence()

                if self.ping_sequence_active == True:
                    time.sleep(self.ping_delay)
        
        if self.save_path != '' and len(self.ip_list) >= 1:
            th.Thread(target=go).start()
    
    def stop_ping_sequence(self):
        self.ping_sequence_active = False
        self.n_pings_total = 0
        self.end_date_str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')