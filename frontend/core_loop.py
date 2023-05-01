"""


"""

from database.models import Recipe, Ingredient, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Kai_quote = 'other people help you make happy hormones in your head'
# 'Games are an integrated system, copied, not distributed'
'RAD'  # ddd

class STD_sqlalchemy_unit(object):
    """ | """

    database = 'sqlite:///G:\CookingWithCoders\database\example.db'
    session = False

    def __init__(self):
        self.init_database_session()

    def init_database_session(self):
        # init DB session
        # boilerplate
        engine = create_engine(self.database)
        print(f"engine.url = {engine.url}")
        print(f"engine.table_names() = {engine.table_names()}")
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def fetch_topics(self):
        # Make a query to find all Roles in the database
        self.session.query(Recipe).all()
        # [<sqlalchemy_declarative.Role object at 0x2ee3a10>]

        # Return the first Role from all Roles in the database
        role = self.session.query(Recipe).first()
        if role:
            print(role.name)

            # Find all Roles whose person field is pointing to the person object
            print(self.session.query(Ingredient).filter(Ingredient.recipe == role).all())

            # Retrieve one Role whose person field is point to the person object
            topic = self.session.query(Ingredient).filter(Ingredient.recipe == role).one()
            print(topic)
            print(topic.description)

        return self.session.query(Ingredient).all()

    def add_new(self):
        print('add a new Topic ->')
        name = input()

        print('Add a description ->')
        description = input()

        # Insert an Topic in the topics table
        new_topic = Ingredient(name=name, description=description)
        self.session.add(new_topic)
        self.session.commit()


if __name__ == '__main__':
    t = STD_sqlalchemy_unit()
    t.fetch_topics()
