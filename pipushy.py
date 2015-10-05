#!/home/james/projects/pushy2/bin/python

# boot execute in /etc/rc.local
# nohup /home/james/projects/pushy2/app/pipushy.py > /dev/null 2>&1 &

import os, sys, time, platform
import subprocess

from pushbullet import Listener
from pushbullet import Pushbullet
# import pyimgur

# import logging
# logging.basicConfig(level=logging.DEBUG)

Http_Proxy_Host = None
Http_Proxy_Port = None

def get_confs():
	# Search for config file containing users and personal api keys	
	conf_file = 'pushy.conf'
	try:
		with open('/home/james/projects/pushy2/app/'+conf_file,'r') as file1:
			dat = []
			for line in file1:
				dat.append(line)
	except:
	    print('No config pushy.conf file found. \nPlease create a file "pushy.conf" containing:\nusers = User Name, Another User \npushyapikey = your_key \nimgurid = yourkey')
	    input('Press enter to exit\n>>')
	    sys.exit()
	
	apikey = ''
	imkey = ''
	users = []
	for i in dat:
		if i[0] != '#':
			info = i.split('=')
			if 'users' in info[0]:
				names = info[-1].split(',')
				for name in names:
					if len(name.strip().strip("'")) > 0:
						users.append(name.strip().strip("'").title())
			
			if 'pushyapi' in info[0]:
				apikey = info[-1].strip().strip("'")
				
			if 'imgurid' in info[0]:
				imkey = info[-1].strip().strip("'")
	
	return apikey, imkey, users


class PushHandler(object):
	commands = ['send dog','send cat','still working?']
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
		if pushes[1]:
			if isinstance(pushes[1][0],dict):			# THESE TWO LINES [1][0] for pip install
				push = pushes[1][0]
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
			push = self.pb.push_note("","Got it!")
			subprocess.call(['sudo /home/james/projects/pushy2/app/cam.py 1'], shell=True)
			with open('/home/james/projects/pushy2/app' + '/picdump/picout.png','rb') as pic:
				pic_data = self.pb.upload_file(pic, "Here's your pic!")
			
			push = self.pb.push_file(**pic_data)
		else:
		# 	#upload_image = im.upload_image(cur_dir+'/picout.png',title='Requested Picture')
		# 	#push = pb.push_note("",upload_image.link, contact = users_contact_info[users_contact_info_names.index(sender)])
			push = self.pb.push_note("","Sorry, Only James can receive pictures.", contact = self.users_contact_info[self.users_contact_info_names.index(user)])
			
	def send_cam2(self,user):
		if user == 'James Kominick':
			push = self.pb.push_note("","Got it!")
			subprocess.call([' sudo /home/james/projects/pushy2/app/cam.py 2'], shell = True)
			with open('/home/james/projects/pushy2/app'+'/picdump/picout.png','rb') as pic:
				pic_data = self.pb.upload_file(pic, "Here's your pic!")
		
			push = self.pb.push_file(**pic_data)
		else:
			#upload_image = im.upload_image(cur_dir+'/picout.png',title='Requested Picture')
			#push = pb.push_note("",upload_image.link, contact = users_contact_info[users_contact_info_names.index(sender)])
			push = self.pb.push_note("","Sorry, Only James can receive pictures.", contact = self.users_contact_info[self.users_contact_info_names.index(user)])
		
	def send_confirm(self,user):
		if user == 'James Kominick':
			push = self.pb.push_note("","Yes, I'm still working!")
		else:
			#push = users_contact_info[users_contact_info_names.index(sender)].push_note("","Yes, i'm still working!")
			push = self.pb.push_note("","Hey " + user + "! Yes, I'm still working!", contact = self.users_contact_info[self.users_contact_info_names.index(user)])
			
	func_list = [send_cam1, send_cam2, send_confirm]

	

def main():
	apikey, imkey, users = get_confs()
	
	if apikey == '':
	    print('No pushbullet apikey found in pushy.conf file, or bad formatting')
	    input('Press enter to exit\n>>')
	    sys.exit()
	  
	if len(users) < 1:
		print('No users found in pushy.conf file. Please specifiy at least one (main) user.')
		input('Press enter to exit \n>>')
		sys.exit()
	
	if imkey != '':
		print('imgur key found')
		#im = pyimgur.Imgur(imkey) #to send to other users

	    
	pb = Pushbullet(apikey)
	startup = pb.push_note("Pushy Listener Initiated","auto start on reboot")
	handler = PushHandler(pb, users)

	s = Listener(account=pb,
		on_push = handler.receive,
		http_proxy_host = Http_Proxy_Host,
		http_proxy_port = Http_Proxy_Port)
	try:
		s.run_forever()
	except	KeyboardInterrupt:
		close = pb.push_note("Pushy Listener Closed","stopped")
		s.close()

if __name__ == '__main__':
	main()
		
