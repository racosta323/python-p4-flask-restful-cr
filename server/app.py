#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
import ipdb

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

#Flask-RESTful's Api class is constructor for RESTful API
api = Api(app)

class Home(Resource):
    def get(self):

        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }

        response = make_response(response_dict,200)
        return response



class Newsletters(Resource):

    #getting a record using Flask RESTful Resource class
    def get(self):
        
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]

        response = make_response(response_dict_list, 200,)
        return response

#resource subclasses are added to the API instance with add_resource()
#uses defined HTTP verb instance methods to determine routes
#handle tasks normally carried otu by @app.route() decorator
#each HTTP verb gets an instance method inside of a Resource class    

    #creating a record using Flask RESTful Resource class
    def post(self):

        new_record = Newsletter(
            ##retrieve form data from request context
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(response_dict, 201,)

class NewsletterByID(Resource):
    def get(self, id):

        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(response_dict, 200,)
        return response


api.add_resource(Home, '/')
api.add_resource(Newsletters, '/newsletters')
api.add_resource(NewsletterByID, '/newsletters/<int:id>')    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
