import numpy as np

def parse_matrix(file_name, test):

	# start user parsing

	# make several lists for classifying
	id_list = []
	age_list = []
	gender_list = []
	signup_method_list = []
	signup_flow_list = []
	language_list = []
	channel_list = []
	provider_list = []
	tracked_list = []
	app_list = []
	device_type_list = []
	browser_list = []

	# begin parsing user file
	train_user_dict = {}
	country_list = []
	with open(file_name, "r") as file:
		first_line = file.readline()
		for line in file:

			user_list = line.strip().split(",")
			# if user_list[-1] == 'NDF':
			# 	continue
			if not test:
				country_list.append(user_list[-1])
			temp_list = []
			temp_list.append(user_list[2])
			if not test:
				temp_list.extend(user_list[4:-1])
			else:
				temp_list.extend(user_list[4:])
			train_user_dict[user_list[0]] = temp_list

			id_list.append(user_list[0])
			gender_list.append(user_list[4])
			age_list.append(user_list[5])
			signup_method_list.append(user_list[6])
			signup_flow_list.append(user_list[7])
			language_list.append(user_list[8])
			channel_list.append(user_list[9])
			provider_list.append(user_list[10])
			tracked_list.append(user_list[11])
			app_list.append(user_list[12])
			device_type_list.append(user_list[13])
			browser_list.append(user_list[14])

	age_list = list(set(age_list))
	gender_list = list(set(gender_list))
	signup_method_list = list(set(signup_method_list))
	signup_flow_list = list(set(signup_flow_list))
	language_list = list(set(language_list))
	channel_list = list(set(channel_list))
	provider_list = list(set(provider_list))
	tracked_list = list(set(tracked_list))
	app_list = list(set(app_list))
	device_type_list = list(set(device_type_list))
	browser_list = list(set(browser_list))

	big_list = [gender_list, age_list, signup_method_list, signup_flow_list, language_list, channel_list, provider_list, 
				tracked_list, app_list, device_type_list, browser_list]


	# Classifying our data into index-based form
	for key in train_user_dict:
		value = train_user_dict[key]
		for i in range(len(big_list)):
			if value[i + 1] in big_list[i]:
				value[i + 1] = big_list[i].index(value[i + 1])

	# print train_user_dict["gxn3p5htnn"]
	# print len(train_user_dict.keys())
	m = len(train_user_dict.values())
	n = len(train_user_dict.values()[0])

	train = np.zeros((m, n))
	counter = 0
	for value in train_user_dict.values():
		train[counter] = value
		counter += 1

	# user info parsing done

	# start session parsing


	return train, country_list, id_list


file_name = './train_users_2.csv'
train, country_list, id_list = parse_matrix(file_name, False)
print 'training parse done'
test_name = './test_users.csv'
test, test_country_list, training_id_list = parse_matrix(test_name, True)
print 'testing parse done'