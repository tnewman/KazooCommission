from kazoocommission import config
import pykazoo.client


class KazooDeviceService:
    """ Provides access to Kazoo platform Devices.

        :param client: The client to use to interact with the Kazoo Crossbar
                       API. The default is pykazoo.
        :type client: pykazoo.client.PyKazooClient
    """

    def __init__(self, client=None):
        self.client = client

        if self.client is None:
            self.client = pykazoo.client.PyKazooClient(config.PYKAZOO_API_URL)

    def get_device_by_mac_address(self, account_id, mac_address):
        """ Gets a specific device for an account by MAC address.

        :param account_id: Account ID to retrieve a device from.
        :param mac_address: Device MAC address in lowercase, colon delimited
               format (57:fb:69:4a:f5:c5)
        :return: Device Configuration
        :type mac_address: str
        :rtype: dict
        """

        self.client.authentication.api_auth(config.PYKAZOO_API_KEY)
        devices = self.client.devices.get_devices(
            account_id, {'filter_mac_address': mac_address})['data']

        if len(devices) == 0:
            return None
        else:
            device = self.client.devices.get_device(account_id,
                                                    devices[0]['id'])

            return device['data']
