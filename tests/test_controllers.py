import kazoocommission
from kazoocommission.controllers import *
from unittest import TestCase
from unittest.mock import create_autospec, Mock
from requests.exceptions import InvalidSchema
from werkzeug.datastructures import EnvironHeaders
from werkzeug.exceptions import Forbidden, NotFound


class TestControllers(TestCase):
    def setUp(self):
        config.SSL_CLIENT_SUBJECT_VALIDATION = False

        self.mac_address = 'testmac'
        self.account = 'testaccount'

        self.account_data = [{'id': 'test'}]
        self.account_service = create_autospec(KazooAccountService)
        self.account_service.get_account_by_name.side_effect = \
            self.account_data

        self.device_data = [{'mac_address': 'te:st:mac', 'sip':
                            {'username': 'user', 'password': 'pass'}}]
        self.device_service = create_autospec(KazooDeviceService)
        self.device_service.get_device_by_mac_address.side_effect = \
            self.device_data

        self.callback_fn = Mock()
        self.authenticate = authenticate(self.callback_fn)

    def test_authenticate_sets_account_and_device_data(self):
        self.authenticate(account_service=self.account_service,
                          device_service=self.device_service,
                          mac_address=self.mac_address,
                          account=self.account)()

        self.callback_fn.assert_called_with(
            mac_address=self.mac_address,
            account_data=self.account_data[0],
            device_data=self.device_data[0],
            account=self.account)

    def test_authenticate_non_existent_account_raises_404(self):
        self.account_service.get_account_by_name.side_effect = [None]

        self.assertRaises(NotFound, self.authenticate,
                          account_service=self.account_service,
                          device_service=self.device_service,
                          mac_address=self.mac_address,
                          account=self.account)

    def test_authenticate_non_existent_device_raises_404(self):
        self.device_service.get_device_by_mac_address.side_effect = [None]

        self.assertRaises(NotFound, self.authenticate,
                          account_service=self.account_service,
                          device_service=self.device_service,
                          mac_address=self.mac_address,
                          account=self.account)

    def test_authenticate_client_certificate(self):
        config.SSL_CLIENT_SUBJECT_VALIDATION = True

        with app.test_request_context('/'):
            request.headers = EnvironHeaders({'X-SSL-Subject':
                                              self.mac_address})

            self.assertRaises(Forbidden, self.authenticate,
                              account_service=self.account_service,
                              device_service=self.device_service,
                              mac_address=self.mac_address,
                              account=self.account)

    def test_authenticate_client_certificate_incorrect_mac(self):
        config.SSL_CLIENT_SUBJECT_VALIDATION = True

        with app.test_request_context('/'):
            request.headers = {'X-SSL-Subject': 'slkjfkldfjsa'}

            self.assertRaises(
                Forbidden, self.authenticate,
                account_service=self.account_service,
                device_service=self.device_service,
                mac_address=self.mac_address,
                account=self.account)

    def test_services_default_implementations(self):
        # This tests ensures 100% code coverage by making sure the statements
        # assigning the default services are covered for metrics.
        config.PYKAZOO_API_URL = 'localhost:98765'

        authenticate_fn = authenticate(self.callback_fn)

        self.assertRaises(InvalidSchema, authenticate_fn,
                          mac_address=self.mac_address, account=self.account)

    def test_get_provisioning_file(self):
        import os.path
        import sys
        sys.path.append(os.path.join(os.path.dirname(kazoocommission.__file__),
                                     'templates'))

        with app.app_context():
            app.jinja_loader.searchpath.append(
                os.path.join(os.path.dirname(kazoocommission.__file__),
                             'templates'))

            response = get_provisioning_file(
                    'cisco', 'spa504g', account_service=self.account_service,
                    device_service=self.device_service, account=self.account,
                    mac_address=self.mac_address)

            assert response.status == '200 OK'
