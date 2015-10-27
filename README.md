#Overview
This project contains a Python module that uses the sqlite3 database to store information on animals and their species. Species and animals can be viewed by all users, and new species can be added if a user is logged in. Only the owner of a species category is able to add, edit, or delete animals inside the species, as well as the specie itself.

The user will have two options for logging in: 1)Google Plus, and 2)Facebook. If the user chooses not to login, they are still able to browse the catalogs, but will not be able to create, edit or delete any entries.

#Usage
1.	Install Vagrant and VirtualBox
2.	Download the source code and unzip it
3.	Launch the Vagrant VM and log in  
	`$ vagrant up`  
	`$ vagrant ssh`
	‘cd /vagrant’ 
	`$ cd` into the directory where you have saved the file  
4.	run the database set to create necessary tables for the site
	`python database_setup.py`
5.	Run animaltoadd.py to populate the database:  
	`python animaltoadd.py`
6.	Once the species and animals have been added successfully (you will see a print statement of ‘added species and animals!’ in the terminal. 
7.	Run `$ python project.py` navigate to localhost:5000 in your browser.

#Database
The database is made up of 3 tables:
1) user
2) specie
3) animal

The user table collects information on users (such as id, name, email, and picture) once a user has logged into the site. A user must log into the site in order to add new species. Any logged in user is able to add new species.

The Specie table contains user-inserted information about an animal species. This table holds information on the animal (such as id, name, user_id of the creator, and picture).

The Animal table also contains user-inserted information about an animal and which species it belongs in. Information available in this table: description, type of food the animal eats, the color of the animal, how long the animal sleeps, the animals adult weight, the animals picture, and what species and user the animal belongs to.

#Using the site.
The site is made up of 3 template pages: 1)Species - the home page, 2)Animals, and 3)Login. When navigating to localhost:5000 the species template will be rendered. This file will also be rendered on /home and /species.

The home page renders all species in the database and allows a user to browse all of the species, regardless of whether the user is logged in or not. If the user logs into the site (using the login button), then the user is able to add a new specie. Adding a new specie happens in a pop-up overlay in the same template.

If the ‘Log In’ button is clicked, the user is taken to /login and the login.html template. From here the user has 2 options of logging in: Google Plus or Facebook. Once logged in, the user will be redirected back to the home page.

By clicking on a particular specie from the home page, the user will be taken to an animals.html template that will render more information and expose the animals associated to the species selected. Depending on whether the user is logged in and if the user is the original creator of the species, they may see options for editing, adding and deleting the species and the animals in the species. All editing is done within a pop-up overlay in the same template.

The user is able to login and logout from any page. If the user is logged in, only the Log Out button will be visible, and the user will see their ‘You are now logged in as username’. If the user is not logged in, then only the Log In button will be available.