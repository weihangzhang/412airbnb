# from sklearn.ensemble import RandomForestClassifier
# from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.linear_model import LogisticRegression
import numpy as np
from parse_agegender import *
from parse_session import *
# Parse train_users_2.csv

def parse_matrix(file_name, test):
	# make several lists for classifying
	agegender_dict = parse_country('age_gender_bkts.csv')
	print "agegender parse done..."
	# session_dict = parse_session('sessions.csv')
	# print "session parse done..."
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

	# big_list = [gender_list, age_list, signup_method_list, signup_flow_list, language_list, channel_list, provider_list, 
	# 			tracked_list, app_list, device_type_list, browser_list]

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

	file.close()
	return train, country_list, id_list

# Helper function to evaluate the total loss on the dataset
def calculate_loss(model):
    W1 = model['W1']
    b1 = model['b1']
    W2 = model['W2']
    b2 = model['b2']

    # Forward propagation to calculate our predictions
    z1 = train.dot(W1) + b1
    a1 = np.tanh(z1)
    z2 = a1.dot(W2) + b2
    exp_scores = np.exp(z2)

    probs = exp_scores / np.sum(exp_scores, axis = 1, keepdims = True)
    # Calculating the loss
    corect_logprobs = -np.log(probs[range(num_examples), country_list])
    data_loss = np.sum(corect_logprobs)
    # Add regulatization term to loss (optional)
    data_loss += regular_rate/2 * (np.sum(np.square(W1)) + np.sum(np.square(W2)))
    return 1./num_examples * data_loss

# Helper function to predict an output
def predict(model, x):
    W1 = model['W1']
    b1 = model['b1']
    W2 = model['W2']
    b2 = model['b2']

    # Forward propagation
    z1 = x.dot(W1) + b1
    a1 = np.tanh(z1)
    z2 = a1.dot(W2) + b2
    exp_scores = np.exp(z2)

    print exp_scores
    probs = exp_scores / np.sum(exp_scores, axis = 1, keepdims = True)

    out_file = open('output.txt', 'w')
    out_file.write('id,country\n')
    print probs
    for i in range(len(probs)):
    	rank = np.argsort(probs[i])
    	print rank
    	for number in range(5):
			out_file.write(str(training_id_list[i]) + ',' + str(country_set[rank[11-number]]) + '\n')

	# out_file.close()
    return np.argmax(probs, axis = 1)


def build_model(train, nn_hdim, nn_input_dim, nn_output_dim, num_examples, learning_rate, regular_rate, y, num_passes = 100):
	np.random.seed(0)
	W1 = np.random.randn(nn_input_dim, nn_hdim) / np.sqrt(nn_input_dim)
	b1 = np.zeros((1, nn_hdim))
	W2 = np.random.randn(nn_hdim, nn_output_dim) / np.sqrt(nn_hdim)
	b2 = np.zeros((1, nn_output_dim))

	model = {}
    # gradient descent
	for i in xrange(0, num_passes):
		z1 = train.dot(W1) + b1
		a1 = np.tanh(z1)
		z2 = a1.dot(W2) + b2
		exp_scores = np.exp(z2)

		probs = exp_scores / np.sum(exp_scores, axis = 1, keepdims = True)
		# print probs
		# start back propagation
		delta3 = probs
		delta3[range(num_examples), y] -= 1
		# delta3[range(num_examples)] -= y

		dW2 = (a1.T).dot(delta3)
		db2 = np.sum(delta3, axis = 0, keepdims = True)
		delta2 = delta3.dot(W2.T) * (1 - np.power(a1, 2))
		dW1 = np.dot(train.T, delta2)
		db1 = np.sum(delta2, axis = 0)

		dW2 += regular_rate * W2
		dW1 += regular_rate * W1

		# Gradient descent parameter update
		W1 += -learning_rate * dW1
		b1 += -learning_rate * db1
		W2 += -learning_rate * dW2
		b2 += -learning_rate * db2

		model['W1'] = W1
		model['b1'] = b1
		model['W2'] = W2
		model['b2'] = b2

		print calculate_loss(model)
		learning_rate *= 0.99
		regular_rate *= 0.99
	return model


file_name = './train_users_2.csv'
train, country_list, id_list = parse_matrix(file_name, False)
print 'training parse done'

test_name = './test_users.csv'
test, test_country_list, training_id_list = parse_matrix(test_name, True)
print 'testing parse done'

# neural network start

num_examples = len(train) # training set size
# num_examples = 2
print 'num exp', num_examples
nn_input_dim = len(train[0]) # input layer dimension
nn_output_dim = 12 # output layer dimension
 
# Gradient descent parameters
learning_rate = 0.000001 # learning rate for gradient descent
regular_rate = 0.000001 # regularization strength

print 'start building neural network...'
country_set = list(set(country_list))
for i in range(len(country_list)):
	country_list[i] = country_set.index(country_list[i])
print country_set

# train = train[:,1:]
train = train

yyy = np.zeros((len(country_list), 12))
for i in range(len(country_list)):
	yyy[i][country_list[i]] = 1
	
print test[1, :]
model = build_model(train, 50, nn_input_dim, nn_output_dim, num_examples, learning_rate, regular_rate, country_list)
# model = build_model(train, 23, nn_input_dim, nn_output_dim, num_examples, learning_rate, regular_rate, yyy)
print 'start predicting neural network...'
# predict(model, test[:, 1:])
predict(model, test)
# predict(model, train)