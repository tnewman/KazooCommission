import pykazoo.client
import kazoocommission.services
from unittest import TestCase
from unittest.mock import create_autospec


def create_pykazoo_mock():
    rest_request = create_autospec(pykazoo.restrequest.RestRequest)

    rest_request.auth_token = 'ajfoijfajf'
    rest_request.account_id = 'j434j09jj0j90fjf9a323232'

    client = pykazoo.client.PyKazooClient('', rest_request=rest_request)

    return client


class TestKazooAccountService(TestCase):
    def setUp(self):
        self.client = create_pykazoo_mock()
        self.service = kazoocommission.services.KazooAccountService(
            self.client)

    def test_pykazoo_client_used_by_default(self):
        client = kazoocommission.services.KazooAccountService().client
        assert type(client) is pykazoo.client.PyKazooClient

    def test_get_account_by_name_returns_auth_token_account(self):
        api_auth = {'auth_token': 'token', 'data':
                    {'account_id': '55555514def94f7ce08cf3e1a999999'}}
        api_auth_account = \
            {'data': {'account_id': '55555514def94f7ce08cf3e1a999999',
                      'name': 'test'}}

        self.client._rest_request.put.side_effect = [api_auth]
        self.client._rest_request.get.side_effect = [api_auth_account]

        account = self.service.get_account_by_name('test')

        assert account == api_auth_account['data']

    def test_get_account_by_name_returns_child_account(self):
        api_auth = \
            {'data': {'account_id': '55555514def94f7ce08cf3e1a999999'},
             'auth_token': 'wetawoij'}
        api_account = {'data': {'name': 'incorrect'}}
        accounts = {'data': [{'id': '55555514def94fasdfcf3e1a999999'}]}
        child_account = \
            {'data': {'id': '55555514def94fasdfcf3e1a999999'}}

        self.client._rest_request.put.side_effect = [api_auth]
        self.client._rest_request.get.side_effect = [api_account, accounts,
                                                     child_account]

        account = self.service.get_account_by_name('test')

        assert account == child_account['data']

    def test_account_account_by_name_no_child_account_returns_none(self):
        api_auth = \
            {'data': {'account_id': '55555514def94f7ce08cf3e1a999999'},
             'auth_token': 'wetawoij'}
        api_account = {'data': {'name': 'incorrect'}}
        accounts = {'data': []}
        child_account = None

        self.client._rest_request.put.side_effect = [api_auth]
        self.client._rest_request.get.side_effect = [api_account, accounts,
                                                     child_account]

        account = self.service.get_account_by_name('test')

        assert account == child_account

    def test_get_account_by_name_authenticated_when_no_auth_cache(self):
        self.client._rest_request.auth_token = None

        assert not self.client.authentication.authenticated

        api_auth = \
            {'data': {'account_id': '55555514def94f7ce08cf3e1a999999'},
             'auth_token': 'wetawoij'}
        account_data = {'data': {'account_id':
                                 '55555514def94f7ce08cf3e1a999999',
                                 'name': 'testname'}}

        self.client._rest_request.put.side_effect = [api_auth]
        self.client._rest_request.get.side_effect = [account_data]

        self.service.get_account_by_name('testname')

        assert self.client.authentication.authenticated

    def test_get_account_by_name_no_account_id_cached(self):
        self.client._rest_request.account_id = None

        assert not self.client.authentication.account_id

        api_auth = \
            {'data': {'account_id': '55555514def94f7ce08cf3e1a999999'},
             'auth_token': 'wetawoij'}
        account_data = {'data': {'account_id':
                                 '55555514def94f7ce08cf3e1a999999',
                                 'name': 'testname'}}

        self.client._rest_request.put.side_effect = [api_auth]
        self.client._rest_request.get.side_effect = [account_data]
        self.service.get_account_by_name('testname')

        assert self.client.authentication.account_id == \
            '55555514def94f7ce08cf3e1a999999'


class TestKazooDeviceService(TestCase):
    def setUp(self):
        self.client = create_pykazoo_mock()
        self.service = kazoocommission.services.KazooDeviceService(
            self.client)

    def test_pykazoo_client_used_by_default(self):
        client = kazoocommission.services.KazooAccountService().client
        assert type(client) is pykazoo.client.PyKazooClient

    def test_get_device_by_mac_address_returns_device(self):
        get_devices_return = {'data': [{'id': 'asdf', 'name': 'Test Phone'}]}
        get_device_return = \
            {'data': {'name': 'Test Phone', 'caller_id':
                      {'internal': {'name': 'cidname',
                                    'number': 'cidnumber'}}}}

        self.client._rest_request.get.side_effect = [get_devices_return,
                                                     get_device_return]

        device = self.service.get_device_by_mac_address('asdf',
                                                        'fd:df:ef:cd:re')

        assert device == get_device_return['data']

    def test_get_device_by_mac_address_returns_empty_for_invalid_mac(self):
        self.client._rest_request.get.return_value = {'data': []}

        device = self.service.get_device_by_mac_address('asdf', 'badmac')

        assert device is None

    def test_get_device_by_mac_address_authenticated_when_no_auth_cache(self):
        self.client._rest_request.auth_token = None

        assert not self.client.authentication.authenticated

        api_auth = \
            {'data': {'account_id': '55555514def94f7ce08cf3e1a999999'},
             'auth_token': 'wetawoij'}

        devices_data = {'data': [{'id': 'asdf', 'name': 'Test Phone'}]}
        device_data = \
            {'data': {'name': 'Test Phone', 'caller_id':
                              {'internal': {'name': 'cidname',
                                            'number': 'cidnumber'}}}}

        self.client._rest_request.put.side_effect = [api_auth]
        self.client._rest_request.get.side_effect = [devices_data, device_data]

        self.service.get_device_by_mac_address(
            '55555514def94f7ce08cf3e1a999999', 'testmac')

        assert self.client.authentication.authenticated

    def test_get_device_by_mac_address_sets_line_display_text(self):
        get_devices_return = {'data': [{'id': 'asdf', 'name': 'Test Phone'}]}
        get_device_return = \
            {'data': {'name': 'Test Phone', 'caller_id':
                      {'internal': {'name': 'cidname',
                                    'number': 'cidnumber'}}}}

        self.client._rest_request.get.side_effect = [get_devices_return,
                                                     get_device_return]

        device = self.service.get_device_by_mac_address('asdf',
                                                        'fd:df:ef:cd:re')

        assert device['line_display_text'] == 'cidnumber-cidname'

    def test_get_device_by_mac_address_default_line_display_text(self):
        get_devices_return = {'data': [{'id': 'asdf', 'name': 'Test Phone'}]}
        get_device_return = {'data': {'name': 'Test Phone'}}

        self.client._rest_request.get.side_effect = [get_devices_return,
                                                     get_device_return]

        device = self.service.get_device_by_mac_address('asdf',
                                                        'fd:df:ef:cd:re')

        assert device['line_display_text'] == 'Test Phone'
