cs-4284
=======

An IRC bot for command-and-controling/monitering many machines for Rackspace.

To start up PyHole, run "pyhole/tools/run_pyhole.py". Any dependencies are
listed in pyhold/README. This will start up an IRC bot that automatically
connects based on a configuration file in "~/.pyhole/pyhole.conf" (default
configuration is found in "configs/custom.conf").

PyHole is controlled by creating "plugins" that react to certain messages
the bot receives, specifically any command that is registered in a plugin and
that begins with a period ('.'). These plugins are listed in the configuration
file and are located in "pyhole\pyhole\plugins". Examples of plugins include:

 .stats  : Responds with the hostname and IP address of where the bot presides
 .sum    : Is a test plugin for a client-side summarizer (found in
              "summarizer\client-side\weechat\summarizer.py"). This summarizer
              is a proof-of-concept work that works by aggregating all of the
              responses from bots. This plugin responds with no actual data,
              but instead simulates data for possible aggregation.
 .bot    : Similar to .sum, this is a test plugin for the server-side summarizer
              (mentioned below)
 .calc   : Is a simple calculator that is a good example plugin
 .update : Runs a script that updates our bot and then terminates itself
 .load   : Creates artificial load for testing purposes. Takes three parameters:
             -message size : Size in bytes of response message
             -send count   : Total amount of times to send the message
             -delay between sends in seconds (accepts floating points)
 .ungroup: Have bots automatically remove themselves from all channels except
              for #all (the default channel)
 .regroup: Have bots automatically add themselves to to a specified channel
              given a certain parameter. Currently only supports the parameter
              of whether the local hostname contains a provided string.
              Ex: ".regroup #vt02 host=vt02" will have every bot on a computer
              whose hostname contains "vt02" add itself to the channel #vt02
.rank:   : Returns the bots rank as well as a random number between 0 and 100
              

In addition, we feature a server-side summarizer that is implemented via PyHole
as well. When it runs (it is special bot that is created under certain
configuration settings), a user is able to send messages to it and have it
automatically forward these messages to bots and subsequently summarize the
results it receives. The summarizer has several aggregation techniques that make
summarizing specific types of data much easier. To begin with you can parse out
certain pieces of the data directly from your command, the syntax is below:

    .command [bot4, bot5] | <type:grouper[:grouper2,]> [<type:grouper[:grouper2,]>,]

Couple of things here, the "[bot4, bot5]" targets specific bots (in this case,
bot4 and bot5). Bots are auto expanded here when using wildcards, e.g. [bot*]
will match all the bots.

After the pipe is a pattern matcher to parse out individual attributes from 
the responses. It begins with a type, followed by a single or list of aggregation
methods. If more than one aggregation method is used then they are piped together,
where the output of the first aggregator is piped to the input of hte second
aggregator. The different possible values for each are below:

  type:
    | n     Match a numeric value, regex is [0-9.-]+
    | s     Any whitespace delimited string, regex is \S+
    | *     Any sequence of characters, greedy. Regex is .+
    | ?     Any sequence of characters, non-greedy. Regex is .+?

  grouper:
    | avg, average      Find the average of the list of numbers
    | concat            Gather all the values in a single list
    | count             Return a count of the number of matches
    | dist              Return several facts about the distribution of the #s
    | max               Return the max variable from all the results
    | min               Return the min variable from all the results
    | sort              Sort all the returned data, either in alphabetical order
                          or numerically if possible
    | sum               Returns the sum of all the values
    | unique            Removes duplicates from the results

A couple of examples for the above methods are below:

=================================================================================

>> .stats [bot*]
Hostname: vt04, IPv4: 198.101.247.220
Hostname: vt03, IPv4: 50.56.178.240
Hostname: vt02, IPv4: 198.101.245.182
Hostname: vt04, IPv4: 198.101.247.220
Hostname: vt03, IPv4: 50.56.178.240
Hostname: vt02, IPv4: 198.101.245.182
Hostname: vt05, IPv4: 198.61.172.118
Hostname: vt08, IPv4: 198.61.172.30
Hostname: vt08, IPv4: 198.61.172.30
Hostname: vt05, IPv4: 198.61.172.118
Hostname: vt06, IPv4: 198.61.172.161
Hostname: vt06, IPv4: 198.61.172.161

>> .stats [bot*] | <s> <s:unique:sort>, <s> <s:unique:concat>
   #        ^1  ^2               ^3  ^4
   #
   # 1. Matches "Hostname:" without a grouping function
   # 2. Matches the actual hostname, e.g. "vt0x" then creates a unique sorted list
   #    of them
   # 3. Matches "IPv4:"
   # 4. Matches the IP address, then creates a unique list and joins them
   
var 1 (s): vt02 | vt03 | vt04 | vt05 | vt06 | vt08
var 3 (s): 198.101.247.220 | 50.56.178.240 | 198.101.245.182 | 198.61.172.118 | 198.61.172.161 | 198.61.172.30

>> .rank                 # default output for all the servers
Rank: -1, Random: 25
Rank: -1, Random: 31
Rank: -1, Random: 52
Rank: -1, Random: 87
.. etc..

>> .rank | Rank: <n:avg>, Random: <n:sort:dist>

var 0 (n): -1.0 # computes the average for the first variable
var 1 (n): .... # shows several statistics, including the 90th, 75th, 50th, 25th
                # 10th percentiles as well as mean, standard variation and
                # generates a histogram of all the values

