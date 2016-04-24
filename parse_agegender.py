import numpy as np

def parse_country(file_name):
	age_gender_dict = {}
	with open(file_name, "r") as file:
		first_line = file.readline()
		for line in file:
			ret_list = line.strip().split(',')
			
			print ret_list
			return

parse_country('age_gender_bkts.csv')

