from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

ksiazki = []

class Ksiazki(Resource):
    def get(self,name):
        print(ksiazki)

        for book in ksiazki:
            if book['name'] == name:
                return book

        return {'name':None},404

    def post(self, name):
        book = {'name':name}
        ksiazki.append(book)
        print(ksiazki)
        return book

    def delete(self,name):

        for ind,book in enumerate(ksiazki):
            if book['name'] == name:
                delted_pup = ksiazki.pop(ind)
                return {'note':'Usunieto'}

class AllNames(Resource):

    def get(self):
        return {'ksiazki': ksiazki}

api.add_resource(Ksiazki, '/ksiazki/<string:name>')
api.add_resource(AllNames,'/ksiazki')

if __name__ == '__main__':
    app.run(debug=True)
