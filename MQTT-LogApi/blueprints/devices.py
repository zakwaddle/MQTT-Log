from flask import Blueprint, request, jsonify
from database import (get_devices, add_device, delete_device, get_device_config,
                      update_device_config, delete_device_config, add_device_config, get_device_sensors)

device_blueprint = Blueprint('device_blueprint', __name__)


@device_blueprint.route('/')
def get_all_devices():
    data = get_devices()
    return jsonify(data)


@device_blueprint.route('/add', methods=['POST'])
def add_new_device():
    device_data = request.json
    new_device = add_device(device_data)
    return jsonify(success=True, device=new_device)


@device_blueprint.route('/<string:device_id>', methods=['DELETE'])
def remove_device(device_id):
    delete_device(device_id)
    return jsonify(success=True)


@device_blueprint.route('/<string:device_id>/config')
def get_config(device_id):
    config = get_device_config(device_id)
    return jsonify(config)


@device_blueprint.route('/<string:device_id>/config', methods=['POST'])
def add_config(device_id):
    new_config = request.json
    config = add_device_config(device_id, new_config)
    return jsonify(success=True, config=config)


@device_blueprint.route('/<string:device_id>/config', methods=['PUT'])
def update_config(device_id):
    new_config = request.json
    update_device_config(device_id, new_config)
    return jsonify(success=True, config=new_config)


@device_blueprint.route('/<string:device_id>/config', methods=['DELETE'])
def delete_config(device_id):
    delete_device_config(device_id)
    return jsonify(success=True)


@device_blueprint.route('/<string:device_id>/sensors')
def get_sensors(device_id):
    sensors = get_device_sensors(device_id)
    return jsonify(sensors)
