from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np
from parse_agegender import *
from parse_session import *
# Parse train_users_2.csv

def parse_matrix(file_name, test):
	# make several lists for classifying
	agegender_dict = parse_country('age_gender_bkts.csv')
	print "agegender parse done..."
	session_dict = parse_session('sessions.csv')
	print "session parse done..."
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
	agegender_1_list = []
	agegender_2_list = []
	agegender_3_list = []
	most_device_list = []

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

			# agegender parsing and append
			temp_age = user_list[5]
			temp_gender = user_list[4]
			agegender_3 = get_top_3(temp_gender, temp_age, agegender_dict)
			temp_list.extend(agegender_3)
			agegender_1_list.append(agegender_3[0])
			agegender_2_list.append(agegender_3[1])
			agegender_3_list.append(agegender_3[2])

			# session parsing and append
			try:
				session_value = session_dict[user_list[0]]
			except:
				session_value = [0, 0, 0, 0, 0, 0, 0, '']
			most_device_list.append(session_value[-1])
			temp_list.append(session_value[-1])
			temp_list.extend(session_value[:-1])

			train_user_dict[user_list[0]] = temp_list

			# append attributes to list 
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
	agegender_1_list = list(set(agegender_1_list))
	agegender_2_list = list(set(agegender_2_list))
	agegender_3_list = list(set(agegender_3_list))
	most_device_list = list(set(most_device_list))

	big_list = [gender_list, age_list, signup_method_list, signup_flow_list, language_list, channel_list, provider_list, 
				tracked_list, app_list, device_type_list, browser_list, agegender_1_list, agegender_2_list, agegender_3_list, most_device_list]


	# print train_user_dict["lsw9q7uk0j"]
	# Classifying our data into index-based form
	for key in train_user_dict:
		value = train_user_dict[key]
		for i in range(len(big_list)):
			if value[i + 1] in big_list[i]:
				value[i + 1] = big_list[i].index(value[i + 1])

	# print train_user_dict["lsw9q7uk0j"]
	# print len(train_user_dict.keys())
	m = len(train_user_dict.values())
	n = len(train_user_dict.values()[0])

	train = np.zeros((m, n))
	counter = 0
	for value in train_user_dict.values():
		train[counter] = value
		counter += 1

	return train, country_list, id_list


file_name = './train_users_2.csv'
train, country_list, id_list = parse_matrix(file_name, False)
print 'training parse done'
test_name = './test_users.csv'
test, test_country_list, training_id_list = parse_matrix(test_name, True)
print 'testing parse done'

print 'starting random forest learning...'
rf = RandomForestClassifier(n_estimators=100)
# rf = GradientBoostingClassifier(loss='deviance', learning_rate=0.1,
#                              n_estimators=30, subsample=0.3,
#                              min_samples_split=2,
#                              min_samples_leaf=1,
#                              max_depth=3,
#                              verbose=2)
rf.fit(train, country_list)
print 'Forest learning done'

# np.savetxt('predict.csv', rf.predict(test), delimiter = ',', fmt = '%f')
ret = rf.predict_proba(test)
print 'Forest predicting done'

# for item in ret:
# 	print item
print rf.classes_
classes = rf.classes_

out_file = open('output.txt', 'w')
out_file.write('id,country\n')
for i in range(len(ret)):
	count = 0
	non_zero = np.count_nonzero(ret[i])
	# print ret[i]
	# print non_zero
	rank = np.argsort(ret[i])[::-1][:5]
	for number in range(5):
		out_file.write(str(training_id_list[i]) + ',' + str(classes[rank[number]]) + '\n')
	# break
out_file.close()