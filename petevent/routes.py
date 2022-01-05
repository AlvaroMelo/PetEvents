from flask import redirect, render_template, request, url_for
from petevent import db, app

from petevent.helpers import save_customer, save_pet, fetch_list_of_pets, update_event
from petevent.models import Events, Customers, Pets

''' Events '''


# The home route
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        page = request.args.get('page', 1, type=int)
        events_render = Events.query \
            .order_by(Events.Date.desc(),
                      Events.Event.asc(),
                      Events.Pet.asc()) \
            .paginate(page=page, per_page=5)
        print(events_render)

        return render_template("index.html", events=events_render)

    else:

        # Cancel button
        if request.form.get("action") == "Cancel":
            return redirect("/")

        # Instead of paginating events, show all events in one page
        elif request.form.get("action") == "Show All":
            return redirect("/event/all_events")

        # Just in case
        else:
            return redirect("/")


# List all events
@app.route("/event/all_events")
def all_events():
    events = Events.query.order_by(Events.Date.desc())
    print(events)

    # For the filters, I shall fetch the years in which there were events registered:
    years = db.execute("SELECT DISTINCT strftime('%Y', Date) as year from events")

    # Also fetch the list of all pets ever registered for the filter
    list_of_pets = fetch_list_of_pets(True)

    return render_template("event/all_events.html", events=events, years=years, pets=list_of_pets)


# Register new event
@app.route("/event/new_event", methods=["GET", "POST"])
def new_event():
    if request.method == "POST":
        date = request.form.get("date")
        pet_id = request.form.get("pet")
        pet_name = db.execute("SELECT Name FROM pets WHERE id = ?", pet_id)[0]["Name"]
        event = request.form.get("event")
        transport = request.form.get("transport")

        db.execute("INSERT INTO events (pet_id, Date, pet, Event, Transport) VALUES (?, ?, ?, ?, ? )", pet_id,
                   date, pet_name, event, transport)

        return redirect("/")

    list_of_pets = fetch_list_of_pets()
    return render_template("event/new_event.html", pets=list_of_pets)


# Edit an event
@app.route("/event/edit_event/<number>", methods=["GET", "POST"])
def edit_event(number):
    if request.method == "POST":

        # Confirm button:
        if request.form.get("action") == "Confirm":
            update_event()

        # Delete button:
        elif request.form.get("action") == "Delete Event":
            event_id = request.form.get("id")
            db.execute("DELETE FROM events WHERE id = ?", event_id)

        # Cancel button - No action needed:
        else:
            pass

        return redirect("/")

    else:
        list_of_pets = fetch_list_of_pets()
        event = db.execute("SELECT * FROM events WHERE id = ?", number)[0]
        return render_template("/event/edit_event.html", pets=list_of_pets, event=event)


''' Customers '''


# Register new customer
@app.route("/customer/new_customer", methods=["GET", "POST"])
def new_customer():
    if request.method == "POST":
        save_customer()
        return redirect("/")

    return render_template("customer/new_customer.html")


# List fo customers
@app.route("/customer/customers")
def customer():
    ctm = Customers.query.order_by(Customers.Name.asc())
    return render_template("customer/customers.html", customers=ctm)


# Edit customer
@app.route("/customer/edit_customer/<number>", methods=["GET", "POST"])
def edit_customer(number):
    if request.method == "POST":
        # Confirm button
        if request.form.get("action") == "Confirm":
            save_customer()
            return redirect(url_for('customer'))

        # Cancel button
        # elif request.form.get("action") == "Cancel":
        else:
            return redirect("/customer/customer_info/{}".format(number))
    else:
        ctm = db.execute("SELECT * FROM customers WHERE id = ?", number)[0]
        address = db.execute("SELECT * FROM addresses WHERE customer_id = ?", number)[0]
        return render_template("/customer/edit_customer.html",
                               name=ctm['Name'],
                               email=ctm['Email'],
                               address=ctm['Address'],
                               phone=ctm['Phone'],
                               zip_code=address['ZipCode'],
                               location=address['Location'],
                               district=address['District'],
                               city=address['City'],
                               state=address['State'],
                               number=address['Number'],
                               complement=address['Complement'],
                               id=number)


# List all about a certain customer
@app.route("/customer/customer_info/<number>", methods=["GET", "POST"])
def customer_info(number):
    if request.method == "POST":
        # Edit customer button
        if request.form.get("action") == "Edit":
            return redirect("/customer/edit_customer/{}".format(number))

        # Register customer's pet button
        else:
            return redirect("/pet/new_pet/{}".format(number))
    else:
        statement = "SELECT * FROM customers WHERE id = ?"
        current_customer = db.execute(statement, number)[0]

        statement_pets = "SELECT * FROM pets WHERE customer_id = ?"
        customer_pets = db.execute(statement_pets, number)

        statement_address = "SELECT * FROM addresses WHERE customer_id = ?"
        customer_address = db.execute(statement_address, number)[0]

        for key, value in customer_address.items():
            if key != "id":
                current_customer[key] = value

        return render_template("customer/customer_info.html", customer=current_customer, pets=customer_pets)


''' Pets '''


# Register a new pet to a customer
@app.route("/pet/new_pet/<number>", methods=["GET", "POST"])
def new_pet(number):
    customer_id = number
    if request.method == "POST":
        name = request.form.get("name").title()
        breed = request.form.get("breed").title()
        gender = request.form.get("gender")
        weight = request.form.get("weight")

        db.execute("INSERT INTO pets (customer_id, Name, Breed, Gender, Weight) VALUES (?, ?, ?, ?, ? )",
                   customer_id, name, breed, gender, weight)
        return redirect("/")

    return render_template("pet/new_pet.html", customer_id=customer_id)


# List all pets
@app.route("/pet/pets")
def pets():
    statement = "SELECT pets.Name as PetName" \
                ", pets.Breed as PetBreed" \
                ", pets.Gender as PetGender" \
                ", pets.Weight as PetWeight" \
                ", pets.id as PetId" \
                ", customers.Name as TutorName" \
                ", customers.id as id " \
                "FROM pets INNER JOIN customers " \
                "ON pets.customer_id = customers.id " \
                "ORDER BY PetName, TutorName;"

    list_of_pets = db.execute(statement)
    for item in list_of_pets:
        if item["PetGender"] == 1:
            item["PetGender"] = "Male"
        else:
            item["PetGender"] = "Female"
    print(list_of_pets)
    return render_template("pet/pets.html", list=list_of_pets)


# List all about a certain pet
@app.route("/pet/pet_info/<number>", methods=["GET", "POST"])
def pet_info(number):
    if request.method == "POST":
        if request.form.get("action") == "Edit Pet":
            pet_id = request.form.get("id")
            return redirect("/pet/edit_pet/{}".format(pet_id))
        else:
            return redirect(url_for('pet_info'))
    else:
        statement = "SELECT * FROM pets WHERE id = ?"
        current_pet = db.execute(statement, number)[0]
        if current_pet["Gender"] == 0:
            current_pet["Gender"] = "Female"
        else:
            current_pet["Gender"] = "Male"

        if current_pet["IsClient"] == 0:
            current_pet["IsClient"] = "No"
        else:
            current_pet["IsClient"] = "Yes"

        statement_tutor = "SELECT Name FROM customers WHERE id = ?"
        tutor_name = db.execute(statement_tutor, current_pet["customer_id"])[0]["Name"]
        print(tutor_name)
        return render_template("/pet/pet_info.html", tutorName=tutor_name, pet=current_pet)


# Edit pet information
@app.route("/pet/edit_pet/<number>", methods=["GET", "POST"])
def edit_pet(number):
    if request.method == "POST":

        # Confirm button:
        if request.form.get("action") == "Confirm":
            save_pet()
            return redirect(url_for('pets'))

        # Cancel button:
        else:
            return redirect("/pet/pet_info/{}".format(number))
    else:
        statement = "SELECT * FROM pets WHERE id = ?"
        current_pet = db.execute(statement, number)[0]
        print("current_pet = {}".format(current_pet))
        return render_template("/pet/edit_pet.html", pet=current_pet)
