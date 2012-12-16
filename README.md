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
              

In addition, we feature a server-side summarizer that is implemented via PyHole
as well. When it runs (it is special bot that is created under certain
configuration settings), a user is able to send messages to it and have it
automatically forward these messages to bots and subsequently summarize the
results it receives. Only specialized commands can be run like this, and
currently the only command is ".bot" (mentioned above).