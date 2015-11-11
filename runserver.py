#!/bin/python
from kazoocommission.controllers import app as application
from kazoocommission.controllers import config

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=config.DEBUG)
