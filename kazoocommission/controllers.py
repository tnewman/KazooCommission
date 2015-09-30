from flask import abort, Flask, request, Request, Response
from functools import wraps
from kazoocommission import config
from kazoocommission.services import KazooAccountService, KazooDeviceService

app = Flask(__name__)


def authenticate(fn, account_service=None, device_service=None):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        nonlocal account_service
        nonlocal device_service

        kwargs['mac_address'] = ':'.join(
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
                account['data']['id'], kwargs['mac_address'])

            if not device:
                abort(404)
        except ValueError:
            abort(404)

        if request.authorization and \
           request.authorization.username == device['sip']['username'] and \
           request.authorization.password == device['sip']['password']:
            return fn(*args, **kwargs)

        else:
            return Response('Please supply proper device credentials.',
                            401,
                            {'WWW-Authenticate':
                             'Basic realm="Login Required"'})

    return decorated_view


@app.route("/<account>/grandstream/<model>/cfg<mac_address>.xml")
@authenticate
def get_grandstream_provisioning_file(account, model, mac_address):
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
