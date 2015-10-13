from kazoocommission.controllers import *
from unittest import TestCase
from unittest.mock import create_autospec, Mock


class TestControllers(TestCase):
    def setUp(self):
        self.mac_address = 'testmac'
        self.account = 'testaccount'

        self.account_data = [{'id': 'test'}]
        self.account_service = create_autospec(KazooAccountService)
        self.account_service.get_account_by_name.side_effect = \
            self.account_data

        self.device_data = [{'mac_address', 'te:st:mac'}]
        self.device_service = create_autospec(KazooDeviceService)
        self.device_service.get_device_by_mac_address.side_effect = \
            self.device_data

        self.callback_fn = Mock()
        self.authenticate = authenticate(self.callback_fn,
                                         self.account_service,
                                         self.device_service)

    def test_authenticate_sets_account_and_device_data(self):

        self.authenticate(self.account_service, self.device_service,
                          mac_address=self.mac_address, account=self.account)()

        self.callback_fn.assert_called_with(
            self.account_service, self.device_service,
            mac_address=self.mac_address, account_data=self.account_data[0],
            device_data=self.device_data[0], account=self.account)
