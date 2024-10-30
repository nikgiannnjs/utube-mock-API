from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name" , type=str , help="Name of video is required" , required=True)
video_put_args.add_argument("views" , type=int , help="Views of video is required" , required=True)
video_put_args.add_argument("likes" , type=int , help="Likes of video is required" , required=True)

videos = {}

def abort_if_not_valid_id(video_id):
    if video_id not in videos:
        abort(404 , message="Video id is not valid.")

def abort_if_video_already_exists(video_id):
    if video_id in videos:
        abort(404 , message="Video already exist.")

class Video(Resource):
    def get(self, video_id):
        abort_if_not_valid_id(video_id)
        return videos[video_id]
    
    def post(self, video_id):
        abort_if_video_already_exists
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201
    
    def delete(self, video_id):
        abort_if_not_valid_id
        del videos[video_id]
        return "Video deleted" , 204
    
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT" , 5000))
    app.run(debug=True, port=port)

    