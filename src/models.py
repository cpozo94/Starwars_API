from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    user_name = db.Column(db.String(25),nullable=False)
    first_name= db.Column(db.String(50),nullable=False)
    last_name= db.Column(db.String(50),nullable=False)
    register_data = db.Column(db.String(50),nullable=False)
    favorites= db.relationship("Favorites")  ##relacion entre clases  1 a N = multiples favoritos,


    def __init__(self):
        self.id=id
        self.email= email
        self.is_active = True
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.register_data= register_data

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active":self.is_active,
            "user_name":self.user_name,
            "first_name":self.user_name,
            "last_name":self.last_name,
            "register_data": self.register_data,
           
        }


class People(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(120), unique=True, nullable=False)
    birth_date= db.Column(db.String(120), unique=True, nullable=False)
    description= db.Column(db.String(120), unique=True, nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False) #relacion de tabla.id
    planet= db.relationship("Planet") #relacion entre clases 
    eye_color=db.Column(db.String(120), unique=True, nullable=False)
    hair_color=db.Column(db.String(120), unique=True, nullable=False)
    favorites= db.relationship("Favorites")

    def __init__(self):
      self.id= id
      self.name= name
      self.birth_date = birth_date
      self.description= description
      self.planet_id =  planet_id
      self.eye_color= eye_color
      self.hair_color=hair_color

      def serialize(self):
        return{
            "id": self.id,
            "name":self.name,
            "birth_day":self.birth_date,
            "description":self.description,
            "planet_id":self.planet_id,
            "eye_color":self.eye_color,
            "hair_color":self.hair_color,
        }


class Planet(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(120), unique=True, nullable=False)
    description= db.Column(db.String(120), unique=True, nullable=False)
    population=db.Column(db.Integer)
    terrain= db.Column(db.String(120), unique=True, nullable=False)
    climate= db.Column(db.String(120), unique=True, nullable=False)
    people = db.relationship("People")
    favorites= db.relationship("Favorites")
    

    def __init__(self):

     self.id= id
     self.name= name
     self.description=description
     self.population=population
     self.terrain=terrain
     self.climate=climate
     self.people_id= people_id

    def serialize(self):
        return {
          "id": self.id,
          "name":self.name,
          "descirption":self.description,
          "population":self.population,
          "terrain": self.terrain,
          "climate":self.climate,
          "people_id":self.people_id

        }



class Favorites(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planets_id= db.Column(db.Integer,db.ForeignKey("planet.id"))          #nombre de la table + id
    people_id= db.Column(db.Integer, db.ForeignKey("people.id"))
    user= db.relationship("User", back_populates="favorites") ##union de clases y tabla    #relacion class y unir tablas- inner join                           #relacion entre las class 
    planet= db.relationship("Planet",back_populates="favorites")
    people= db.relationship("People",back_populates="favorites") #insertar en la tabla favoritos las clases 


    def __init__(self):
     self.id = id
     self.planets_id = planets_id
     self.people_id = people_id


    def serialize(self):
      return {
         "id":self.id,
         "people_id":self.people_id,
         "planet_id":self.planets_id,

      }