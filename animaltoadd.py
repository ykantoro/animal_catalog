
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Species, Base, Animal, User
import datetime
import time
 


engine = create_engine('sqlite:///speciesandanimals.db')
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

now = datetime.datetime.now()

# Create dummy user
User1 = User(name="Yelana Webb", email="yelana.webb@gmail.com",
             picture='https://lh4.googleusercontent.com/-NtvOdTj7iZg/VKDw5dx4ZnI/AAAAAAAAHbM/gkwMgpa4LFE/s256-no/f2b199bc-6fd8-42d9-8483-0c286e655bf1')
session.add(User1)
session.commit()

# Animals for Cats
species1 = Species(user_id=1, name="Cats", 
       picture = "http://images5.fanpop.com/image/photos/28500000/Cats-cats-28572014-1600-1200.jpg")
session.add(species1)
session.commit()

# Animals for Dogs
species2 = Species(user_id=1, name="Dogs", 
       picture = "http://intl.petsafe.net/intl/blog/wp-content/uploads/2013/05/lots-of-happy-dogs1.jpg")
session.add(species2)
session.commit()

# Animals for Pigs
species3 = Species(user_id=1, name="Pigs", 
       picture = "http://www.fixfood.org/files/pigs-1774.jpg")
session.add(species3)
session.commit()

# Animals for Monkeys
species4 = Species(user_id=1, name="Monkeys", 
       picture = "http://www.forexlifestyleguide.com/wp-content/uploads/3monkies.jpg")
session.add(species4)
session.commit()

# Animals for Turtles
species5 = Species(user_id=1, name="Turtles", 
       picture = "https://melinabeachturtlehatchery.files.wordpress.com/2010/07/turtle4.jpg")
session.add(species5)
session.commit()


# Animals for Rabbits
species6 = Species(user_id=1, name="Rabbits", 
       picture = "http://hannahsociety.com/blog/wp-content/uploads/2015/02/Wild_Rabbits_at_Edinburgh_Zoo.jpg")
session.add(species6)
session.commit()

# Animals for Birds
species7 = Species(user_id=1, name="Birds", 
       picture = "http://everythingbirdsonline.com/wp-content/uploads/2014/06/birds-of-paradise.jpg")
session.add(species7)
session.commit()

# Animals for Fish
species8 = Species(user_id=1, name="Fish", 
       picture = "http://www.funchap.com/wp-content/uploads/2014/07/tropical-fish-digital-art-wallpaper.jpg")
session.add(species8)
session.commit()


animal1 = Animal(user_id=1, name="Persian", 
       description = "The Persian is a long-haired breed of cat characterized by its round face and short muzzle.",
       picture = "http://holisticpetcareproducts.com/wp-content/uploads/2013/05/young-persian-cat-sitting-17952898.jpg",
       food = "meat protein",
       color = "White",
       weight = "10 lbs",
       sleep = "16 Hours",
       species = species1)
session.add(animal1)
session.commit()


animal2 = Animal(user_id=1, name="Red Tabby", 
       description = '''Red tabbies can actually range from red to orange to yellow to buff. 
       However, people generally refer to these cats as orange no matter which shade they are. 
       An orange tabby is the combination of two main traits: Color and Pattern''',
       picture = "https://s-media-cache-ak0.pinimg.com/736x/01/b7/3c/01b73c623190b6adbf1b227a98dc5649.jpg",
       food = "meat protein",
       color = "Red / Orange / Yellow / Buff",
       weight = "10 lbs",
       sleep = "16 Hours",
       species = species1)
session.add(animal2)
session.commit()



animal3 = Animal(user_id=1, name="Great Pyreneese", 
       description = "The Pyrenean Mountain Dog, known as the Great Pyrenees in North America, is a large breed of dog used as a livestock guardian dog.",
       picture = "https://chewonthisdogbarkery.files.wordpress.com/2013/06/great-pryrenees.jpg",
       food = "meat protein",
       color = "White",
       weight = "130 lbs",
       sleep = "14 Hours",
       species = species2)
session.add(animal3)
session.commit()


animal4 = Animal(user_id=1, name="Pot-bellied", 
       description = '''Considerably smaller than standard American or European farm pigs.
       Boars, intact male pigs, become fertile at six months of age, long before they are
       completely physically mature. Pot-bellied pigs are considered fully grown by six
       years of age, when the epiphyseal plates in the long bones of the legs finally close''',
       picture = "http://images.fineartamerica.com/images-medium-large-5/pot-belly-pig-dick-willis.jpg",
       food = "leaves, grasses, roots, fruits, and flowers",
       color = "Pink",
       weight = "100 to 300 lbs",
       sleep = "8 Hours",
       species = species3)
session.add(animal4)
session.commit()


animal5 = Animal(user_id=1, name="Miniature", 
       description = '''A miniature pig is a breed of pig developed and used 
       for medical research or for use as a pet. These smaller pigs were first 
       used for medical research in Europe before being introduced to the United 
       States in the 1980s. Since then, the animals have been used in studies by 
       scientists around the world, and have also risen and fallen in popularity 
       as unusual pets.''',
       picture = "http://greatinspire.com/wp-content/uploads/2013/07/35-Cute-Miniature-Pig-Pictures-17.jpg",
       food = "leaves, grasses, roots, fruits, and flowers",
       color = "Pink",
       weight = "100 to 300 lbs",
       sleep = "8 Hours",
       species = species3)
session.add(animal5)
session.commit()



animal6 = Animal(user_id=1, name="Baboon", 
       description = '''Sharing 91% DNA similarities with humans is the Baboon.
       This particular Monkey is often argued to be an Ape instead. 
       However, science has placed them into the area of being a Monkey based 
       on a variety of contributing factors.''',
       picture = "http://upload.wikimedia.org/wikipedia/commons/9/97/BABOON-e.JPG",
       food = "bananas",
       color = "Yellow and Olive",
       weight = "90 lbs",
       sleep = "10 Hours",
       species = species4)
session.add(animal6)
session.commit()


animal8 = Animal(user_id=1, name="Snapping", 
       description = '''The common snapping turtle (Chelydra serpentina) is a large freshwater 
       turtle of the family Chelydridae. Its natural range extends from southeastern Canada, 
       southwest to the edge of the Rocky Mountains, as far east as Nova Scotia and Florida. 
       This species and the larger alligator snapping turtle are the only two species in this 
       family found in North America (though the common snapping turtle, as its name implies, 
       is much more widespread).''',
       picture = "https://s-media-cache-ak0.pinimg.com/736x/01/b7/3c/01b73c623190b6adbf1b227a98dc5649.jpg",
       food = "Fish pellets and gut-loaded insects",
       color = "Green",
       weight = "175 lbs",
       sleep = "12 Hours",
       species = species5)
session.add(animal8)
session.commit()



animal9 = Animal(user_id=1, name="Great Pyreneese", 
       description = "The Pyrenean Mountain Dog, known as the Great Pyrenees in North America, is a large breed of dog used as a livestock guardian dog.",
       picture = "https://chewonthisdogbarkery.files.wordpress.com/2013/06/great-pryrenees.jpg",
       food = "meat protein",
       color = "White",
       weight = "130 lbs",
       sleep = "14 Hours",
       species = species2)
session.add(animal9)
session.commit()


animal10 = Animal(user_id=1, name="Persian", 
       description = "The Persian is a long-haired breed of cat characterized by its round face and short muzzle.",
       picture = "http://holisticpetcareproducts.com/wp-content/uploads/2013/05/young-persian-cat-sitting-17952898.jpg",
       food = "meat protein",
       color = "White",
       weight = "10 lbs",
       sleep = "16 Hours",
       species = species1)
session.add(animal10)
session.commit()


animal11 = Animal(user_id=1, name="Red Tabby", 
       description = '''Red tabbies can actually range from red to orange to yellow to buff. 
       However, people generally refer to these cats as orange no matter which shade they are. 
       An orange tabby is the combination of two main traits: Color and Pattern''',
       picture = "https://s-media-cache-ak0.pinimg.com/736x/01/b7/3c/01b73c623190b6adbf1b227a98dc5649.jpg",
       food = "meat protein",
       color = "Red / Orange / Yellow / Buff",
       weight = "10 lbs",
       sleep = "16 Hours",
       species = species1)
session.add(animal11)
session.commit()



animal12 = Animal(user_id=1, name="Great Pyreneese", 
       description = "The Pyrenean Mountain Dog, known as the Great Pyrenees in North America, is a large breed of dog used as a livestock guardian dog.",
       picture = "https://chewonthisdogbarkery.files.wordpress.com/2013/06/great-pryrenees.jpg",
       food = "meat protein",
       color = "White",
       weight = "130 lbs",
       sleep = "14 Hours",
       species = species2)
session.add(animal12)
session.commit()




print "added species and animals!"