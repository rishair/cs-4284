require 'socket'

# IRC Connection Class
class IRCConn
    def initialize(server, name, port = 6667)
        # Store the information as instance data.
        @name = name

        # Make a connection
        @sock = TCPSocket.open(server, port)

        # Initialize ourselves on the IRC server
        nick(name)
        user(name, "Rabbit McQueue")
    end

    def say(channel, message)
        sock_send "PRIVMSG #{channel} :#{message}"
    end

    def join(channel, key = nil)
        if key.nil?
            sock_send "JOIN #{channel}"
        else
            sock_send "JOIN #{channel} #{key}"
        end
    end

    def start_recv_thread(&cback)
        Thread.new do
            loop do
                # Block this thread waiting for a message to come.
                msgs = @sock.recvmsg.first
                msgs.split("\r\n").each do |msg|
                    # Grab the prefix if there is one.
                    if msg[0] == ':' then
                        origin = msg.split.first[1..-1]
                        msg = msg[msg.index(' ')..-1]
                    end

                    # Parse the rest based on the command.
                    case msg.split.first.upcase
                    when "PING"
                        pong(msg.split[1])
                    when "PRIVMSG"
                        split = msg.split
                        channel = split[1]
                        message = split[2..-1].join(' ')
                        
                        # Get the leading : if there is one.
                        if message[0] == ':' then
                            message = message[1..-1]
                        end

                        cback.call(channel, origin, message)
                    else
                        # Do something with it?
                    end
                end
            end
        end
    end

    private

    # Send data on the socket, appending the CRLF.
    def sock_send(msg)
        @sock.send "#{msg}\r\n", 0
    end

    def user(username, realname)
        sock_send "USER #{username} #{Socket.gethostname} SERVER :#{realname}"
    end

    def pong(daemon)
        sock_send "PONG #{daemon}"
    end

    def nick(name)
        sock_send "NICK #{name}" 
    end
end
