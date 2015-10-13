""" Kazoo Commission Runtime Configuration Options

.. note::
   Remember that this file is Python code. You can use your creativity to
   set the configuration in other ways that meet your needs, such as
   environmental variables.
"""

from enum import Enum


class DNSMode(Enum):
    a_record = 0
    srv = 1
    naptr_srv = 2
    ip = 3

# Settings for Kazoo Commission Server
PYKAZOO_API_URL = 'localhost'

PYKAZOO_API_KEY = 'mykey'
""" The API Key to use for 2600hz Authentication. """

DEBUG = False
""" Enable Server Debug Mode """

SSL_CLIENT_SUBJECT_VALIDATION = True
""" Whether or not the server will validate the MAC address of the requested
    device against the the X-SSL-Subject. Highly recommended for security . """

# Settings for Template Generation
SIP_OUTBOUND_PROXY = 'preproduction.cita-communications.net'

SIP_DNS_MODE = DNSMode.srv
""" DNS Mode for SIP """

FIRMWARE_SERVER_URL = 'http://localhost'
""" URL of base directory firmware is served from (note: each template has
    its own subdirectory for firmware) """
