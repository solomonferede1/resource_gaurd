#!/usr/bin/python3
"""Product API Routes"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.product import Product


@app_views.route('/products/', methods=['GET'], strict_slashes=False)
def get_products():
    """Retrieve all products"""
    all_products = storage.all(Product).values()
    return jsonify([product.to_dict() for product in all_products])


@app_views.route('/products/<int:product_id>', methods=['GET'], strict_slashes=False)
def get_product(product_id):
    """Retrieve a Product object by its ID"""
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    return jsonify(product.to_dict())


@app_views.route('/products/<int:product_id>', methods=['DELETE'], strict_slashes=False)
def delete_product(product_id):
    """Delete a Product object by its ID"""
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    storage.delete(product)
    storage.save()
    return jsonify({}), 200


@app_views.route('/products', methods=['POST'], strict_slashes=False)
def create_product():
    """Create a new Product"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    if 'product_name' not in data:
        abort(400, description="Missing product_name")
    if 'product_type' not in data:
        abort(400, description="Missing product_type")
    if 'quantity' not in data:
        abort(400, description="Missing quantity")
    if 'price' not in data:
        abort(400, description="Missing price")
    if 'category_id' not in data:
        abort(400, description="Missing category_id")

    data['category_id'] = int(data['category_id'])  # Convert category_id to int
    product = Product(**data)
    storage.new(product)
    storage.save()
    return jsonify(product.to_dict()), 201


@app_views.route('/products/<int:product_id>', methods=['PUT'], strict_slashes=False)
def update_product(product_id):
    """Update an existing Product object"""
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    
    #  Convert category_id to int if present
    if 'category_id' in data:
        data['category_id'] = int(data['category_id'])

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'deleted_at']:
            setattr(product, key, value)
    storage.save()
    return jsonify(product.to_dict()), 200
