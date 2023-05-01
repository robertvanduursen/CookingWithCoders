from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import backref

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('ingredients_id', Integer, ForeignKey('ingredients.id')),
    Column('recipes_id', Integer, ForeignKey('recipes.id'))
)

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))

    ingredients = relationship(
        "Ingredient",
        secondary=association_table,
        back_populates="recipes")



class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    description = Column(String(250))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))

    recipes = relationship(
        "Recipe",
        secondary=association_table,
        back_populates="ingredients")


if __name__ == '__main__':
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///recipes.db')

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

    print('<create> finished')
