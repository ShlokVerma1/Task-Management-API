from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Category
from app.schemas import CategorySchema

category_bp = Blueprint('categories', __name__)
category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)

@category_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()
    errors = category_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user_id = get_jwt_identity()
    category = Category(name=data['name'], user_id=user_id)
    db.session.add(category)
    db.session.commit()
    return category_schema.dump(category), 201

@category_bp.route('/categories', methods=['GET'])
@jwt_required()
def list_categories():
    user_id = get_jwt_identity()
    categories = Category.query.filter_by(user_id=user_id).all()
    return category_list_schema.dump(categories), 200
