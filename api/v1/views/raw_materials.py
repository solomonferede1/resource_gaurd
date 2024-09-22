#!/usr/bin/python3
"""Raw Material API Routes"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.raw_material import RawMaterial


@app_views.route('/raw_materials/', methods=['GET'], strict_slashes=False)
def get_raw_materials():
    """Retrieve all raw materials"""
    all_raw_materials = storage.all(RawMaterial).values()
    return jsonify([raw_material.to_dict() for raw_material in all_raw_materials])


@app_views.route('/raw_materials/<int:raw_material_id>', methods=['GET'], strict_slashes=False)
def get_raw_material(raw_material_id):
    """Retrieve a Raw Material object by its ID"""
    raw_material = storage.get(RawMaterial, raw_material_id)
    if not raw_material:
        abort(404)
    return jsonify(raw_material.to_dict())


@app_views.route('/raw_materials/<int:raw_material_id>', methods=['DELETE'], strict_slashes=False)
def delete_raw_material(raw_material_id):
    """Delete a Raw Material object by its ID"""
    raw_material = storage.get(RawMaterial, raw_material_id)
    if not raw_material:
        abort(404)
    storage.delete(raw_material)
    storage.save()
    return jsonify({}), 200


@app_views.route('/raw_materials', methods=['POST'], strict_slashes=False)
def create_raw_material():
    """Create a new Raw Material"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    if 'material_name' not in data:
        abort(400, description="Missing material_name")
    if 'quantity' not in data:
        abort(400, description="Missing quantity")
    if 'unit_price' not in data:
        abort(400, description="Missing unit_price")
    if 'supplier_id' not in data:
        abort(400, description="Missing supplier_id")

    data['supplier_id'] = int(data['supplier_id'])  # Convert supplier_id to int
    raw_material = RawMaterial(**data)
    storage.new(raw_material)
    storage.save()
    return jsonify(raw_material.to_dict()), 201


@app_views.route('/raw_materials/<int:raw_material_id>', methods=['PUT'], strict_slashes=False)
def update_raw_material(raw_material_id):
    """Update an existing Raw Material object"""
    raw_material = storage.get(RawMaterial, raw_material_id)
    if not raw_material:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    
    # Convert supplier_id to int if present
    if 'supplier_id' in data:
        data['supplier_id'] = int(data['supplier_id'])

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'deleted_at']:
            setattr(raw_material, key, value)
    storage.save()
    return jsonify(raw_material.to_dict()), 200
