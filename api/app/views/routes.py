from flask import Blueprint, jsonify, request
from app.models import db

api = Blueprint('api', __name__)

### HEALTH ENDPOINT #########################
@api.route('/health')
def health():
    return jsonify({
            "healthy":True
        }), 200
