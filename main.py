#!/usr/bin/env python
# The imports bellow are necessary to initialise the dash apps
import candidates
import polls

from server import server

if __name__ == '__main__':
    server.run(debug=True)
