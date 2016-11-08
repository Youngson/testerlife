#!/usr/bin/env python3
from testerlife import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
