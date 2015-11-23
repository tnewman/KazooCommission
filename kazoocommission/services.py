from kazoocommission import config
import couchdb.client


class KazooBaseService:
    def __init__(self, couch_client=None):
        """ Base class to provide access to the Kazoo platform.

        :param couch_client: The CouchDB client to use to interact with the
                             Kazoo CouchDB database. The default is
                             couchdb-python.
        :type couch_client: couchdb.client.Server
    """

        self.couch_client = couch_client

        if self.couch_client is None:
            self.couch_client = couchdb.client.Server(
                config.KAZOO_COUCH_DB_URL)

    @staticmethod
    def _remove_private_keys_from_couch_data(unfiltered_couch_data):
        return {key: unfiltered_couch_data[key] for key in
                unfiltered_couch_data.keys() if not key.startswith('pvt_')}

    @staticmethod
    def _get_kazoo_account_id_couch_db_format(account_id):
        part_one = account_id[0:2]
        part_two = account_id[2:4]
        part_three = account_id[4:]
        couch_account_id = 'account' + '/' + part_one + '/' + part_two + '/' \
                           + part_three

        return couch_account_id


class KazooAccountService(KazooBaseService):
    """ Provides access to Kazoo platform accounts.

        :param couch_client: The CouchDB client to use to interact with the
                             Kazoo CouchDB database. The default is
                             couchdb-python.
        :type couch_client: couchdb.client.Server
    """

    def __init__(self, couch_client=None):
        KazooBaseService.__init__(self, couch_client)

    def get_account_by_name(self, account_name):
        """ Gets a specific account by name.

        :param account_name: Account Name to retrieve a device from.
        :return: Account Data
        :type account_name: str
        :rtype: dict
        """

        try:
            account_list = list(self.couch_client['accounts'].view(
                'accounts/listing_by_name',
                key=account_name))
            account_id = account_list[0]['id']
            account_data = self.couch_client['accounts'][account_id]
        except IndexError:
            return None

        account_data = self._remove_private_keys_from_couch_data(account_data)

        return account_data


class KazooDeviceService(KazooBaseService):
    """ Provides access to Kazoo platform Devices.

        :param couch_client: The CouchDB client to use to interact with the
                             Kazoo CouchDB database. The default is
                             couchdb-python.
        :type couch_client: couchdb.client.Server
    """

    def __init__(self, couch_client=None):
        KazooBaseService.__init__(self, couch_client)

    def get_device_by_mac_address(self, account_id, mac_address):
        """ Gets a specific device for an account by MAC address.

        :param account_id: Account ID to retrieve a device from.
        :param mac_address: Device MAC address in lowercase, colon delimited
               format (57:fb:69:4a:f5:c5)
        :return: Device Configuration
        :type mac_address: str
        :rtype: dict
        """

        couch_account_id = self._get_kazoo_account_id_couch_db_format(
            account_id)

        device_data = self._retrieve_device(couch_account_id, mac_address)

        return device_data

    def _retrieve_device(self, account_id_couch, mac_address):
        try:
            device_id = list(self.couch_client[account_id_couch].view(
                'devices/listing_by_macaddress', key=mac_address))[0]['id']
            device_data = self.couch_client[account_id_couch][device_id]
        except IndexError:
            return None

        device_data = self._remove_private_keys_from_couch_data(device_data)

        device_data['line_display_text'] = self._get_line_display_text(
            device_data)

        return device_data

    @staticmethod
    def _get_line_display_text(device_data):
        if 'caller_id' in device_data:
            caller_id = device_data['caller_id']

            if 'internal' in caller_id:
                internal = caller_id['internal']

                if 'name' in internal and 'number' in internal:
                    return internal['number'] + '-' + internal['name']

        return device_data['name']
