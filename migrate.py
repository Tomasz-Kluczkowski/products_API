from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from database.models import db
from run import create_app


app = create_app('config')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

"""
Usage:
python migrate.py db init - initialize migrations (folder etc)
python migrate.py db migrate - create tables
python migrate.py db upgrade - apply changes

use migrate and upgrade after any model changes
"""

