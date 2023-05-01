from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Recipe, Ingredient, Base

engine = create_engine(r'sqlite:///G:\CookingWithCoders\database\recipes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class Manager(object):

    def __init__(self):
        pass

    @property
    def recipes(self):
        found_recipes = session.query(Recipe)
        if found_recipes:
            return found_recipes.all()
        return None