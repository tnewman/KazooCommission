from kazoocommission import config
import pykazoo.client


class BaseKazooService:
    def __init__(self, client=None):
        self.client = client

        if self.client is None:
            self.client = pykazoo.client.PyKazooClient(config.PYKAZOO_API_URL)


class KazooAccountService(BaseKazooService):
    """ Provides access to Kazoo platform Accounts.

        :param client: The client to use to interact with the Kazoo Crossbar
                       API. The default is pykazoo.
        :type client: pykazoo.client.PyKazooClient
    """

    def __init__(self, client=None):
        BaseKazooService.__init__(self, client)

    def get_account_by_name(self, account_name):
        """ Gets a specific account by name, searching both the account
            associated with the API key in config.py and its descendants.

        :param account_name: Account name to retrieve account for.
        :return: Account
        :type account_name: str
        :rtype: dict
        """

        if self.client.authentication.authenticated and \
                self.client.authentication.account_id:
            account_id = self.client.authentication.account_id
        else:
            account_id = self.client.authentication.api_auth(
                config.PYKAZOO_API_KEY)['data']['account_id']

        account = self.client.accounts.get_account(account_id)

        if account['data']['name'] == account_name:
            return account

        accounts = self.client.accounts.get_account_descendants(
            account_id, {'filter_name': account_name})

        if len(accounts['data']) == 0:
            return None
        else:
            account = self.client.accounts.get_account(
                account_id, accounts['data'][0]['id'])

            return account


class KazooDeviceService(BaseKazooService):
    """ Provides access to Kazoo platform Devices.

        :param client: The client to use to interact with the Kazoo Crossbar
                       API. The default is pykazoo.
        :type client: pykazoo.client.PyKazooClient
    """

    def __init__(self, client=None):
        BaseKazooService.__init__(self, client)

    def get_device_by_mac_address(self, account_id, mac_address):
        """ Gets a specific device for an account by MAC address.

        :param account_id: Account ID to retrieve a device from.
        :param mac_address: Device MAC address in lowercase, colon delimited
               format (57:fb:69:4a:f5:c5)
        :return: Device Configuration
        :type mac_address: str
        :rtype: dict
        """

        if not self.client.authentication.authenticated:
            self.client.authentication.api_auth(config.PYKAZOO_API_KEY)

        devices = self.client.devices.get_devices(
            account_id, {'filter_mac_address': mac_address})['data']

        if len(devices) == 0:
            return None
        else:
            device = self.client.devices.get_device(account_id,
                                                    devices[0]['id'])

            return device['data']
