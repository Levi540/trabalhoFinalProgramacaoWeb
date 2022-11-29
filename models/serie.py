from sql_alchemy import database
from sqlalchemy.sql.expression import func

class SerieModel (database.Model):
    
    __tablename__ = 'series'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(50))
    season = database.Column(database.String(20))
    rating = database.Column(database.String(5))
    # movies = database.Column(database.Integer)

    def __init__(self, id, name, season, rating):
        self.id = id
        self.name = name
        self.season = season
        self.rating = rating

    def json(self):
        return {'id' : self.id,
        'name' : self.name,
        'season' : self.season,
        'rating' : self.rating}

    @classmethod  
    def find_serie_by_id(cls, id):
        
        serie = cls.query.filter_by(id = id).first() # select * from movie where id = 1
        if serie:
            return serie
        return None

    def save_serie(self): 
        database.session.add(self)
        database.session.commit()

    def update_serie(self, name, season, rating): 
        self.name = name
        self.season = season
        self.rating = rating

    def delete_serie(self): 
        database.session.delete(self)
        database.session.commit()
    

    @classmethod
    def find_last_serie(cls):
        serie_id = database.session.query(func.max(cls.id)).one()[0]
        
        if serie_id:
            return serie_id + 1
        return 1