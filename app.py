import os
from main import create_app, db

app = create_app()
app.app_context().push()


if __name__ == '__main__':
    db.create_all()
    app.run(port=5000, host='0.0.0.0')

