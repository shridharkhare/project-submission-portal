from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import Client, create_client
import os


def create_app():
    app = Flask(__name__)

    load_dotenv()



    cors_origins = os.getenv("CORS_ORIGINS", "")

    origins_list = [
        origin.strip() for origin in cors_origins.split(",") if origin.strip()
    ]

    CORS(app, resources={r"/*": {"origins": origins_list}}, supports_credentials=True)

    # Load configuration
    app.config.from_object("app.utils.config.Config")

    # Load environment variables
    app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
    app.config['IS_PROD'] = app.config['ENV'] == 'production'

    # Import and register blueprints
    from app.routes import welcome, authtoken, users, projects, g_classrooms, students, subjects

    # Initialize Supabase
    app.supabase = create_client(app.config["SUPABASE_URL"], app.config["SUPABASE_KEY"])

    app.register_blueprint(welcome.bp, url_prefix="/")

    app.register_blueprint(authtoken.bp, url_prefix="/api/v1/authtoken")
    app.register_blueprint(users.bp, url_prefix="/api/v1/users")
    app.register_blueprint(g_classrooms.bp, url_prefix="/api/v1/g_classrooms")

    app.register_blueprint(subjects.bp, url_prefix="/api/v1/subjects")

    app.register_blueprint(students.bp, url_prefix="/api/v1/students")
    app.register_blueprint(projects.bp, url_prefix="/api/v1/projects")

    # Register blueprints to be added later
    # app.register_blueprint(classes.bp, url_prefix='/api/v1/classes')
    # app.register_blueprint(teams.bp, url_prefix='/api/v1/teams')

    return app
