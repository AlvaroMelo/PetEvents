from flask import request
from petevent import db, db_alchemy

from petevent.forms import NewCustomerForm
from petevent.models import Addresses, Customers


# Save customer on database
def save_customer(form: NewCustomerForm, customer_id: int = None) -> None:
    zip_code = form.zip_code.data
    location = form.location.data
    district = form.district.data
    city = form.city.data
    state = form.state.data
    number = form.number.data
    complement = form.complement.data

    name = form.name.data.title()
    phone = form.phone.data
    email = form.email.data
    address = "{}, {}, {} - {}".format(location, number, city, state)

    if customer_id is None:
        new_customer = Customers(Name=name, Address=address, Email=email, Phone=phone)
        db_alchemy.session.add(new_customer)
        db_alchemy.session.commit()
        customer_id = Customers.query.order_by(Customers.id.desc()).first().id

        customer_address = Addresses(customer_id=customer_id, ZipCode=zip_code, Location=location, District=district,
                                     City=city, State=state, Number=number, Complement=complement)
        db_alchemy.session.add(customer_address)
        db_alchemy.session.commit()

    else:
        updated_customer = Customers.query.get_or_404(customer_id)
        updated_customer.Name = name
        updated_customer.Address = address
        updated_customer.Email = email
        updated_customer.Phone = phone

        updated_customer.full_address[0].ZipCode = zip_code
        updated_customer.full_address[0].Location = location
        updated_customer.full_address[0].District = district
        updated_customer.full_address[0].City = city
        updated_customer.full_address[0].State = state
        updated_customer.full_address[0].Number = number
        updated_customer.full_address[0].Complement = complement
        db_alchemy.session.commit()


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


def get_choices():
    pets_list = fetch_list_of_pets()
    choices = [("", "Select a Pet")]
    for pet in pets_list:
        choices.append((pet['id'], pet['Name']))
    return choices
