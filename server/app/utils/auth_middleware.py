from flask import request, jsonify, current_app
import jwt, datetime
from app.controllers.users_controller import get_user
from functools import wraps


def token_required(f):
    """JWT Authentication Middleware"""

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.cookies.get("access_token")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"],
                leeway=10,  # Grace period of 10 seconds
            )

            # Check expiry
            if datetime.datetime.fromtimestamp(
                data["exp"], datetime.timezone.utc
            ) < datetime.datetime.now(datetime.timezone.utc):
                return jsonify({"message": "Token expired"}), 401

            # Fetch the user
            current_user = get_user(data)

            # ✅ Execute the decorated function with the current_user
            return f(current_user, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 401
        except Exception as e:
            print(e)
            return jsonify({"message": "An error occurred!"}), 500

    return decorated
