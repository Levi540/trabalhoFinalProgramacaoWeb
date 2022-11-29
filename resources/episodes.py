from flask_restful import Resource, reqparse
from models.episode import EpisodeModel
from flask_jwt_extended import jwt_required

class Episodes(Resource):
    def get(self):
        return {'episodes' : [movie.json() for movie in EpisodeModel.query.all()]}


class Episode(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('name', type=str, required=True, help="name is required")
    minha_requisicao.add_argument('rating')
    minha_requisicao.add_argument('duration', type=int, required=True, help="duration is required")
    minha_requisicao.add_argument('serieId', type=int, required=True, help="serie id is required")

    @jwt_required()
    def get(self, id):
        episode = EpisodeModel.find_episode_by_id(id)
        if episode:
            return episode.json()
        return {'message':'episode not found'}, 200 # or 204

    @jwt_required()
    def post(self, id):
        episode_id = EpisodeModel.find_last_episode()
        dados = Episode.minha_requisicao.parse_args()
        new_episode = EpisodeModel(episode_id, **dados)
        
        try:
            new_episode.save_episode()
        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_episode.json(), 201

    def put(self, id):
        dados = Episode.minha_requisicao.parse_args()
        episode = EpisodeModel.find_episode_by_id(id)
        if episode:
            episode.update_episode(**dados)
            episode.save_episode()
            return episode.json(), 200

        episode_id = EpisodeModel.find_last_episode()
        new_episode = EpisodeModel(episode_id, **dados)
        new_episode.save_episode()
        return new_episode.json(), 201

    def delete(self, id):
        episode = EpisodeModel.find_episode_by_id(id)
        if episode:
            episode.delete_episode()
            return {'message' : 'Episode deleted.'}
        return {'message' : 'Episode not founded'}, 204