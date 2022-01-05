from petevent import db_alchemy


class Customers(db_alchemy.Model):
    id = db_alchemy.Column(db_alchemy.Integer, primary_key=True)
    Name = db_alchemy.Column(db_alchemy.String(100), nullable=False)
    Address = db_alchemy.Column(db_alchemy.String(100), nullable=False)
    Email = db_alchemy.Column(db_alchemy.String(45), nullable=False)
    Phone = db_alchemy.Column(db_alchemy.String(45), nullable=False)

    def __repr__(self):
        return "Customer({}, {})".format(self.Name, self.Email)


class Events(db_alchemy.Model):
    id = db_alchemy.Column(db_alchemy.Integer, primary_key=True)
    pet_id = db_alchemy.Column(db_alchemy.Integer, db_alchemy.ForeignKey('pets.id'))
    Date = db_alchemy.Column(db_alchemy.Date, nullable=False)
    Pet = db_alchemy.Column(db_alchemy.String(15), nullable=False)
    Event = db_alchemy.Column(db_alchemy.String(45), nullable=False)
    Transport = db_alchemy.Column(db_alchemy.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Event('{self.Event}', '{self.Date}')"


class Pets(db_alchemy.Model):
    id = db_alchemy.Column(db_alchemy.Integer, primary_key=True)
    customer_id = db_alchemy.Column(db_alchemy.Integer, db_alchemy.ForeignKey('customers.id'))
    Name = db_alchemy.Column(db_alchemy.String(15), nullable=False)
    Breed = db_alchemy.Column(db_alchemy.String(100), nullable=False)
    Gender = db_alchemy.Column(db_alchemy.Boolean, nullable=False)
    Weight = db_alchemy.Column(db_alchemy.Integer, nullable=False)
    IsClient = db_alchemy.Column(db_alchemy.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"Pet('{self.Name}', '{self.Breed}', '{self.Gender}')"


class Addresses(db_alchemy.Model):
    id = db_alchemy.Column(db_alchemy.Integer, primary_key=True)
    customer_id = db_alchemy.Column(db_alchemy.Integer, db_alchemy.ForeignKey('customers.id'))
    ZipCode = db_alchemy.Column(db_alchemy.String(8), nullable=False)
    Location = db_alchemy.Column(db_alchemy.String(100), nullable=False)
    District = db_alchemy.Column(db_alchemy.String(100), nullable=False)
    City = db_alchemy.Column(db_alchemy.String(45), nullable=False)
    State = db_alchemy.Column(db_alchemy.String(2), nullable=False)
    Number = db_alchemy.Column(db_alchemy.String(10), nullable=False)
    Complement = db_alchemy.Column(db_alchemy.String(15), nullable=False)

    def __repr__(self):
        return f"Address('{self.customer_id}' - '{self.Location}', '{self.District}', '{self.City}' - '{self.State}')"
