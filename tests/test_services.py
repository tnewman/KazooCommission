import pykazoo.client
import kazoocommission.services
from unittest import TestCase
from unittest.mock import create_autospec


def create_pykazoo_mock():
    client = pykazoo.client.PyKazooClient('')
    client.authentication = create_autospec(client.authentication)
    client.devices = create_autospec(client.devices)

    return client


class TestKazooDeviceService(TestCase):
    def setUp(self):
        self.client = create_pykazoo_mock()
        self.account_id = 'asdf3a3affa'
        self.device_id = 'test_id'
        self.mac = '57:fb:69:4a:f5:c5'
        self.auth_token = 'asdfjkl;'
        self.client.authentication.api_auth.return_value = self.auth_token

        self.services = kazoocommission.services.KazooDeviceService(
            self.client)

    def test_pykazoo_client_used_by_default(self):
        client = kazoocommission.services.KazooDeviceService()

        assert type(client.client) is pykazoo.client.PyKazooClient

    def test_get_device_by_mac_address_returns_device(self):
        self.client.devices.get_devices.return_value = \
            {'data': [{'id': self.device_id}]}

        self.client.devices.get_device.return_value = \
            {'device': 'data'}

        result = self.services.get_device_by_mac_address(
            self.account_id, self.mac)

        self.client.devices.get_devices.assert_called_with(
            self.account_id, {'filter_mac_address': self.mac})

        self.client.devices.get_device.assert_called_with(
            self.account_id, self.device_id)

        assert result == {'device': 'data'}

    def test_get_device_by_mac_address_returns_empty_for_invalid_mac(self):
        invalid_mac = 'notamac'

        self.client.devices.get_devices.return_value = {'data': []}

        result = self.services.get_device_by_mac_address(
            self.account_id, invalid_mac)

        self.client.devices.get_devices.assert_called_with(
            self.account_id, {'filter_mac_address': invalid_mac})

        assert result is None
