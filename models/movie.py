from sql_alchemy import database
from sqlalchemy.sql.expression import func

class MovieModel (database.Model):
    
    __tablename__ = 'movies'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(50))
    rating = database.Column(database.String(5))
    duration = database.Column(database.Integer)

    def __init__(self, id, name, rating, duration):
        self.id = id
        self.name = name
        self.rating = rating
        self.duration = duration

    def json(self):
        return {'id' : self.id,
        'name' : self.name,
        'rating' : self.rating,
        'duration' : self.duration}

    @classmethod  
    def find_movie_by_id(cls, id): #metodo de classe, mesmo que chamar Movie.query
        
        movie = cls.query.filter_by(id = id).first() # select * from movie where id = 1
        if movie:
            return movie
        return None

    def save_movie(self): 
        database.session.add(self)
        database.session.commit()

    def update_movie(self, name, rating, duration): 
        self.name = name
        self.rating = rating
        self.duration = duration

    def delete_movie(self): 
        database.session.delete(self)
        database.session.commit()
    

    @classmethod
    def find_last_movie(cls):
        movie_id = database.session.query(func.max(cls.id)).one()[0]
        
        if movie_id:
            return movie_id + 1
        return 1