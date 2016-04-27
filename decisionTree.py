import math
from parse_agegender import *
from parse_session import *
log2=lambda x:math.log(x) / math.log(2)

attributes = list(range(3))
targetIndex = -1

def parse_matrix(file_name, test):
    # make several lists for classifying
    agegender_dict = parse_country('age_gender_bkts.csv')
    print "agegender parse done..."
    #session_dict = parse_session('sessions.csv')
    #print "session parse done..."
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
    # agegender_1_list = []
    # agegender_2_list = []
    # agegender_3_list = []
    # most_device_list = []

    # begin parsing user file
    train_user_dict = {}
    country_list = []
    with open(file_name, "r") as file:
        first_line = file.readline()
        for line in file:

            user_list = line.strip().split(",")
            # if user_list[-1] == 'NDF':
            #   continue
            if not test:
                country_list.append(user_list[-1])
            temp_list = []
            temp_list.append(user_list[2])
            if not test:
                temp_list.extend(user_list[4:-1])
            else:
                temp_list.extend(user_list[4:])

            # agegender parsing and append
            # temp_age = user_list[5]
            # temp_gender = user_list[4]
            # agegender_3 = get_top_3(temp_gender, temp_age, agegender_dict)
            # temp_list.extend(agegender_3)
            # agegender_1_list.append(agegender_3[0])
            # agegender_2_list.append(agegender_3[1])
            # agegender_3_list.append(agegender_3[2])

            # session parsing and append
            # try:
            #     session_value = session_dict[user_list[0]]
            # except:
            #     session_value = [0, 0, 0, 0, 0, 0, 0, '']
            # most_device_list.append(session_value[-1])
            # temp_list.append(session_value[-1])
            # temp_list.extend(session_value[:-1])

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
    # agegender_1_list = list(set(agegender_1_list))
    # agegender_2_list = list(set(agegender_2_list))
    # agegender_3_list = list(set(agegender_3_list))
    # most_device_list = list(set(most_device_list))

    big_list = [gender_list, age_list, signup_method_list, signup_flow_list, language_list, channel_list, provider_list, 
                tracked_list, app_list, device_type_list, browser_list]

#, agegender_1_list, agegender_2_list, agegender_3_list, most_device_list
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
    print "Matrix Parse Done"
    return train, country_list, id_list

## ======================================== End of Parsing Matrix


def calcTargetEntropy(country_list):
    countryDict = {}
    for country in country_list:
        if country in countryDict:
            countryDict[country] += 1
        else:
            countryDict[country] = 1
        
    totalCountryCount = sum(countryDict.values())
    entropy = 0
    for key in countryDict.keys():
        pi = countryDict[key] * 1.0 / totalCountryCount
        entropy -= pi * log2(pi)
    return entropy

## restrict numbers in myList
def calcE(myList):
    mySum = sum(myList)
    entropy = 0
    for item in myList:
        pi = item * 1.0 / mySum
        entropy -= pi * log2(pi)
    return entropy

def calcDoubleEntropy(attrIndex, data, country_list):
    count = 0
    myDict = {}
    for row in data:
        label = row[attrIndex]
        country = country_list[count]
        if label not in myDict:
            myDict[label] = {}
            myDict[label][country] = 1
        else:
            if country not in myDict[label]:
                myDict[label][country] = 1
            else:
                myDict[label][country] += 1

        count += 1

    totalCountryCount = len(country_list)
    entropy = 0
    for key in myDict.keys():
        attrDict = myDict[key]
        attrValue = attrDict.values()
        entropy += sum(attrValue) * 1.0 / totalCountryCount * calcE(attrValue)
    return entropy

def calcInfoGain(data, target_entropy):
    attrDict = {}
    row = data[0]
    for attrIndex in range(len(row)):
        attrDict[attrIndex] = target_entropy - calcDoubleEntropy(attrIndex, data, country_list)
    
    largest = max(attrDict, key = attrDict.get)
    return largest, attrDict

def getMajor(country_list):
    myDict = {}
    for item in country_list:
        if item in myDict:
            myDict[item] += 1
        else:
            myDict[item] = 1

    largest = max(myDict, key = myDict.get)
    return largest

def getData(data, largest):
    
    return np.delete(data, np.s_[largest:largest + 1], axis = 1)

def buildTree(data, attributes, target_entropy, recursion, targetIndex, country_list):

    recursion += 1
    classes = country_list
    if data.all() is None or len(attributes) == 1:
        return getMajor(country_list)

    elif classes.count(classes[0]) == len(classes):
        major = classes[0]
        return classes[0]
    else:
    # choose the best attribute
        largest, attrDict = calcInfoGain(data, target_entropy)

        tree = {largest: {}}
        largest_list = data[:, largest]
        largest_list = list(set(largest_list))

        for value in largest_list:
            newData = getData(data, largest)
            newAttr = attributes[:]
            newAttr.pop(largest)
            subTree = buildTree(newData, newAttr, target_entropy, recursion, targetIndex, country_list)
            tree[largest][value] = subTree
    return tree


def predict(test_data, model):
    while isinstance(tempDict, dict):
        tempDict = tempDict[temp.keys()[0]]
        tempDict



# class TreeNode:

#     def __init__(self, attr = None, data = [], children = []):
#         self.attr = attr
#         self.data = data
#         self.children = children

# def buildTree(data, attributes, target_entropy, targetIndex, country_list):

#     if data.all() is None:
#         return TreeNode()

#     else:
#         largest = calcInfoGain(data, target_entropy)
#         newData = getData(data, largest)
#         attributes = attributes[:]
#         attributes.pop(largest)
#         print attributes
#         root = TreeNode(largest, newData, [])
#         largest_list = data[:, largest]
#         largest_list = list(set(largest_list))
#         for value in largest_list:
#             if (len(attributes) - 1) <= 0:
#                 node = TreeNode()
#             else:
#                 node = buildTree(newData, attributes, target_entropy, targetIndex, country_list)
#             root.children.append(node)

#     return root


file_name = './train_users_2.csv'
train, country_list, id_list = parse_matrix(file_name, False)
train = train[:, 1:4]
print 'training parse done'
test_name = './test_users.csv'
test, test_country_list, training_id_list = parse_matrix(test_name, True)
test = test[:, 1:4]
print 'testing parse done'
target_entropy = calcTargetEntropy(country_list)
largest, attrDict = calcInfoGain(train, target_entropy)
result = buildTree(train, attributes, target_entropy, 0, -1, country_list)
print result
print result.keys()