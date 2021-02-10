import time
from flask_session import Session

from abovl import models
from abovl.app import create_app

def wait_for_database(app):
    wait = 2

    while True:
        try:
            with app.session_scope() as session:
                session.execute('SELECT 1')
            break
        except Exception as e:
            app.logger.info(e)
            app.logger.info('... waiting {} seconds ...'.format(wait))
            time.sleep(wait)
            wait = wait * 2


def tables_ready(app):
    try:
        with app.session_scope() as session:
            session.query(OAuthClient).filter_by(token=token).first()
        return True
    except Exception as e:
        return False


def prepare_tables(app):
    models.Base.metadata.bind = app.db.session.get_bind()
    models.Base.metadata.create_all()

    # if we are not using 'filesystem' sessions, then lets create
    # those tables as well
    session = Session(app)

    if hasattr(session.app.session_interface, 'db'):
        session.app.session_interface.db.create_all()

def bootstrap(app):
    wait_for_database(app)
    prepare_tables(app)


if __name__ == '__main__':
    bootstrap(create_app())
