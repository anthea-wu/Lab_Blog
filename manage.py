from app_blog import app, db
from flask_script import Manager, Command, Shell
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.debug = True
    manager.run()
    app.run()