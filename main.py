from flask import Flask
from flask_restful import Api, Resource
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"data": "Hello World."}

api.add_resource(HelloWorld, "/")

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT" , 5000))
    app.run(debug=True, port=port)