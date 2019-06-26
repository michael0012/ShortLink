# Helper function for website


def to_base62(url_id):
	all_62_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	final_string = ""
	while url_id:
		final_string = all_62_char[url_id%62] + final_string
		url_id = url_id // 62
	while len(final_string) < 6:
		final_string = all_62_char[0] + final_string
	return final_string



def to_base10(url_short):
	all_62_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	current_62_place = 1
	final_10_base_val = 0
	while len(url_short):
		final_10_base_val += current_62_place*all_62_char.find(url_short[len(url_short)-1])
		current_62_place*=62
		url_short = url_short[0:len(url_short)-1]
	return final_10_base_val
