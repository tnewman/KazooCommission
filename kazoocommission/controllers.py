from flask import abort, Flask, make_response, render_template, request
from functools import wraps
from kazoocommission import config
from kazoocommission.services import KazooAccountService, KazooDeviceService

app = Flask(__name__)


def authenticate(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        account_service = kwargs.get('account_service')
        device_service = kwargs.get('device_service')

        kwargs.pop('account_service', None)
        kwargs.pop('device_service', None)

        mac_address_delimited = ':'.join(
            a+b for a, b in zip(kwargs['mac_address'][::2],
                                kwargs['mac_address'][1::2])).lower()

        if account_service is None:
            account_service = KazooAccountService()

        if device_service is None:
            device_service = KazooDeviceService()

        try:
            kwargs['account_data'] = account_service.get_account_by_name(
                kwargs['account'])

            if not kwargs['account_data']:
                abort(404)

            kwargs['device_data'] = device_service.get_device_by_mac_address(
                kwargs['account_data']['id'], mac_address_delimited)

            if not kwargs['device_data']:
                abort(404)
        except ValueError:
            abort(404)

        if config.SSL_CLIENT_SUBJECT_VALIDATION:
            ssl_subject = request.headers.get('X-SSL-Subject')

            if not ssl_subject:
                abort(403)

            if not kwargs['mac_address'] in ssl_subject:
                abort(403)

        return fn(*args, **kwargs)

    return decorated_view


@app.route('/<manufacturer>/<model>/<account>/<mac_address>.xml')
@authenticate
def get_provisioning_file(manufacturer, model, account, mac_address,
                          account_data, device_data):

    template_path = manufacturer + '/' + model + '.xml'

    phone_config = render_template(template_path, config=config,
                                   account=account_data, device=device_data,
                                   mac_address=mac_address)

    response = make_response(phone_config)
    response.headers['Content-Type'] = 'application/xml'

    return response
