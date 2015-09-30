from flask import abort, Flask, make_response, render_template, request, \
    Response
from functools import wraps
from kazoocommission import config
from kazoocommission.services import KazooAccountService, KazooDeviceService

app = Flask(__name__)


def authenticate(fn, account_service=None, device_service=None):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        nonlocal account_service
        nonlocal device_service

        mac_address_delimited = ':'.join(
            a+b for a, b in zip(kwargs['mac_address'][::2],
                                kwargs['mac_address'][1::2])).lower()

        if account_service is None:
            account_service = KazooAccountService()

        if device_service is None:
            device_service = KazooDeviceService()

        try:
            account = account_service.get_account_by_name(kwargs['account'])

            if not account:
                abort(404)

            device = device_service.get_device_by_mac_address(
                account['id'], mac_address_delimited)

            if not device:
                abort(404)
        except ValueError:
            abort(404)

        if request.authorization and \
           request.authorization.username == device['sip']['username'] and \
           request.authorization.password == device['sip']['password']:
            kwargs['account_data'] = account
            kwargs['device_data'] = device

            return fn(*args, **kwargs)

        else:
            return Response('Please supply proper device credentials.',
                            401, {'WWW-Authenticate':
                                  'Basic realm="Login Required"'})

    return decorated_view


@app.route('/grandstream/<model>/<account>/cfg<mac_address>.xml')
@authenticate
def get_grandstream_provisioning_file(model, account, mac_address,
                                      account_data, device_data):
    phone_config = render_template('ht502.xml', config=config,
                                   account=account_data, device=device_data,
                                   mac_address=mac_address)

    response = make_response(phone_config)
    response.headers['Content-Type'] = 'application/xml'

    return response

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host='0.0.0.0')
