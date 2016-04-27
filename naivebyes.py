# from sklearn.ensemble import RandomForestClassifier
# from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.linear_model import LogisticRegression
import numpy as np
from parse_agegender import *
from parse_session import *
# Parse train_users_2.csv
import csv
import random
import math




def separateByClass(dataset):
	separated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[-1] not in separated):
			separated[vector[-1]] = []
		separated[vector[-1]].append(vector)
	return separated


def summarize(dataset):
	summaries = [(np.mean(attribute), np.std(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries

def summarizeByClass(dataset):
	separated = separateByClass(dataset)
	summaries = {}
	for classValue, instances in separated.iteritems():
		summaries[classValue] = summarize(instances)
	return summaries

def calculateProbability(x, mean, stdev):
	if stdev != 0:
		exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
		return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
	else:
		return 0

def calculateClassProbabilities(summaries, inputVector):
	probabilities = {}
	for classValue, classSummaries in summaries.iteritems():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = inputVector[i]
			probabilities[classValue] *= calculateProbability(x, mean, stdev)
	return probabilities
			
def predict(summaries, inputVector):
	probabilities = calculateClassProbabilities(summaries, inputVector)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.iteritems():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel

def getPredictions(summaries, testSet):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i])
		predictions.append(result)
	return predictions



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


# print "train is:"
# print train

# print "country_list is:"
# print country_list

# print "id_list is"
# print id_list

# print 'training parse done'


test_name = './test_users.csv'
test, test_country_list, test_list = parse_matrix(test_name, True)
print 'testing parse done'
country_list = list(set(country_list))
###prasings are done, now start prediction



summaries = summarizeByClass(train)
predictions = getPredictions(summaries, test)

#  Predictions : ['A', 'B']


f = open('output_naive_byes.txt', 'w')
f.write('id,country\n')
for i in range(len(predictions)):
	top = np.argsort(predictions[i])[::-1][:5].tolist()
	for j in top:
		f.write(str(test_list[i]) + ',' + str(country_list[j]) + '\n')
	
