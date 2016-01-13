# see settings_copy.py for more info

import os
import sys

from pushyapp import settings
import time
import platform 
import subprocess

from pushbullet import Listener
from pushbullet import Pushbullet

# import logging
# logging.basicConfig(level=logging.DEBUG)

Http_Proxy_Host = None
Http_Proxy_Port = None


class PushHandler(object):
    commands = ['send dog','send cat','still working?']
    # func_list set after class method defs
    cur_dir = os.getcwd()

    def __init__(self, pb, users):
        self.lastpush = time.time()
        self.pb = pb
        self.users = users
        print('start up')
        self.users_contact_info = []
        self.users_contact_info_names = []
        peeps = self.pb.contacts
        for peep in peeps:
            if peep.name in self.users:
                self.users_contact_info.append(peep)
                self.users_contact_info_names.append(peep.name)

    def receive(self, data):
        print('received data: \n{}'.format(data))
        print(data['type'])
        pushes = self.pb.get_pushes(self.lastpush)
        self.lastpush = time.time()
        if pushes:
            if isinstance(pushes[0],dict):
                push = pushes[0]
            else:
                print('not a dict')
                return
        else:
            print(pushes)
            print('no data available...')
            return
        if push['dismissed'] == False:
            print('\n' + data['type'] + ', pushtype: active')
            print(push['body'])
            self.check_message(push)
        else:
            print('\n' + data['type'] + ', pushtype: dismissed')
            return

    def check_message(self,push):
        message = push['body'].strip().lower()
        sender = push['sender_name']
        if message in self.commands:
            if sender in self.users:
                self.pb.delete_push(push.get("iden"))
                print('received command: ' + message)
                self.func_list[self.commands.index(message)](self,sender)
            else:
                print(sender + ' is not a verified user')
                return
        else: # message is not a command
            return

    def send_cam1(self,user):
        if user == 'James Kominick':
            push = self.pb.push_note("", "Got it!")
            subprocess.call(['{}/cam.py 1'.format(settings.BASE_DIR)], shell=True)
            with open('{}/picdump/picout.png'.format(settings.BASE_DIR),'rb') as pic:
                pic_data = self.pb.upload_file(pic, "Here's your pic!")
            
            push = self.pb.push_file(**pic_data)
        else:
            push = self.pb.push_note("", "Sorry, Only James can receive pictures.",
                                    contact = self.users_contact_info\
                                              [self.users_contact_info_names.index(user)])
                
    def send_cam2(self,user):
        if user == 'James Kominick':
            push = self.pb.push_note("", "Got it!")
            subprocess.call(['{}/cam.py 2'.format(settings.BASE_DIR)], shell = True)
            with open('{}/picdump/picout.png'.format(settings.BASE_DIR),'rb') as pic:
                pic_data = self.pb.upload_file(pic, "Here's your pic!")
    
            push = self.pb.push_file(**pic_data)
        else:
            push = self.pb.push_note("", "Sorry, Only James can receive pictures.", 
                                    contact = self.users_contact_info\
                                              [self.users_contact_info_names.index(user)])
            
    def send_confirm(self,user):
        if user == 'James Kominick':
            push = self.pb.push_note("", "Yes, I'm still working!")
        else:
            push = self.pb.push_note("", "Hey {}! Yes, I'm still working!".format(user),
                                    contact = self.users_contact_info\
                                              [self.users_contact_info_names.index(user)])

    func_list = [send_cam1, send_cam2, send_confirm]


def main():
    apikey = settings.key
    users = settings.users

    if apikey == '':
        print('No pushbullet apikey found in pushy.conf file, or bad formatting')
        input('Press enter to exit\n>>')
        return

    if len(users) < 1:
        print('No users found in settings.py. Please specifiy at least one (main) user.')
        input('Press enter to exit \n>>')
        return

 
    pb = Pushbullet(apikey)
    startup = pb.push_note("Pushy Listener Initiated", "auto start on reboot")
    handler = PushHandler(pb, users)

    s = Listener(account=pb,
        on_push = handler.receive,
        http_proxy_host = Http_Proxy_Host,
        http_proxy_port = Http_Proxy_Port)
    try:
        s.run_forever()
    except KeyboardInterrupt:
        close = pb.push_note("Pushy Listener Closed", "stopped")
        s.close()


def start():
    main()


if __name__ == '__main__':
    main()
		
