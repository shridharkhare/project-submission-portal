from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import Client, create_client
import os

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173","http://localhost:3000", "http://127.0.0.1:5500", "http://localhost:5500"]}}, supports_credentials=True)

    load_dotenv()
    
    # Load configuration
    app.config.from_object('app.utils.config.Config')
    # print(app.config)

    # Import and register blueprints
    from app.routes import welcome, authtoken, users, projects, g_classrooms
    
    # Initialize Supabase
    app.supabase = create_client(app.config["SUPABASE_URL"], app.config["SUPABASE_KEY"])

    app.register_blueprint(welcome.bp, url_prefix='/')

    app.register_blueprint(authtoken.bp, url_prefix='/api/v1/authtoken')
    app.register_blueprint(users.bp, url_prefix='/api/v1/users')
    app.register_blueprint(projects.bp, url_prefix='/api/v1/projects')
    app.register_blueprint(g_classrooms.bp, url_prefix='/api/v1/g_classrooms')

    # Register blueprints to be added later
    # app.register_blueprint(classes.bp, url_prefix='/api/v1/classes')
    # app.register_blueprint(teams.bp, url_prefix='/api/v1/teams')
    
    return app
