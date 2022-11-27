from flask_restful import Resource, reqparse
from models.serie import SerieModel
from flask_jwt_extended import jwt_required

class Series(Resource):
    def get(self):
        return {'series' : [movie.json() for movie in SerieModel.query.all()]}


class Serie(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('name', type=str, required=True, help="name is required")
    minha_requisicao.add_argument('rating')

    @jwt_required()
    def get(self, id):
        serie = SerieModel.find_serie_by_id(id)
        if serie:
            return serie.json()
        return {'message':'Serie not found'}, 200 # or 204

    @jwt_required()
    def post(self, id):
        serie_id = SerieModel.find_last_serie()
        dados = Serie.minha_requisicao.parse_args()
        new_serie = SerieModel(serie_id, **dados)
        
        try:
            new_serie.save_serie()
        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_serie.json(), 201

    def put(self, id):
        dados = Serie.minha_requisicao.parse_args()
        serie = SerieModel.find_movie_by_id(id)
        if serie:
            serie.update_serie(**dados)
            serie.save_serie()
            return serie.json(), 200

        serie_id = SerieModel.find_last_serie()
        new_serie = SerieModel(serie_id, **dados)
        new_serie.save_serie()
        return new_serie.json(), 201

    def delete(self, id):
        serie = SerieModel.find_serie_by_id(id)
        if serie:
            serie.delete_serie()
            return {'message' : 'Serie deleted.'}
        return {'message' : 'Serie not founded'}, 204