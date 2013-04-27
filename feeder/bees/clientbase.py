# Copyright (C) 2013 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from feeder.models.session import BeeSession


class ClientBase(object):

    def __init__(self, sessions):
        self.sessions = sessions

    def do_session(self, login, password, server_host, server_port, my_ip):
        raise Exception('Do not call base class!')

    def create_session(self, login, password, server_host, server_port):
        protocol = self.__class__.__name__
        session = BeeSession(protocol, login, password, server_host, server_port)
        self.sessions[session.id] = session
        return session