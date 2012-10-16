# Make sure you run the following commands before executing this script:
#
# $ gem install json
# $ gem install http_request.rb
# 

require 'rubygems'
require 'json'
require 'http_request.rb'


# Modify this to the server that we'll be placing the bot in
# Authentication done by public/private keys
role :rlogin, "rishair@rlogin.cs.vt.edu"

$NAME = "hypno"
$LATEST_HASH = nil
# Uncomment this line to hide all the output (besides errors)
# logger.level = Logger::IMPORTANT 

# Hack to eliminate the SSL certificate verification notification
class Net::HTTP
	alias_method :old_initialize, :initialize
	def initialize(*args)
		old_initialize(*args)
		@ssl_context = OpenSSL::SSL::SSLContext.new
		@ssl_context.verify_mode = OpenSSL::SSL::VERIFY_NONE
	end
end

# Access the github api
def github(path)
	response = HttpRequest.get("https://api.github.com/#{path}").body
	JSON.parse(response)
end

# Download a github repo from a specific user/repo to a local file
def github_download(user, repo, commit, to)
	tarball = HttpRequest.get("https://github.com/#{user}/#{repo}/zipball/#{commit}").body
	File.open(to, 'w') do |f|
		f.write(tarball)
	end
end

# Get the latest commit hash
def latest_hash
	return $LATEST_HASH if $LATEST_HASH != nil
	$LATEST_HASH = github("repos/rishair/cs-4284/branches/master")["commit"]["sha"].slice(0,7)
end

desc 'Download the latest build to your system then upload it to the server'
task :upload_latest do
	hash = latest_hash
	# Download the latest github version of the github repo from master
	github_download("rishair", "cs-4284", hash, "#{hash}.zip")
	# Clean up the directories
	run "rm -rf #{$NAME}/versions/#{hash}"
	# Create the directories
	run "mkdir -p #{$NAME}/packaged-builds/; mkdir -p #{$NAME}/versions/#{hash}"
	# Upload the build to the server
	upload("#{hash}.zip", "#{$NAME}/packaged-builds/#{hash}.zip")
	# Unzip the build to $NAME/versions/<hash>
	run "unzip -d #{$NAME}/versions/#{hash}/ #{$NAME}/packaged-builds/#{hash}.zip"
	# Move the repo to the top level of versions/<hash>
	run "mv #{$NAME}/versions/#{hash}/*/* #{$NAME}/versions/#{hash}"
	# Clean up the left over directory
	run "rm -rf #{$NAME}/versions/#{hash}/rishair-cs-4284-*"
	# Clean up local system
	system "rm #{hash}.zip"

	# Add command to start the application here
end