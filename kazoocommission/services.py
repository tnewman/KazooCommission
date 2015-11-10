from kazoocommission import config
import couchdb.client


class KazooDeviceService:
    """ Provides access to Kazoo platform Devices.

        :param couch_client: The CouchDB client to use to interact with the
                             Kazoo CouchDB database. The default is
                             couchdb-python.
        :type couch_client: couchdb.client.Server
    """

    def __init__(self, couch_client=None):
        self.couch_client = couch_client

        if self.couch_client is None:
            self.couch_client = couchdb.client.Server(
                config.KAZOO_COUCH_DB_URL)

    def get_device_by_mac_address(self, account_name, mac_address):
        """ Gets a specific device for an account by MAC address.

        :param account_name: Account Name to retrieve a device from.
        :param mac_address: Device MAC address in lowercase, colon delimited
               format (57:fb:69:4a:f5:c5)
        :return: Device Configuration
        :type mac_address: str
        :rtype: dict
        """

        couch_account_id = self._get_couch_account_id_for_account_name(
            account_name)

        if couch_account_id is None:
            return None

        device_data = self._retrieve_device(couch_account_id, mac_address)

        if not device_data:
            return None

        return device_data

    def _get_couch_account_id_for_account_name(self, account_name):
        try:
            account_list = list(self.couch_client['accounts'].view(
                'accounts/listing_by_name',
                key=account_name))
            account_id = account_list[0]['value']['account_id']
        except IndexError:
            return None

        couch_account_id = self._get_kazoo_account_id_couch_db_format(
            account_id)

        return couch_account_id

    @staticmethod
    def _get_kazoo_account_id_couch_db_format(account_id):
        part_one = account_id[0:2]
        part_two = account_id[2:4]
        part_three = account_id[4:]
        couch_account_id = 'account' + '/' + part_one + '/' + \
                           part_two + '/' + part_three

        return couch_account_id

    def _retrieve_device(self, account_id_couch, mac_address):
        try:
            device_id = list(self.couch_client[account_id_couch].view(
                'devices/listing_by_macaddress', key=mac_address))[0]['id']
            unfiltered_device_data = \
                self.couch_client[account_id_couch][device_id]
        except IndexError:
            return None

        device_data = self._remove_private_keys_from_device(
            unfiltered_device_data)

        device_data['line_display_text'] = self._get_line_display_text(
            device_data)

        return unfiltered_device_data

    @staticmethod
    def _remove_private_keys_from_device(unfiltered_device_data):
        return {key: unfiltered_device_data[key] for key in
                unfiltered_device_data.keys() if not key.startswith('pvt_')}

    @staticmethod
    def _get_line_display_text(device_data):
        if 'caller_id' in device_data:
            caller_id = device_data['caller_id']

            if 'internal' in caller_id:
                internal = caller_id['internal']

                if 'name' in internal and 'number' in internal:
                    return internal['number'] + '-' + internal['name']

        return device_data['name']
