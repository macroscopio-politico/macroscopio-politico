#!/usr/bin/env python
# The imports bellow are necessary to initialise the dash apps
import candidates
import polls

from server import server


server.config.from_object('settings.DevelopmentConfig')


if __name__ == '__main__':
    server.run(host='0.0.0.0')
