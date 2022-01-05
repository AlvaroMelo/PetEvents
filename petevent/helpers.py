from flask import request
from petevent import db


# Save customer on database
def save_customer():
    customer_id = request.form.get("id")
    print(customer_id)

    zip_code = request.form.get("zip_code")
    location = request.form.get("location")
    district = request.form.get("district")
    city = request.form.get("city")
    state = request.form.get("state")
    number = request.form.get("number")
    complement = request.form.get("complement")

    name = request.form.get("name").title()
    phone = request.form.get("phone")
    email = request.form.get("email")
    address = "{}, {}, {} - {}".format(location, number, city, state)

    if customer_id is None:
        statement_customer = "INSERT INTO customers (Name, Address, Email, Phone) VALUES (?, ?, ?, ? )"
        statement_address = "INSERT INTO addresses" \
                            "(customer_id, ZipCode, Location, District, City, State, Number, Complement)" \
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        customer_id = db.execute(statement_customer, name, address, email, phone)
        db.execute(statement_address, customer_id, zip_code, location, district, city, state, number, complement)
    else:
        statement_customer = "UPDATE customers SET Name= ?, Email= ?, Address = ?, Phone= ? WHERE id = ?"
        statement_address = "UPDATE addresses SET " \
                            "ZipCode = ?, Location = ?, District = ?, City = ?, " \
                            "State = ?, Number = ?, Complement = ? WHERE customer_id = ?"

        db.execute(statement_customer, name, email, address, phone, customer_id)
        db.execute(statement_address, zip_code, location, district, city,
                   state, number, complement, customer_id)


# Save pet on database
def save_pet():
    pet_id = request.form.get("id")
    name = request.form.get("name").title()
    breed = request.form.get("breed")
    gender = request.form.get("gender")
    weight = request.form.get("weight")
    is_active = request.form.get("is_client")

    statement = "UPDATE pets SET Name = ?, Breed = ?, Gender = ?, Weight = ?, IsClient = ? WHERE id = ?"
    db.execute(statement, name, breed, gender, weight, is_active, pet_id)


# Fetch list of pets alphabetically
def fetch_list_of_pets(full_list=False):
    if full_list:
        return db.execute("SELECT id, Name FROM pets ORDER BY Name")
    else:
        return db.execute("SELECT id, Name FROM pets WHERE IsClient = ? ORDER BY Name", 1)


def update_event():
    event_id = request.form.get("id")
    date = request.form.get("date")
    pet_id = request.form.get("pet")
    pet_name = db.execute("SELECT Name FROM pets WHERE id = ?", pet_id)[0]["Name"]
    event = request.form.get("event")
    transport = request.form.get("transport")

    statement = "UPDATE events SET pet_id = ?, Date = ?, Pet = ?, Event = ?, Transport = ?" \
                " WHERE id = ?"
    db.execute(statement, pet_id, date, pet_name, event, transport, event_id)
