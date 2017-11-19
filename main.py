#!/usr/bin/env python
from server import server
from polls.app import dash_app as polls_app
from candidates.app import dash_app as candidates_app

if __name__ == '__main__':
    server.run(port=80, host='0.0.0.0')
