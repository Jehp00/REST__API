from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self, name=name, views=views, likes=likes):
        return f"Video(name={name}, views={views}, likes={likes}"


videos_put_args = reqparse.RequestParser()
videos_put_args.add_argument("views", type=int, help="Number of views of the video", required=True)
videos_put_args.add_argument("likes", type=int, help="Number of likes on the video", required=True)
videos_put_args.add_argument("name", type=str, help="name of the video", required=True)

videos_update_args = reqparse.RequestParser()
videos_update_args.add_argument("views", type=int, help="Number of views of the video")
videos_update_args.add_argument("likes", type=int, help="Number of likes on the video")
videos_update_args.add_argument("name", type=str, help="name of the video")

resources_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    "likes": fields.Integer
}


class Video(Resource):
    @marshal_with(resources_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video not found")
        return result, 201

    @marshal_with(resources_fields)
    def put(self, video_id):
        args = videos_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(403, message='Videos already exists')
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resources_fields)
    def patch(self, video_id):
        args = videos_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Videos doesnt exists, cannot update')

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        db.session.delete(result)
        db.session.commit()
        return "User deleted", 204



api.add_resource(Video, "/Video/<int:video_id>")

if __name__ == '__main__':
    app.run(debug=True)
