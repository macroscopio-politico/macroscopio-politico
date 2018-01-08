#!/usr/bin/env python
# The imports bellow are necessary to initialise the dash apps
import os

import candidates
import polls

from server import server as application


application.config.from_object(os.environ['FLASK_SETTINGS'])


if __name__ == '__main__':
    application.run(host='0.0.0.0')
