from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Usuario %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class Personajes(db.Model):
    __tablename__ = 'personajes'
  
    id = db.Column(db.Integer, primary_key=True)
    name_people= db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Personaje %r>' % self.name_people

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name_people,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            # do not serialize the password, its a security breach
        }
    

class Planetas(db.Model):
    __tablename__ = 'planetas'
   
    id = db.Column(db.Integer, primary_key=True)
    name_planet= db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Planeta %r>' % self.name_planet

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name_planet,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            # do not serialize the password, its a security breach
        }
    
class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    usuario = db.relationship(User)
    personajes_id = db.Column(db.Integer, db.ForeignKey('personajes.id'))
    personajes = db.relationship(Personajes)
    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id'))
    planetas = db.relationship(Planetas)

    def __repr__(self):
        return '<favorito %r>' % self.usuario

    def serialize(self):
        return {
        "id": self.id,
        "usuario": self.usuario.serialize(),  
        "personajes": self.personajes.serialize(), 
        "planetas": self.planetas.serialize(),  
    }
    
