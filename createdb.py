import os
from abovl import models
from abovl.app import create_app

if __name__ == '__main__':
    app = create_app()
    models.Base.metadata.bind = app.db.session.get_bind()
    models.Base.metadata.create_all()
