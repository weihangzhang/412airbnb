import numpy as np
import random

def parse_country(file_name):
	age_gender_dict = {}
	with open(file_name, "r") as file:
		first_line = file.readline()
		for line in file:
			ret_list = line.strip().split(',')

			key = ret_list[2]+ret_list[0]
			if key not in age_gender_dict.keys():
				age_gender_dict[key] = {}
				if ret_list[1] not in age_gender_dict[key].keys():
					age_gender_dict[key][ret_list[1]] = float(ret_list[3])
				else:
					age_gender_dict[key][ret_list[1]] += float(ret_list[3])
			else:
				if ret_list[1] not in age_gender_dict[key].keys():
					age_gender_dict[key][ret_list[1]] = float(ret_list[3])
				else:
					age_gender_dict[key][ret_list[1]] += float(ret_list[3])
	for key in age_gender_dict.keys():
		value = age_gender_dict[key]
		age_gender_dict[key] = sorted(value.items(), key=lambda x: x[1], reverse=True)

		temp_list = []
		temp_list.append(age_gender_dict[key][0][0])
		temp_list.append(age_gender_dict[key][1][0])
		temp_list.append(age_gender_dict[key][2][0])
		age_gender_dict[key] = temp_list
	file.close()
	return age_gender_dict

def get_top_3(gender, age, dd):
	if age == '':
		return ['', '', '']
	if gender == '-unknown-' or gender == 'OTHER':
		foo = ['male', 'female']
		ranfoo = random.randint(0,1)
		gender = foo[ranfoo]

	age = float(age)
	gender = gender.lower()
	query = ''
	if age <= 4 and age >= 0:
		query = gender + '0-4'
	elif age <= 9 and age >= 5:
		query = gender + '5-9'
	elif age <= 14 and age >= 10:
		query = gender + '10-14'
	elif age <= 19 and age >= 15:
		query = gender + '15-19'
	elif age <= 24 and age >= 20:
		query = gender + '20-24'
	elif age <= 29 and age >= 25:
		query = gender + '25-29'
	elif age <= 34 and age >= 30:
		query = gender + '30-34'
	elif age <= 39 and age >= 35:
		query = gender + '35-39'
	elif age <= 44 and age >= 40:
		query = gender + '40-44'
	elif age <= 49 and age >= 45:
		query = gender + '45-49'
	elif age <= 54 and age >= 50:
		query = gender + '50-54'
	elif age <= 59 and age >= 55:
		query = gender + '55-59'
	elif age <= 64 and age >= 60:
		query = gender + '60-64'
	elif age <= 69 and age >= 65:
		query = gender + '65-69'
	elif age <= 74 and age >= 70:
		query = gender + '70-74'
	elif age <= 79 and age >= 75:
		query = gender + '75-79'
	elif age <= 84 and age >= 80:
		query = gender + '80-84'
	elif age <= 89 and age >= 85:
		query = gender + '85-89'
	elif age <= 94 and age >= 90:
		query = gender + '90-94'
	elif age <= 99 and age >= 95:
		query = gender + '95-99'
	else:
		query = gender + '100+'
	# print query
	return dd[query]

# dd = parse_country('age_gender_bkts.csv')
# print get_top_3('male', 35, dd)