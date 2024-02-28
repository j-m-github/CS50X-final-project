import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///food.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method =="POST":
        y_restaurant = request.form.get("restaurant")
        y_dish = request.form.get("dish")
        y_cuisines = request.form.getlist("cuisine")
        y_senses = request.form.getlist("sense")
        y_dietaries = request.form.getlist("dietary")
        y_takeout = request.form.getlist("takeout")

        tags = [y_cuisines, y_senses, y_dietaries]

        if y_restaurant:
            restaurants = db.execute(
                "SELECT * FROM inputs WHERE user_id = ? AND id = ?",
                session["user_id"],
                y_restaurant
            )
            dishes = db.execute(
                """SELECT * FROM inputs WHERE user_id = ? AND id IN 
                (SELECT input_id FROM category_tags WHERE cat_id = 
                (SELECT id FROM categories WHERE category = 'Dishes'))
                AND id IN (SELECT tag_id FROM input_tags WHERE item_id = ?)""",
                session["user_id"],
                y_restaurant
            )
            y_cuisines = []
            dbcuisines = db.execute(
                """SELECT tag_id FROM input_tags WHERE user_id = ? AND item_id = ?
                AND tag_id IN (SELECT input_id FROM category_tags WHERE cat_id = 
                (SELECT id FROM categories WHERE category = 'Cuisines'))""",
                session["user_id"],
                y_restaurant
            )
            for x in dbcuisines:
                y_cuisines.append(x["tag_id"])
            y_senses = []
            dbsenses = db.execute(
                """SELECT tag_id FROM input_tags WHERE user_id = ? AND item_id = ?
                AND tag_id IN (SELECT input_id FROM category_tags WHERE cat_id = 
                (SELECT id FROM categories WHERE category = 'Senses'))""",
                session["user_id"],
                y_restaurant
            )
            for x in dbsenses:
                y_senses.append(x["tag_id"])
            y_dietaries = []
            dbdietaries = db.execute(
                """SELECT tag_id FROM input_tags WHERE user_id = ? AND item_id = ?
                AND tag_id IN (SELECT input_id FROM category_tags WHERE cat_id = 
                (SELECT id FROM categories WHERE category = 'Dietaries'))""",
                session["user_id"],
                y_restaurant
            )
            for x in dbdietaries:
                y_dietaries.append(x["tag_id"])
            y_takeout = []
            dbtakeout = db.execute(
                """SELECT cat_id FROM category_tags WHERE user_id = ? AND input_id = ?
                AND cat_id = (SELECT id FROM categories WHERE category = 'Takeout')""",
                session["user_id"],
                y_restaurant
                )
            for x in dbtakeout:
                y_takeout.append(x["cat_id"])
        elif y_dish:
            dishes = db.execute(
                """SELECT * FROM inputs WHERE user_id = ? AND id = ?""",
                session["user_id"],
                y_dish
            )
            restaurants = db.execute(
                """SELECT * FROM inputs WHERE user_id = ? AND id IN 
                (SELECT input_id FROM category_tags WHERE cat_id = 
                (SELECT id FROM categories WHERE category = 'Restaurants'))
                AND id IN (SELECT item_id FROM input_tags WHERE tag_id = ?)""",
                session["user_id"],
                y_dish
            )
            y_cuisines = []
            dbcuisines = db.execute(
                """SELECT tag_id FROM input_tags WHERE user_id = ? AND item_id = ?
                AND tag_id IN (SELECT input_id FROM category_tags WHERE cat_id = 
                (SELECT id FROM categories WHERE category = 'Cuisines'))""",
                session["user_id"],
                y_dish
            )
            for x in dbcuisines:
                y_cuisines.append(x["tag_id"])
            y_senses = []
            dbsenses = db.execute(
                """SELECT tag_id FROM input_tags WHERE user_id = ? AND item_id = ?
                AND tag_id IN (SELECT input_id FROM category_tags WHERE cat_id = 
                (SELECT id FROM categories WHERE category = 'Senses'))""",
                session["user_id"],
                y_dish
            )
            for x in dbsenses:
                y_senses.append(x["tag_id"])
            y_dietaries = []
            dbdietaries = db.execute(
                """SELECT tag_id FROM input_tags WHERE user_id = ? AND item_id = ?
                AND tag_id IN (SELECT input_id FROM category_tags WHERE cat_id = 
                (SELECT id FROM categories WHERE category = 'Dietaries'))""",
                session["user_id"],
                y_dish
            )
            for x in dbdietaries:
                y_dietaries.append(x["tag_id"])
            y_takeout = []
            dbtakeout = db.execute(
                """SELECT cat_id FROM category_tags WHERE user_id = ? AND input_id = ?
                AND cat_id = (SELECT id FROM categories WHERE category = 'Takeout')""",
                session["user_id"],
                y_dish
                )
            for x in dbtakeout:
                y_takeout.append(x["cat_id"])
        else:
            queryr = "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Restaurants'))"
            queryd = "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dishes'))"
            varr = [session["user_id"]]
            vard = [session["user_id"]]
            add = " AND id IN (SELECT item_id FROM input_tags WHERE user_id = ? AND tag_id = ?)"
            addto = " AND id IN (SELECT input_id FROM category_tags WHERE user_id = ? AND cat_id = ?)"

            for cat in tags:
                if len(cat) > 0:
                    for tag in cat:
                        queryr = queryr + add
                        queryd = queryd + add
                        varr.append(session["user_id"])
                        varr.append(tag)
                        vard.append(session["user_id"])
                        vard.append(tag)
            if len(y_takeout) > 0:
                for yes in y_takeout:
                    queryr = queryr + addto
                    varr.append(session["user_id"])
                    varr.append(yes)
            restaurants = db.execute(queryr, *varr)
            dishes = db.execute(queryd, *vard)
        cuisines = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Cuisines'))", 
            session["user_id"]
            )
        senses = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Senses'))", 
            session["user_id"]
            )
        dietaries = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dietaries'))", 
            session["user_id"]
            )
        takeout = db.execute(
            "SELECT * FROM categories WHERE category = 'Takeout'"
        )

        return render_template(
            "index.html",
            restaurants=restaurants,
            dishes=dishes,
            cuisines=cuisines,
            senses=senses,
            dietaries=dietaries,
            takeout=takeout,
            y_cuisines=y_cuisines,
            y_senses=y_senses,
            y_dietaries=y_dietaries,
            y_takeout=y_takeout
            )
    else:
        # Display table of data tied to user database
        # Send category names to html
        restaurants = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Restaurants'))", 
            session["user_id"]
            )
        dishes = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dishes'))", 
            session["user_id"]
            )
        cuisines = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Cuisines'))", 
            session["user_id"]
            )
        senses = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Senses'))", 
            session["user_id"]
            )
        dietaries = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dietaries'))", 
            session["user_id"]
            )
        takeout = db.execute(
            "SELECT * FROM categories WHERE category = 'Takeout'"
        )
    
        return render_template(
            "index.html", 
            restaurants=restaurants,
            dishes=dishes,
            cuisines=cuisines,
            senses=senses,
            dietaries=dietaries,
            takeout=takeout
            )


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        categories = db.execute("SELECT * FROM categories WHERE category NOT LIKE 'Takeout'")
        category = request.form.get("category")
        entry = request.form.get("entry")

        # check for valid category
        checkc = False
        for row in categories:
            if category == row["category"]:
                checkc = True
        if not checkc:
            return apology("please select from provided categories")

        db.execute("BEGIN TRANSACTION")
        check = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND input = ?",
            session["user_id"],
            entry
        )
        if len(check) == 0:
            db.execute(
                "INSERT INTO inputs (user_id, input) VALUES (?, ?)",
                session["user_id"],
                entry
                )
            db.execute(
                "INSERT INTO category_tags (user_id, input_id, cat_id) VALUES (?, (SELECT id FROM inputs WHERE user_id = ? AND input = ?), (SELECT id FROM categories WHERE category = ?))",
                session["user_id"],
                session["user_id"],
                entry,
                category
            )
            message = "Added " + entry + " to the " + category + " category"
            flash(message)
        else:
            flash("Entry already exists, please enter unique input")
        db.execute("COMMIT")
        return render_template("add.html", categories=categories, category=category, entry=entry)
    else:
        # List categories for user to select and add to
        categories = db.execute("SELECT * FROM categories WHERE category NOT LIKE 'Takeout'")
        return render_template("add.html", categories=categories)
    

@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        deletion = request.form.get("deletion")
        id, sep, input = deletion.partition('_')
        id = int(id)

        # check for valid input
        db.execute("BEGIN TRANSACTION")
        check = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id = ?",
            session["user_id"],
            id
        )
        if check != 0 and check[0]["id"] == id and check[0]["input"] == input:
            db.execute(
                "DELETE FROM category_tags WHERE user_id = ? AND input_id = ?",
                session["user_id"],
                id
            )
            db.execute(
                "DELETE FROM input_tags WHERE user_id = ? AND (item_id = ? OR tag_id = ?)",
                session["user_id"],
                id,
                id
            )
            db.execute(
                "DELETE FROM inputs WHERE user_id = ? AND id = ?",
                session["user_id"],
                id
                )
        else:
            db.execute("END TRANSACTION")
            return apology("please select from provided options")
        db.execute("COMMIT")

        restaurants = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Restaurants'))", 
            session["user_id"]
            )
        dishes = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dishes'))", 
            session["user_id"]
            )
        cuisines = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Cuisines'))", 
            session["user_id"]
            )
        senses = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Senses'))", 
            session["user_id"]
            )
        dietaries = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dietaries'))", 
            session["user_id"]
            )
        
        message = input + " has been removed"
        flash(message)
        return render_template(
            "delete.html",
            restaurants=restaurants, 
            dishes=dishes,
            cuisines=cuisines,
            senses=senses,
            dietaries=dietaries,
            deletion=deletion
            )
    else:
        
        restaurants = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Restaurants'))", 
            session["user_id"]
            )
        dishes = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dishes'))", 
            session["user_id"]
            )
        cuisines = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Cuisines'))", 
            session["user_id"]
            )
        senses = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Senses'))", 
            session["user_id"]
            )
        dietaries = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dietaries'))", 
            session["user_id"]
            )
        return render_template(
            "delete.html",
            restaurants=restaurants, 
            dishes=dishes,
            cuisines=cuisines,
            senses=senses,
            dietaries=dietaries
            )

    

@app.route("/restaurant_tag", methods=["GET", "POST"])
@login_required
def restaurant_tag():
    if request.method == "POST":
        # update changed checkbox/tags, don't change unchanged
        y_dishes = request.form.getlist("dish")
        y_cuisines = request.form.getlist("cuisine")
        y_senses = request.form.getlist("sense")
        y_dietaries = request.form.getlist("dietary")
        y_takeout = request.form.getlist("takeout")

        db.execute("BEGIN TRANSACTION")
        old_tags = db.execute(
            "SELECT * FROM input_tags WHERE user_id = ?",
            session["user_id"]
        )
        new_tags = [y_dishes, y_cuisines, y_senses, y_dietaries]
        old_takeout = db.execute(
            "SELECT * FROM category_tags WHERE user_id = ? AND cat_id = (SELECT id FROM categories WHERE category = 'Takeout')",
            session["user_id"]
        )

        # Deletes deselected takeout tags
        for row in old_takeout:
            check = False
            if len(y_takeout) > 0:
                for rest in y_takeout:
                    if row["input_id"] == rest:
                        check = True
                        break
            if not check:
                db.execute(
                    """DELETE FROM category_tags WHERE user_id = ? AND input_id = ? AND cat_id = 
                    (SELECT id FROM categories WHERE category = 'Takeout')""",
                    session["user_id"],
                    row["input_id"]
                )

        # Adds selected takeout tags
        if len(y_takeout) > 0:
            for rest in y_takeout:
                check = db.execute(
                    """SELECT * FROM category_tags WHERE user_id = ? AND input_id = ? AND cat_id = 
                    (SELECT id FROM categories WHERE category = 'Takeout')""",
                    session["user_id"],
                    rest
                )
                if len(check) == 0:
                    db.execute(
                        """INSERT INTO category_tags (user_id, input_id, cat_id) VALUES (?, ?, (SELECT id FROM categories WHERE category = 'Takeout'))""",
                        session["user_id"],
                        rest
                    )

        # Deletes deselected tags
        for row in old_tags:
            check = False
            for cat in new_tags:
                if len(cat) > 0:
                    for new_tag in cat:
                        item_id, sep, tag_id = new_tag.partition('_')
                        item_id = int(item_id)
                        tag_id = int(tag_id)
                        if row["item_id"] == item_id and row["tag_id"] == tag_id:
                            check = True
                            break
                if check:
                    break
            if not check:
                db.execute(
                    """DELETE FROM input_tags WHERE user_id = ? AND item_id = ? AND tag_id = ? AND item_id IN
                    (SELECT input_id FROM category_tags WHERE user_id = ? AND cat_id = 
                    (SELECT id FROM categories WHERE category = 'Restaurants'))""",
                    session["user_id"],
                    row["item_id"],
                    row["tag_id"],
                    session["user_id"]
                )

        # Adds newly selected tags
        for cat in new_tags:
            if len(cat) > 0:
                for new_tag in cat:
                    item_id, sep, tag_id = new_tag.partition('_')
                    check = db.execute(
                        "SELECT * FROM input_tags WHERE user_id = ? AND item_id = ? AND tag_id = ?",
                        session["user_id"],
                        item_id,
                        tag_id
                    )
                    if len(check) == 0:
                        db.execute(
                            "INSERT INTO input_tags (user_id, item_id, tag_id) VALUES (?, ?, ?)",
                            session["user_id"],
                            item_id,
                            tag_id
                        )
        db.execute("COMMIT")

        restaurants = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Restaurants'))", 
            session["user_id"]
            )
        dishes = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dishes'))", 
            session["user_id"]
            )
        cuisines = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Cuisines'))", 
            session["user_id"]
            )
        senses = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Senses'))", 
            session["user_id"]
            )
        dietaries = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dietaries'))", 
            session["user_id"]
            )
        
        tags = db.execute(
            "SELECT * FROM input_tags WHERE user_id = ?",
            session["user_id"]
        )

        takeout = db.execute(
            "SELECT * FROM category_tags WHERE user_id = ? AND cat_id = (SELECT id FROM categories WHERE category = 'Takeout')",
            session["user_id"]
        )

        flash("Tags saved!")

        return render_template(
            "restaurant_tag.html",
            restaurants=restaurants, 
            dishes=dishes,
            cuisines=cuisines,
            senses=senses,
            dietaries=dietaries,
            tags=tags,
            takeout=takeout
        )
    else:
        # list all available tags for each dish and restaurant
        # have existing tags already checked
        restaurants = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Restaurants'))", 
            session["user_id"]
            )
        dishes = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dishes'))", 
            session["user_id"]
            )
        cuisines = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Cuisines'))", 
            session["user_id"]
            )
        senses = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Senses'))", 
            session["user_id"]
            )
        dietaries = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dietaries'))", 
            session["user_id"]
            )
        tags = db.execute(
            "SELECT * FROM input_tags WHERE user_id = ?",
            session["user_id"]
        )
        takeout = db.execute(
            "SELECT * FROM category_tags WHERE user_id = ? AND cat_id = (SELECT id FROM categories WHERE category = 'Takeout')",
            session["user_id"]
        )

        return render_template(
            "restaurant_tag.html", 
            restaurants=restaurants, 
            dishes=dishes,
            cuisines=cuisines,
            senses=senses,
            dietaries=dietaries,
            tags=tags,
            takeout=takeout
            )
    

@app.route("/dish_tag", methods=["GET", "POST"])
@login_required
def dish_tag():
    if request.method == "POST":
        # update changed checkbox/tags, don't change unchanged
        y_restaurants = request.form.getlist("restaurant")
        y_cuisines = request.form.getlist("cuisine")
        y_senses = request.form.getlist("sense")
        y_dietaries = request.form.getlist("dietary")

        db.execute("BEGIN TRANSACTION")
        old_tags = db.execute(
            "SELECT * FROM input_tags WHERE user_id = ?",
            session["user_id"]
        )
        new_tags = [y_restaurants, y_cuisines, y_senses, y_dietaries]

        # Deletes unselected tags
        for row in old_tags:
            check = False
            for cat in new_tags:
                if len(cat) > 0:
                    for new_tag in cat:
                        item_id, sep, tag_id = new_tag.partition('_')
                        item_id = int(item_id)
                        tag_id = int(tag_id)
                        if row["item_id"] == item_id and row["tag_id"] == tag_id:
                            check = True
                            break
                if check:
                    break
            if not check:
                db.execute(
                    """DELETE FROM input_tags WHERE 
                    (user_id = ? AND item_id = ? AND tag_id = ? AND item_id IN 
                    (SELECT input_id FROM category_tags WHERE user_id = ? AND cat_id = 
                    (SELECT id FROM categories WHERE category = 'Dishes')))
                    OR (user_id = ? AND item_id = ? AND tag_id = ? AND item_id IN
                    (SELECT input_id FROM category_tags WHERE user_id = ? AND cat_id = 
                    (SELECT id FROM categories WHERE category = 'Restaurants'))
                    AND tag_id IN (SELECT input_id FROM category_tags WHERE user_id = ? AND cat_id = 
                    (SELECT id FROM categories WHERE category = 'Dishes')))""",
                    session["user_id"],
                    row["item_id"],
                    row["tag_id"],
                    session["user_id"],
                    session["user_id"],
                    row["item_id"],
                    row["tag_id"],
                    session["user_id"],
                    session["user_id"]
                )

        # Adds newly selected tags
        for cat in new_tags:
            if len(cat) > 0:
                for new_tag in cat:
                    item_id, sep, tag_id = new_tag.partition('_')
                    check = db.execute(
                        "SELECT * FROM input_tags WHERE user_id = ? AND item_id = ? AND tag_id = ?",
                        session["user_id"],
                        item_id,
                        tag_id
                    )
                    if len(check) == 0:
                        db.execute(
                            "INSERT INTO input_tags (user_id, item_id, tag_id) VALUES (?, ?, ?)",
                            session["user_id"],
                            item_id,
                            tag_id
                        )
        db.execute("COMMIT")

        restaurants = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Restaurants'))", 
            session["user_id"]
            )
        dishes = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dishes'))", 
            session["user_id"]
            )
        cuisines = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Cuisines'))", 
            session["user_id"]
            )
        senses = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Senses'))", 
            session["user_id"]
            )
        dietaries = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dietaries'))", 
            session["user_id"]
            )
        
        tags = db.execute(
            "SELECT * FROM input_tags WHERE user_id = ?",
            session["user_id"]
        )
        
        flash("Tags saved!")

        return render_template(
            "dish_tag.html",
            restaurants=restaurants, 
            dishes=dishes,
            cuisines=cuisines,
            senses=senses,
            dietaries=dietaries,
            tags=tags
        )
    else:
        # list all available tags for each dish and restaurant
        # have existing tags already checked
        restaurants = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Restaurants'))", 
            session["user_id"]
            )
        dishes = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dishes'))", 
            session["user_id"]
            )
        cuisines = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Cuisines'))", 
            session["user_id"]
            )
        senses = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Senses'))", 
            session["user_id"]
            )
        dietaries = db.execute(
            "SELECT * FROM inputs WHERE user_id = ? AND id IN (SELECT input_id FROM category_tags WHERE cat_id = (SELECT id FROM categories WHERE category = 'Dietaries'))", 
            session["user_id"]
            )
        
        tags = db.execute(
            "SELECT * FROM input_tags WHERE user_id = ?",
            session["user_id"]
        )

        return render_template(
            "dish_tag.html", 
            restaurants=restaurants, 
            dishes=dishes,
            cuisines=cuisines,
            senses=senses,
            dietaries=dietaries,
            tags=tags
            )
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username").lower(),
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and confirmation match
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("password must match confirmation", 400)

        # Ensure password contains criteria (Number, lower, Upper, 6 len)
        num = False
        low = False
        up = False
        length = False

        for c in request.form.get("password"):
            if c.isnumeric():
                num = True
            if c.islower():
                low = True
            if c.isupper():
                up = True
        if len(request.form.get("password")) >= 6:
            length = True

        if num == False or low == False or up == False or length == False:
            return apology("password does not meet criteria", 400)

        # Query database for username
        db.execute("BEGIN TRANSACTION")
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username").lower(),
        )

        # Ensure username is unique
        if len(rows) != 0:
            db.execute("END TRANSACTION")
            return apology("username already exists", 400)

        # Store username and password into database as a new user
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username").lower(),
            generate_password_hash(request.form.get("password")),
        )

        # Update user list
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username").lower(),
        )
        db.execute("COMMIT")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Flash message
        flash("Registered!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")