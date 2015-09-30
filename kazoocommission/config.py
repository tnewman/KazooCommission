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
PYKAZOO_API_URL = 'http://localhost:8000/v2'
""" The URL of the 2600hz Kazoo Crossbar API """

PYKAZOO_API_KEY = 'yourapikeyhere'
""" The API Key to use for 2600hz Authentication """

DEBUG = False
""" Enable Server Debug Mode """

# Settings for Template Generation
SIP_OUTBOUND_PROXY = 'localhost'

SIP_DNS_MODE = DNSMode.a_record
""" DNS Mode for SIP """

AUTOPROVISION_SERVER_URL = 'http://localhost'
""" URL to Provisioning Server (where Kazoo Commission is running). Don't
    forget the port number and path! """

FIRMWARE_SERVER_URL = 'http://localhost'
""" URL of base directory firmware is served from (note: each template has
    its own subdirectory for firmware) """
