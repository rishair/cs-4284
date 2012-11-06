import weechat
import random

weechat.register("summarizer", "CS4284", "1.0", "GPL3", "Summarizer for Rackspace IRC botnet", "", "")
weechat.prnt("", "yo dawg!");

# A table to keep track of responses
responseTracker = {}

# TODO: Allow for flushing of a specific command only
def flush(data, buffer, args):
	global responseTracker
	if len(responseTracker) == 0:
		#print info so they know the command didn't just not run
		weechat.prnt(buffer, "No data to flush!")
	else:
		for h in responseTracker:
			summarize(responseTracker[h], buffer)
		
		# clear the old data
		responseTracker = {}
	
	return weechat.WEECHAT_RC_OK;

# debug method, prints the responseTracker
def inspect(data, buffer, args):
	global responseTracker
	weechat.prnt(buffer, str(responseTracker))
	return weechat.WEECHAT_RC_OK;

weechat.hook_command("flush", "Flushes the summary buffer", "", "", "", "flush"," ");
weechat.hook_command("inspect", "Inspects the summary buffer", "", "", "", "inspect"," ");

# I don't use the modify hook, but instead the signal hook
#def summarizeModify(data, modifier, modifier_data, string):
#	weechat.prnt("","Private message:\n\tData: %s\n\tModifier: %s\n\tModifier data: %s\n\tString: %s" % (data, modifier, modifier_data, string));
#	return string;
#weechat.hook_modify("*,irc_in_privmsg", "summarizeModify", "");


def summarizeSignal(data, signal, signal_data):
	global responseTracker
	split = signal_data.split(" ",3)
	if len(split) != 4:
		# The message is weirdly formatted, something weird is going on;
		#    just ignore it.
		return weechat.WEECHAT_RC_OK;
	
	# sender == 0th index
	# PRIVMSG == 1st index
	# receiver == 2nd index
	# message == 3rd index (starts with ':')
	
	# message is in the format of:
	# %s;%s;%s
	# 0th is initial command
	# 1st is hash of full command + sending user
	# 2nd is actual response data
	sender = split[0]
	msg = split[3][1:].split(";", 2)
	
	if len(msg) != 3:
		# The message is weirdly formatted or it wasn't a valid bot response
		#    So just ignore it!
		return weechat.WEECHAT_RC_OK;
	
	if msg[1] in responseTracker:
		respList = responseTracker[msg[1]]
	else:
		respList = [msg[0]]
		responseTracker[msg[1]] = respList
	
	respList.append( (sender, msg[2]) )
	
	# TODO: Make this number configurable
	if len(respList)>20:
		#TODO: Somehow figure out which buffer the user is currently on
		#    and post this info there. For now, just use main buffer
		summarize(respList, "")
		del responseTracker[msg[1]]
	
	return weechat.WEECHAT_RC_OK;

weechat.hook_signal("*,irc_in_privmsg", "summarizeSignal", "");

# Specialized methods to summarize specific commands:

def sum_test(respList, buffer):
	# For this command, a single digit 0-4 is returned as the message.
	# We want to summarize which hosts gave back which digit:
	digits = { '0': [], '1': [], '2': [], '3': [], '4': [] }
	for resp in respList:
		digits[resp[1]].append(resp[0])
	
	for i in digits:
		l = digits[i]
		if len(l) > 0:
			weechat.prnt(buffer, str(len(l)) + " bots replied with " + i + ": ");
			weechat.prnt(buffer, "\t" + ", ".join(digits[i]))

# Mapping of command to the summarizer function.
#   A summarizer function takes exactly two parameters:
#		-A list of tuples where each has two elements:
#			- A user/host name of who sent the message
#			- The response message
#		-A buffer to where information should be posted
summaryFunctions = {
	'sum': sum_test
};

def summarize(respList, buffer):
	cmd = respList[0]
	weechat.prnt(buffer, "\nSummary for command \"" + cmd + "\":")
	if cmd in summaryFunctions:
		summaryFunctions[cmd](respList[1:], buffer)
	else:
		weechat.prnt(buffer, "Warning: No summary function for \"" + cmd + "\"!")
	





