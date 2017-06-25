from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Cuisine, Dish, User
 
engine = create_engine('sqlite:///new-cuisinewise.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User2 = User(name="Ishani", email="ishmukherjee89@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

#Menu for UrbanBurger
cuisine1 = Cuisine(user_id=1, name = "Indian")

session.add(cuisine1)
session.commit()

dish1 = Dish(user_id=1, name = "Biriyani", description = "with rice and chicken/mutton", picurl='biriyani.jpg', recipe = "We'll add the Biriyani recipe soon", cuisine = cuisine1, created_on='2017-07-22 11:30:01', modified_on ='2017-06-24 11:30:01')

session.add(dish1)
session.commit()

dish2 = Dish(user_id=1, name = "Chicken Tikka Masala", description = "with butter", picurl='chkn_tikka_masala.jpg', recipe = "We'll add the Tikka Masala recipe soon", cuisine = cuisine1, created_on='2017-06-12 11:30:01', modified_on ='2017-06-24 11:30:01')

session.add(dish2)
session.commit()

dish3 = Dish(user_id=1, name = "Indian Pizza", description = "with awesome toppings", picurl='indian_pizza.jpg', recipe = "We'll add the Indian Pizza recipe soon", cuisine = cuisine1, created_on='2017-05-17 11:30:01', modified_on ='2017-06-24 11:30:01')

session.add(dish3)
session.commit()

dish4 = Dish(user_id=1, name = "Masala Dosa", description = "with raita", picurl='masala_dosa.jpg', recipe = "We'll add the Masala Dosa recipe soon", cuisine = cuisine1, created_on='2017-06-24 11:30:01', modified_on ='2017-01-25 11:30:01')

session.add(dish4)
session.commit()

dish5 = Dish(user_id=1, name = "Fish Curry", description = "with rice and fish", picurl='fish_curry.jpg', recipe = "We'll add the Fish Curry recipe soon", cuisine = cuisine1, created_on='2017-02-24 11:30:01', modified_on ='2017-06-24 11:30:01')

session.add(dish5)
session.commit()


#Menu for Super Stir Fry
cuisine2 = Cuisine(user_id=2, name = "Mexican")

session.add(cuisine2)
session.commit()


d1 = Dish(user_id=2, name = "Tocos", description = "with rice and chicken/mutton", picurl='tocos.jpg', recipe = "We'll add the Tocos recipe soon", cuisine = cuisine2, created_on='2017-06-24 11:30:01', modified_on ='2017-04-21 11:30:01')

session.add(d1)
session.commit()

d2 = Dish(user_id=2, name = "Rice Bowl", description = "with rice and chicken/mutton", picurl='rice_bowl.jpg', recipe = "We'll add the Rice Bowl recipe soon", cuisine = cuisine2, created_on='2017-04-03 11:30:01', modified_on ='2017-06-24 11:30:01')

session.add(d2)
session.commit()

d3 = Dish(user_id=2, name = "Enchilada", description = "with rice and chicken/mutton", picurl='enchilada.jpg', recipe = "We'll add the Enchilada recipe soon", cuisine = cuisine2, created_on='2017-05-28 11:30:01', modified_on ='2017-06-24 11:30:01')

session.add(d3)
session.commit()

d4 = Dish(user_id=2, name = "Burrito", description = "with rice and chicken/mutton", picurl='burrito.jpg', recipe = "We'll add the Burrito recipe soon", cuisine = cuisine2, created_on='2017-06-12 11:30:01', modified_on ='2017-06-24 11:30:01')

session.add(d4)
session.commit()

d5 = Dish(user_id=2, name = "Quesadilla", description = "with sauce", picurl='quesadilla.jpg', recipe = "We'll add the Quesadilla recipe soon", cuisine = cuisine2, created_on='2017-06-24 11:30:01', modified_on ='2017-05-22 11:30:01')

session.add(d5)
session.commit()



print "added menu items!"