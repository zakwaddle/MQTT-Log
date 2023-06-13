import {useState} from 'react';

// const BASE_URL = `http://localhost:5000/api/home`
const BASE_URL = `http://yawntsum.local/api/home`;


const useApi = () => {
    const [loading, setLoading] = useState(false);

    const fetchLogs = async () => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/logs`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const deleteLogEntry = async (id) => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/logs/entries/${id}`, {
            method: 'DELETE',
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const fetchDevices = async () => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/devices`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const addDevice = async (deviceId, platform, displayName) => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/devices/add`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                id: deviceId,
                platform: platform,
                display_name: displayName,
                device_info: {
                    "name": deviceId,
                    "manufacturer": "ZRW",
                    "model": `${platform.toUpperCase()}-Circuit`,
                    "identifiers": deviceId
                }
            })
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const deleteDevice = async (id) => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/devices/${id}`, {
            method: 'DELETE',
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const fetchDeviceConfig = async (deviceId) => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/devices/${deviceId}/config`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const updateDeviceConfig = async (id, config) => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/devices/${id}/config`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(config)
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const fetchDeviceSensors = async (id) => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/devices/${id}/sensors`);
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const addSensor = async (sensorType, sensorName, deviceConfigId, sensorConfig) => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/sensors/add`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                    sensor_type: sensorType,
                    name: sensorName,
                    device_config_id: deviceConfigId,
                    sensor_config: sensorConfig
                }
            )
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const updateSensorConfig = async (id, config) => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/sensors/${id}/config`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(config)
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const deleteSensor = async (id) => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/sensors/${id}`, {
            method: 'DELETE',
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };

    const checkIn = async () => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/logs/check-in`, {
            method: 'POST',
        });
        const data = await response.json();
        setLoading(false);
        return data;
    };
    return {
        fetchLogs,
        deleteLogEntry,
        fetchDevices,
        addDevice,
        deleteDevice,
        fetchDeviceConfig,
        updateDeviceConfig,
        fetchDeviceSensors,
        addSensor,
        updateSensorConfig,
        deleteSensor,
        checkIn,
        loading
    };
};

export default useApi;
