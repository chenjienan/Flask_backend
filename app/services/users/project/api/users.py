from flask import Blueprint, request, render_template
from flask_restful import Resource, Api

from project import db
from project.api.models import User

from sqlalchemy import exc

users_blueprint = Blueprint("users", __name__, template_folder="./templates")
api = Api(users_blueprint)


@users_blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        db.session.add(User(username=username, email=email))
        db.session.commit()

    users = User.query.all()
    # it's like a view bag
    return render_template("index.html", users=users)


class Users(Resource):
    def get(self, user_id):

        response = {"status": "fail", "message": "User does not exist"}
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return response, 404

            response = {
                "status": "success",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "active": user.active,
                },
            }
            return response, 200

        except ValueError:
            return response, 404

        response = {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "active": user.active,
            },
        }
        return response, 200


class UsersList(Resource):
    def get(self):
        """Get all users"""
        response = {
            "status": "success",
            "data": {"users": [user.to_json() for user in User.query.all()]},
        }
        return response, 200

    def post(self):
        # where is request? It's from Flask request
        post_data = request.get_json()

        response = {"status": "fail", "message": "Invalid payload."}

        # error handling: if data is None
        if not post_data:
            return response, 400

        username = post_data.get("username")
        email = post_data.get("email")

        # error handling: if email exsits
        try:
            # where is this query come from?
            user = User.query.filter_by(email=email).first()
            if not user:
                db.session.add(User(username=username, email=email))
                db.session.commit()
                response["status"] = "success"
                response["message"] = f"{email} was added!"
                return response, 201
            else:
                response["message"] = "Email already exists."
                return response, 400

        # what is exc? It's SQL exception
        except exc.IntegrityError:
            db.session.rollback()
            return response, 400


class UsersPing(Resource):
    def get(self):
        return {"status": "success", "message": "pong"}

api.add_resource(UsersPing, "/users/ping")
api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<user_id>")

