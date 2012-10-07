#!/usr/bin/env ruby
# IRC Frontend to the Master Server
# Note that this assumes that the master server is already running and listening
# on a UNIX domain socket located at /tmp/master (subject to change).

require 'socket'
require './lib/ircconn'


class IRCFront
    def initialize(name, server, channel, unix_loc)
        # Open the IRC server and the UNIX domain socket.
        @irc = IRCConn.new(server, name)
        @uds = UNIXSocket.new(unix_loc)

        # Join the appropriate channel
        @irc.join(channel)

        # Proxy from the IRC server to the UNIX socket
        @irc.start_recv_thread { |channel, origin, message|
            @uds.sendmsg message
        }

        # Proxy from the UNIX socket to the IRC server
        loop do
            mesg = @uds.recvmsg.first
            @irc.say channel, mesg
        end
    end
end

IRCFront.new('rbtmq', 'irc.oftc.net', '#cs4944', '/tmp/master')
