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
PYKAZOO_API_URL = 'http://192.168.1.239:8000/v2'

PYKAZOO_API_KEY = '089879bd0dd6504081cf6b9601a2bc4e' + \
                  '0cc4d9c5668d5f771c4d8a62f1e65ae8'
""" The API Key to use for 2600hz Authentication. """

DEBUG = True
""" Enable Server Debug Mode """

SSL_CLIENT_SUBJECT_VALIDATION = False
""" Whether or not the server will validate the MAC address of the requested
    device against the the X-SSL-Subject. Highly recommended for security . """

# Settings for Template Generation
SIP_OUTBOUND_PROXY = 'preproduction.cita-communications.net'

SIP_DNS_MODE = DNSMode.srv
""" DNS Mode for SIP """

FIRMWARE_SERVER_URL = 'http://192.168.1.190:5000'
""" URL of base directory firmware is served from (note: each template has
    its own subdirectory for firmware) """