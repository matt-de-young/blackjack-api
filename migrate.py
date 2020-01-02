# TODO: reuse this as a "cli" module with click
from api.app import create_app, db

if __name__ == "__main__":
    create_app()
    db.cli.run()
