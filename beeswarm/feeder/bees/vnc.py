# Copyright (C) 2013 Aniket Panse <contact@aniketpanse.in>
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

import logging
import socket

from beeswarm.feeder.bees.clientbase import ClientBase
from beeswarm.shared.vnc_constants import *


class vnc(ClientBase):

    def __init__(self, sessions):
        super(vnc, self).__init__(sessions)

    def do_session(self, login, password, server_host, server_port, my_ip):
        session = self.create_session(login, password, server_host, server_port, my_ip)
        self.sessions[session.id] = session

        logging.debug('Sending %s honeybee to %s:%s. (bee id: %s)' % ('vnc', server_host, server_port, session.id))
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((server_host, int(server_port)))
            session.source_port = client_socket.getsockname()[1]

        except socket.error as e:
            logging.debug('Caught exception: %s (%s)' % (e, str(type(e))))
        else:
            session.did_connect = True
            protocol_version = client_socket.recv(1024)
            client_socket.send(RFB_VERSION)
            supported_auth_methods = client_socket.recv(1024)

            # \x02 implies that VNC authentication method is to be used
            # Refer to http://tools.ietf.org/html/rfc6143#section-7.1.2 for more info.
            if '\x02' in supported_auth_methods:
                client_socket.send(VNC_AUTH)
            challenge = client_socket.recv(1024)

            # Ideally, we should encrypt the challenge and send it across, but since the capability is
            # going to reject the connection anyway, we don't do that yet.
            client_socket.send('\x00' * 16)
            auth_status = client_socket.recv(1024)
            if auth_status == AUTH_SUCCESSFUL:
                session.did_login = True
        finally:
            session.alldone = True