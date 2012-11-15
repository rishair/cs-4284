#   Copyright 2010-2011 Josh Kearney
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Updater plugin"""

from pyhole import plugin
from pyhole import utils
import os
import subprocess
import sys

class Update(plugin.Plugin):
    """Provide access to search engines"""

    @plugin.hook_add_command("update")
    @utils.spawn
    def update(self, params=None, **kwargs):
        """Update bot."""
        
        # This is innefficient for large lists but the overhead is small for smaller lists.
        #    if it is forseen that bots will be in 20+ channels we'll have to change this.
        
        # In addition, if there's a way to do this within irclib feel free to change it.
        #    I don't feel like looking through 50kb to find something that looks remotely
        #    like it will do this
        copy = list(self.irc.channels)
        for ch in copy:
            self.irc.part_channel(ch)
        
        wd = os.getcwd()
        cmd = wd + "/tools/update.sh"
        subprocess.call([cmd])
        sys.exit()
