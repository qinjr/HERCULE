import random

#separator:0 is ',',1 is '/t'
def label(input_file, output_file, separator):
	input_file = open(input_file, 'r')
	output_file = open(output_file, 'w')
	while True:
		log_string = input_file.readline()
		if not log_string:
			break
		decision = random.randint(0, 7)
		if decision == 0:
			new_str = log_string[:-1] + separator + '0\n'
		else:
			new_str = log_string[:-1] + separator + '1\n'
		output_file.writelines([new_str])

label('../data/sjtu_flow/resp/resp_test.log', '../data/sjtu_flow/resp/resp_test_corrected.log', '\t')