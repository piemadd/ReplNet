import curses, json, textwrap

f = open('test_messages.json', 'r')
test_messages = json.load(f)

def generate_screen(): # generates a screen where there is a 2 line area (with a border) at the bottom to write a message before sending it
	screen = curses.initscr()
	num_rows, num_cols = screen.getmaxyx()
	pad_messages = curses.newpad(int(500/num_rows) * 100, num_cols)
	pad_draft = curses.newpad(int(500/num_cols) + 2, num_cols - 2)
	return screen, pad_messages, pad_draft

def display_messages(json_array, pad_messages):
	#converting the list of message objects into one long string
	initial_message_string = ""
	for message in json_array:
		initial_message_string = f"{initial_message_string}{message['message_content']}\n"
	final_message_string = textwrap.fill(initial_message_string, width=pad_messages.getmaxyx()[1])
	print(final_message_string)

	
	#pad_messages.refresh()

screen, pad_messages, pad_draft = generate_screen()

display_messages(test_messages, pad_messages)