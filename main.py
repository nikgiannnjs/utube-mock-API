from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name" , type=str , help="Name of video is required")
video_update_args.add_argument("views" , type=int , help="Views of video is required")
video_update_args.add_argument("likes" , type=int , help="Likes of video is required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        
        result = VideoModel.query.filter_by(id=video_id).first()
        
        if not result:
            abort(404, message="Video id could not be found.")
        
        return result
    
    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_put_args.parse_args()
        
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(404, message="Video id already exist.")
        
        video = VideoModel(id=video_id, name=args['name'] , views=args['views'], likes=args['likes'])
       
        db.session.add(video)
        db.session.commit()
        
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video id could not be found. Cannot update.")
        
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.name = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        db.session.commit()
        
        return result
    
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video does not exist. Cannot delete.")
        
        db.session.delete(result)
        db.session.commit()

        return {"message": "Video deleted successfully"}, 200


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT" , 5000))
    app.run(debug=True, port=port)

    