from sql_alchemy import database
from sqlalchemy.sql.expression import func

class EpisodeModel (database.Model):
    
    __tablename__ = 'episodes'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(50))
    rating = database.Column(database.String(5))
    duration = database.Column(database.Integer)
    serieId = database.Column(database.Integer)

    def __init__(self, id, name, rating, duration, serieId):
        self.id = id
        self.name = name
        self.rating = rating
        self.duration = duration
        self.serieId = serieId

    def json(self):
        return {'id' : self.id,
        'name' : self.name,
        'rating' : self.rating,
        'duration' : self.duration,
        'serieId' : self.serieId}

    @classmethod  
    def find_episode_by_id(cls, id): #metodo de classe, mesmo que chamar Movie.query
        
        episode = cls.query.filter_by(id = id).first() # select * from movie where id = 1
        if episode:
            return episode
        return None

    def save_episode(self): 
        database.session.add(self)
        database.session.commit()

    def update_episode(self, name, rating, duration, serieId): 
        self.name = name
        self.rating = rating
        self.duration = duration
        self.serieId = serieId

    def delete_episode(self): 
        database.session.delete(self)
        database.session.commit()
    

    @classmethod
    def find_last_episode(cls):
        episode_id = database.session.query(func.max(cls.id)).one()[0]
        if episode_id:
            return episode_id + 1
        return 1