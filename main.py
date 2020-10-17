"""
This is just simple for testing your typing speed
"""
import time
import json
import random
import sys
import os
from colorama import init, Fore
import pickle
from datetime import datetime as dt

init()

class Typing:
	def __init__(self):
		self.rows , self.cols = [int(x) for x in os.popen('stty size','r').read().split()] # get size terminal
		self.logged = False
		self.profile = {}
		self.check_db()
		self.data = None
		with open('quotes.json','r') as f:
			self.data = (l.strip() for l in f.readlines())
		self.res = [z[0].split() for z in [json.loads(x.encode('utf-8')) for x in self.data if x]]
		self.display_text = self.load_text(self.res) 
		self.display_menu()

# loading text for display
	def display_menu(self):
		self.clear()
		if self.logged:
			print(Fore.RED + "WELCOME BACK {} ".format(self.profile['name']).center(self.cols))
		else:
			print(Fore.RED + "WELCOME {}".format(self.profile['name']).center(self.cols))
		choices = {
			"1": self.start,
			"2": self.my_info,
			"3": sys.exit
		}
		print(Fore.WHITE + "TYPING RACER".center(self.cols))
		print("1. Start ".center(self.cols))
		print("2. My Info ".center(self.cols))
		print("3. Exit\n".center(self.cols))
		ask = input("Pilih No ? ::>".rjust(self.rows))
		if ask not in choices:
			sys.exit()
		choices[ask]()

# for see your info
	def my_info(self):
		self.clear()
		print("=====YOUR INFO=====".center(self.cols))
		print("HIGHES SCORE\tLATEST_SCORE".center(self.cols))
		print("NO, WPM, right, wrong \t WPM, right, wrong".center(self.cols))
		for x in range(len(self.profile['high_score'])):
			print("\t\t  {},   {},   {},   {} \t\t  {},   {},   {}".format(Fore.WHITE+str(x),
				Fore.CYAN + str(int(self.profile['high_score'][x]['wpm'])),
				Fore.GREEN + str(self.profile['high_score'][x]['right']),
				Fore.RED + str(self.profile['high_score'][x]['wrong']),
				Fore.CYAN + str(int(self.profile['last_score'][x]['wpm'])),
				Fore.GREEN + str(self.profile['last_score'][x]['right']),
				Fore.RED + str(self.profile['last_score'][x]['wrong']),
				).center(self.cols))
		if input("\n" + Fore.WHITE + "Back to Menu or Exit (y/n) ? ::>> ".rjust(self.rows)) in ['Y','y']:
			self.display_menu()
		else:
			sys.exit()

# clear screen
	def clear(self):
		os.system('cls') if sys.platform != "linux" else os.system('clear')

#reload text
	def load_text(self, res):
		display_text = [x for x in random.choice([random.choice(self.res) for _ in range(10)]) if "’" not in x]
		return display_text

# write file
	def write_db(self, profile):
		file = open('profile.pkl','wb')
		pickle.dump(profile, file)
		file.close()

# read file
	def read_db(self):
		profile = open('profile.pkl', 'rb')
		self.profile = pickle.load(profile)
		profile.close()

# check file
	def check_db(self):
		if not os.path.exists('profile.pkl'):
			self.clear()
			name = input("Enter A Name :> ".ljust(self.cols))
			age = input("Enter A Age :> ".ljust(self.cols))
			# name = input()
			self.profile = {
				"name":name,
				"age": age,
				"high_score": [],
				"last_score": []
			}

			self.write_db(self.profile)
		else:
			self.logged = True
			self.read_db()

# Starting 
	def start(self):
		wpm = 0
		right = 0
		wrong = 0
		now = time.time()
		timing = 0
		future = now + 61
		wrong_temp = 0
		temp_right = []

		while time.time() < future:
			self.clear()
			if self.display_text == []: self.display_text = self.load_text(self.res)
			
			print(Fore.GREEN + "WPM = {} ".format(int(wpm)).center(self.cols))
			print(Fore.GREEN + "Right Answer = {} ".format(int(right)).center(self.cols))
			print(Fore.RED + "Wrong Answer = {} ".format(wrong).center(self.cols))
			print("\n\n")
			if wrong_temp != wrong:
				print(Fore.RED + self.display_text[0].center(self.cols))
				wrong_temp += 1
			else:
				print(Fore.WHITE + self.display_text[0].center(self.cols))
			
			print(Fore.WHITE + " ".join(self.display_text[1:]).center(self.cols))
			print("\n")
			answer = input("::>>".rjust(self.rows))
			if  answer == self.display_text[0]:
				right += 1
				wpm += (len(self.display_text[0]) / 5) / 1 
				self.display_text.remove(self.display_text[0])
			else:
				wrong += 1

		res = {
				"wpm": int(wpm),
				"right": right,
				"wrong": wrong,
				"time": str(dt.now()).split('.')[0]
				}
		if self.profile['high_score'] != []:
			for i in range(len(self.profile['high_score'])):
				if res['wpm'] > self.profile['high_score'][i]['wpm']:
					self.profile['high_score'].insert(i, res)

		self.profile['last_score'].append(res)
		self.profile['high_score'].append(res)
		self.profile['last_score'].reverse()
		self.write_db(self.profile)

		print("======= RESULT =======".center(self.cols))
		print("WPM : {}".format(int(wpm)).center(self.cols))
		print("RIGHT : {}".format(right).center(self.cols))
		print("WRONG : {}".format(wrong).center(self.cols))
		
		if str(input("Continue (y/n) :> ".rjust(self.rows))) in ['Y','y']:
			self.start()
		else:
			self.display_menu()

if __name__ == "__main__":
	Typing()