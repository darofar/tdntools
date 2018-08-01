import os

DATABASE_URI = "{path}{db}".format(path=os.path.realpath(__file__), db="/data/tdnactivities.db")
