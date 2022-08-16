import json
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required
from models.item import ClientModel


class Item(Resource):
    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('name', type=str, required=True,
                        help='Este campo é obrigátorio.')
    parser.add_argument('email', type=str, required=True,
                        help='Este campo é obrigátorio.')
    parser.add_argument('password', type=str, required=True,
                        help='Este campo é obrigátorio.')
    parser.add_argument('passwordConfirmation', type=str, required=True,
                        help='Este campo é obrigátorio.')
    parser.add_argument('phone', type=str, required=False,
                        help='Este campo é opcional.')

    # @jwt_required()  
    def get(self, name):
        item = ClientModel.find_by_client(name)
        if item:
            return item.json(), 200
        return 404

    # @jwt_required()
    def post(self):
        
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']
        passwordConfirmation = data['passwordConfirmation']
        phone = data['phone']

        if ClientModel.find_by_client(email):
            return {'message': f"E-mail: '{email}' indisponível."}, 400
        
        data = Item.parser.parse_args()
        item = ClientModel(name, email, password, passwordConfirmation, phone)
        try:
            item.save_to_db()
        except:
            return {"message": "Ocorreu algum erro ao salvar este item."}, 500
        return item.json(), 201

    # @jwt_required()
    def delete(self, name):

        item = ClientModel.find_by_client(name)
        if item:
            item.delete_from_db()
            return 200
        
        return 204

    # @jwt_required()
    def put(self, name):
        # Create or Update
        data = Item.parser.parse_args()
        item = ClientModel.find_by_client(name)

        if item is None:
            return {'message': 'Item não encontrado, alteração não concluida.'}, 404
        else:
            item.price = data['price']

        item.save_to_db()

        return 200


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {
            'clients': [item.json() for item in ClientModel.query.all()]}