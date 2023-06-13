import unittest
import requests
import tests.test_data as td

host = 'http://localhost:5000/api/home'


# class FlaskLogTestCase(unittest.TestCase):
#     def setUp(self):
#         print("Add Device")
#         response = requests.post(url=f'{host}/devices/add', json=td.device_data1)
#         data = response.json()
#         self.assertEqual(response.status_code, 200, "Failed to add device")
#         self.assertEqual(data.get('success'), True, "Failed to add device")
#         self.device_id = td.device_data1.get('id')
#
#     def tearDown(self):
#         print('Delete Device')
#         response = requests.delete(url=f'{host}/devices/{self.device_id}')
#         data = response.json()
#         self.assertEqual(response.status_code, 200, "Failed to delete device")
#         self.assertEqual(data.get('success'), True, "Failed to delete device")
#
#     # Log tests
#     def test_add_and_delete_logs(self):
#         print('Add logs')
#         log1 = td.test_log1
#         log2 = td.test_log2
#         log1.update({"device_id": self.device_id})
#         log2.update({"device_id": self.device_id})
#         response = requests.post(url=f'{host}/logs/add', json=log1)
#         self.assertEqual(response.status_code, 200)
#         response = requests.post(url=f'{host}/logs/add', json=log2)
#         self.assertEqual(response.status_code, 200)
#
#         print('Delete logs')
#         response = requests.get(url=f'{host}/logs/')
#         logs = response.json()
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(logs), 2)
#         for i in logs:
#             response = requests.delete(url=f'{host}/logs/entries/{i["id"]}')
#             self.assertEqual(response.status_code, 200, "Failed to delete Log")


class DeviceEndpointsTestCase(unittest.TestCase):
    def setUp(self):
        print("Setup for tests")
        self.device_id = None

    def tearDown(self):
        print("Tear down for tests")
        if self.device_id is not None:
            print('Delete Device')
            response = requests.delete(url=f'{host}/devices/{self.device_id}')
            data = response.json()
            self.assertEqual(response.status_code, 200, "Failed to delete device")
            self.assertEqual(data.get('success'), True, "Failed to delete device")

    def test_add_device(self):
        print('Add Device')
        response = requests.post(url=f'{host}/devices/add', json=td.device_data1)
        data = response.json()
        self.assertEqual(response.status_code, 200, "Failed to add device")
        self.assertEqual(data.get('success'), True, "Failed to add device")
        self.assertIsNotNone(data.get('device'), "No device data returned")
        self.device_id = data.get('device').get('id')

    def test_get_all_devices(self):
        print('Get all devices')
        response = requests.get(url=f'{host}/devices')
        data = response.json()
        self.assertEqual(response.status_code, 200, "Failed to fetch devices")
        self.assertIsInstance(data, list, "Data returned is not a list")

    def test_get_device_sensors(self):
        print('Get device sensors')
        response = requests.get(url=f'{host}/devices/{self.device_id}/sensors')
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, 200, "Failed to fetch device sensors")
        self.assertIsInstance(data, list, "Data returned is not a list")

    def test_delete_device(self):
        print('Delete Device')
        response = requests.delete(url=f'{host}/devices/{self.device_id}')
        data = response.json()
        self.assertEqual(response.status_code, 200, "Failed to delete device")
        self.assertEqual(data.get('success'), True, "Failed to delete device")


if __name__ == '__main__':
    unittest.main()
