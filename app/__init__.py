from flask import Flask
from flask_marshmallow import Marshmallow
# from flask_cors import CORS
from .config import Config

ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    ma.init_app(app)

    with app.app_context():

        #API Blueprints
        from .routes import users_surveyor_bp, auth_surveyor_bp, notifications_bp
        from .routes import attendants_survey_bp, tasks_survey_bp, demandas_bp
        from .routes import customers_bp, vessel_bp, cargo_bp, survey_pdf_bp
        from .routes import cargo_condition_bp, cargo_inspection_bp, lashing_cargo_bp
        from .routes import lashing_material_bp, cargo_storage_bp, lifting_operation_bp
        from .routes import lifting_material_bp, tarefas_bp, checklist_bp
        from .routes import offiline_bp, auth_customer_bp, users_customer_bp
        from .routes import notifications_customer_bp, lifting_inspection_bp, clients_bp
        from .routes import lashing_inspection_bp, statement_of_facts_bp, relation_bp, health_bp 
        from .routes import settings_bp, medicoes_bp, nota_fiscal_bp, pdf_extraction_bp

        app.register_blueprint(users_surveyor_bp)
        app.register_blueprint(auth_surveyor_bp)
        app.register_blueprint(notifications_bp)
        app.register_blueprint(attendants_survey_bp)
        app.register_blueprint(tasks_survey_bp)
        app.register_blueprint(demandas_bp)
        app.register_blueprint(customers_bp)
        app.register_blueprint(vessel_bp)
        app.register_blueprint(cargo_bp)
        app.register_blueprint(cargo_condition_bp)
        app.register_blueprint(cargo_inspection_bp)
        app.register_blueprint(lashing_cargo_bp)
        app.register_blueprint(lashing_material_bp)
        app.register_blueprint(cargo_storage_bp)
        app.register_blueprint(lifting_operation_bp)
        app.register_blueprint(lifting_material_bp)
        app.register_blueprint(tarefas_bp)
        app.register_blueprint(checklist_bp)
        app.register_blueprint(offiline_bp)
        app.register_blueprint(auth_customer_bp)
        app.register_blueprint(users_customer_bp)
        app.register_blueprint(notifications_customer_bp)
        app.register_blueprint(lifting_inspection_bp)
        app.register_blueprint(lashing_inspection_bp)
        app.register_blueprint(statement_of_facts_bp)
        app.register_blueprint(relation_bp)
        app.register_blueprint(clients_bp)
        app.register_blueprint(health_bp)
        app.register_blueprint(survey_pdf_bp)
        app.register_blueprint(settings_bp)
        app.register_blueprint(medicoes_bp)
        app.register_blueprint(nota_fiscal_bp)
        app.register_blueprint(pdf_extraction_bp)


    return app
