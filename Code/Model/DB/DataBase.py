import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class DataBase:
    """This class allows communication with FireBase DB"""

    def __init__(self, reference, url):
        self.path = "Configuration/FireBase/db.json"
        cred = credentials.Certificate(self.path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': url
        })
        self.ref = db.reference(reference)

    def update(self, id, data):
        """Update individual parking state.
        Parameters are supposed to be string and dict"""
        self.ref.child(f"{id}").set(data)

    def add(self, id, data):
        """Add individual parking state.
        Parameters are supposed to be string and dict"""
        self.ref.child(f"{id}").set(data)

    def check(self, id):
        """Return True if id exists as a child"""
        return True if self.ref.child(f"{id}").get() is not None else False




