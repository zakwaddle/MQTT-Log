from flask import Blueprint, request, jsonify
from database import (get_devices, add_device, update_display_name, delete_device, get_device_config, get_device,
                      update_device_config, delete_device_config, add_device_config, get_device_sensors,
                      get_wifi_network, get_mqtt_broker, get_ftp_server)
from flask_sse import sse

device_blueprint = Blueprint('device_blueprint', __name__)


def create_default_config():
    wifi = get_wifi_network(1)
    mqtt_broker = get_mqtt_broker(1)
    ftp = get_ftp_server(1)
    default_config = {}
    if wifi:
        default_config.update({"wifi_network_id": 1})
    if mqtt_broker:
        default_config.update({"mqtt_broker_id": 1})
    if ftp:
        default_config.update({"ftp_server_id": 1})
    return default_config


@device_blueprint.route('/')
def get_all_devices():
    data = get_devices()
    return jsonify(data)


@device_blueprint.route('/add', methods=['POST'])
def add_new_device():
    device_data = request.json
    new_device = add_device(device_data)
    add_device_config(new_device['id'], **create_default_config())
    device = get_device(new_device['id'])
    sse.publish({"message": "New device added", "type": "device", "device": device})
    return jsonify(success=True, device=device)


@device_blueprint.route('/<string:device_id>')
def get_single_device(device_id):
    data = get_device(device_id)
    data = data.to_dict() if data is not None else {}
    return jsonify(data)


@device_blueprint.route('/<string:device_id>/display_name', methods=['POST'])
def update_device_display_name(device_id):
    new_name = request.json
    name = new_name.get('display_name')
    if name is not None:
        data = update_display_name(device_id, name)
        return jsonify(success=True, device=data.to_dict())
    return jsonify(success=False, device=None)


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
