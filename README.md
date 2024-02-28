# FOOD
#### Video Demo: https://youtu.be/fAoQFMFd43c
#### Description:
## Overview
My final project, FOOD, is a web application that relies on a user-populated database to help users narrow down food choices when they are getting hungry and can't decide what they would like to eat.

After creating an account, users will add input to different categories: restaurants, dishes, cuisines, sensory descriptors, and dietary restrictions. They will then use the tag pages to connect their inputs. Restaurants and dishes can be tagged with inputs from the other categories in order to describe them. Dishes can also be tagged to restaurants in order to create a menu of dishes for each restaurant that the user enjoys. The takeout tag is to indicate whether a restaurant allows takeout ordering.

After tagging, users can navigate to the dashboard. All of their inputs will appear in a table, organized by category. Restaurants and dishes appear as buttons, while the other categories are checkboxes. 

If a restaurant is clicked, the table will update to show all of the dishes that are available at the selected restaurant, and checkboxes will appear checked with any tagged descriptors of the restaurant. 

If a dish is clicked, only restaurants that serve that dish will appear, and any descriptors assigned to that dish will appear checked.

Users can also check boxes of any of the descriptor tags they desire, and then click submit. The table will then update to only include restaurants and dishes with those exact descriptors assigned to them ("and" logic, not "or").

Tagging and untagging is easy, as the tag pages display all of the user's previous tags for each category. Tags "By Restaurant" and "By Dish" display the same information, just organized differently.

Users can also delete any inputs that may be cluttering their dashboard by navigating to the Delete page.

## Functionality/Files

### food.db
The database containing tables of users, categories, inputs, category tags (links categories to inputs), and input tags (links inputs to other inputs).

### schema.sql
Structure/schema of food.db.

### app.py
Contains functions and paths to connect the database and HTML templates. Uses some functions and elements from previous problem sets (register, login, logout, session/filesystem/after_request) to aid in functionality.

### helpers.py
Contains apology() and login_required() functions from previous problem set (Finance) to aid in functionality.

### styles.css
Additional css style elements to quickly supplement bootstrap elements.

### layout.html
The layout of all HTML pages, contains the HTML for the navbar. Contains bootstrap stylesheet and script for quick style and functionality.

### register.html and login.html
Allows users to register and login, connects to register() and login() functions in app.py

### add.html
HTML that connects to add() function in app.py, allows users to add input to a selected category.

### restaurant_tag.html and dish_tag.html
HTML that connects to restaurant_tag() and dish_tag() functions. Allows users to view current tags, select and deselect tags for restaurants and dishes.

### index.html
HTML for the dynamic dashboard/homepage, connects to index() function in app.py. Allows users to interact with their created database, filter existing restaurant and dish options.

### delete.html
HTML that connects to delete() in app.py, allows users to delete inputs.

### apology.html
HTML that connects to apology() in helpers.py, returns error codes for users if something goes wrong.


## Goals
When brainstorming ideas for my final project, I aimed to build off of what I learned from CS50 to reinforce my understanding. I wanted to create something that had potential to evolve in the future with further functionality, rather than a binary tool.

"Fiftyville" was one of my favorite problem sets, as it was fun tying data together to solve a puzzle. I wanted to design a program and database that could reliably and safely tie data together with user interaction. Deciding what one wants to eat is a common question that I hope this web application can help answer.

## Challenges and Triumphs
The first major challenge of this project was designing the database to efficiently allow user interaction and input while maintaining its integrity. I wanted users to be able to add as many descriptors a desired, so I researched tagging techniques within SQL that avoid redundancy. My research landed me upon something similar to an adjacency list. I also considered a nested set model; however it seemed a bit overly complicated for this particular application.

Another challenge and triumph was the creation of a dynamic dashboard. Designing a solution for secure and dynamic SQL queries based off of user interaction was an exciting puzzle that deepened my understanding of how Python handles variables. Also, figuring out how to pass a list of variables to db.execute took longer than I care to admit, as in my research, most people seemed to be able to do this without issue. However, I used the CS50 module, which requires an asterisk in front of the variable list. This taught me an important lesson on reading documentation.

Figuring out a way to maintain checked checkboxes on the dashboard and tag pages was maybe the most exciting challenge and triumph for me. My first iteration of tag pages prevented duplicate tags and allowed adding tags, but could not untag and was maybe unintuitive for the user, as it required them to remember what they had previously tagged if they wanted to adjust after their initial submission. This taught me more about how Jinja handles defining variables and an interesting workaround to pass a Boolean into and out of loops.

## What Could Be Improved
Ultimately, this final project hammered in the importance of accepting where I am at and moving forward despite that ("Perfection is the enemy of progress"). 

I spent a lot of time hemming and hawing over database design and rewriting it, trying to think too far in the future for possible functionality. But I knew I could never know what would be the completely ideal scenario without starting, trying, making mistakes and learning from them. Now, a change that I would make would be to eliminate the category_tags table altogether and just include category_id as another column in the inputs table. My original idea was the possibility of having a single input be tagged as multiple things (e.g., a restaurant named after a dish); however, this can get dicey with data integrity and, in a scenario where it works, might require overly verbose checks in the code. It would be easier to just have two inputs with the same name and different primary keys that are locked to a category, and I ended up preventing the ability to input identical entries to the inputs table in order to move forward.

There are also several spots, such as the SQL queries for lists of individual categories, that could be written more concisely, dynamically, and elegantly with loops and perhaps some recursion, but to continue progress I wrote what worked for me at the moment.

## Future Development
This web application could be developed further in several interesting ways:

- Building off of a larger user base, the ability to add friends, share restaurants, dishes, menus, etc., starting a "party" where friends can have deciding/voting sessions to fairly compromise on a meal option could all be implemented.

- Adding the ability to pull information (nearby restaurants, cuisine, menu items, and takeout options) from search engines and websites to save time and effort for the user.

- This could be a template for restaurant websites to create dynamic menus for patrons. Patrons could filter items for dietary restrictions/needs or cravings.