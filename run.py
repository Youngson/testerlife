#!/usr/bin/env python3
from testerlife import create_app
from flask_alembic import alembic_script

app = create_app()
app.cli.add_command(alembic_script,'db')


if __name__ == '__main__':
    app.run()