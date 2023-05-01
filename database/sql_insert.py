from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Recipe, Ingredient, Base

engine = create_engine('sqlite:///recipes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Insert a Role in the person table
new_role = Recipe(name='shepards pie')
session.add(new_role)
session.commit()

# Insert an Topic in the topics table with a relationship to the new_role just made
new_topic = Ingredient(name='puff pastry')
session.add(new_topic)
session.commit()

# pie = session.query(Recipe).filter(Recipe.name == 'shepards pie').first()
# pie.ingredients = ingredients
# print(pie.ingredients)


print('yes')
