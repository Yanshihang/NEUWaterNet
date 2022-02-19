# Created by 闫世航 on 2021/10/11

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from project.model import db
from project import create_app

app = create_app()
manager = Manager(app=app)

migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
