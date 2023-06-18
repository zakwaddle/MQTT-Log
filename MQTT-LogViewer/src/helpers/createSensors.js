

export function createMotionSensor(deviceConfigId, name, pin, retriggerTimeMS=120000){
    return {
        "sensor_type": "motion",
        "device_config_id": deviceConfigId,
        "name": name,
        "sensor_config": {
            "pin": pin,
            "retrigger_delay_ms": retriggerTimeMS
        }
    }
}
export function createDimmableLED(deviceConfigId, name, pin, freq=300, fadeTimeMS=4, brightnessScale=255){
    return {
        "sensor_type": "led",
        "device_config_id": deviceConfigId,
        "name": name,
        "sensor_config": {
            "pin": pin,
            "freq": freq,
            "fade_time_ms": fadeTimeMS,
            "brightness_scale": brightnessScale
        }
    }
}
export function createWeatherSensor(deviceConfigId, name, pin, measurementIntervalMS=10000){
    return {
        "sensor_type": "weather",
        "device_config_id": deviceConfigId,
        "name": name,
        "sensor_config": {
            "pin": pin,
            "measurement_interval_ms": measurementIntervalMS
        }
    }
}