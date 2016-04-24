import numpy as np

def parse_session(file_name):
	session_dict = {}

	with open(file_name, "r") as file:
		first_line = file.readline()
		for line in file:
			session_list = line.strip().split(',')
			user_id = session_list[0]

			secs_elapsed = 0
			if session_list[5] != "":
				secs_elapsed = float(session_list[5])

			if user_id not in session_dict:
				session_dict[user_id] = []
				action_list = []
				action_type_list = []
				device_list = []
				action_detail_list = []

				if session_list[1] != "":
					action_list.append(session_list[1])
				if session_list[2] != "":
					action_type_list.append(session_list[2])
				if session_list[3] != "":
					action_detail_list.append(session_list[3])
				if session_list[4] != "":
					device_list.append(session_list[4])

				session_dict[user_id].append(action_list)
				session_dict[user_id].append(action_type_list)
				session_dict[user_id].append(action_detail_list)
				session_dict[user_id].append(device_list)
				session_dict[user_id].append(secs_elapsed)
				session_dict[user_id].append(1)

				session_dict[user_id].append(secs_elapsed)

				# print session_dict
				# print session_dict[user_id][0]
				# print session_dict[user_id][1]
				# print session_dict[user_id][2]
				# print session_dict[user_id][3]
				# print session_dict[user_id][4]
				# break

			else:
				if session_list[1] not in session_dict[user_id][0] and session_list[1] != "":
					session_dict[user_id][0].append(session_list[1])
				if session_list[2] not in session_dict[user_id][1] and session_list[2] != "":
					session_dict[user_id][1].append(session_list[2])
				if session_list[3] not in session_dict[user_id][2] and session_list[3] != "":
					session_dict[user_id][2].append(session_list[3])
				if session_list[4] not in session_dict[user_id][3] and session_list[4] != "":
					session_dict[user_id][3].append(session_list[4])
				session_dict[user_id][4] += secs_elapsed
				session_dict[user_id][5] += 1
				session_dict[user_id][6] = session_dict[user_id][4] / session_dict[user_id][5]


	return session_dict


my_dict = parse_session('sessions.csv')
print my_dict["d1mm9tcy42"]
