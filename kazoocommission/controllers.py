from flask import abort, Flask, make_response, render_template, request
from functools import wraps
from jinja2.exceptions import TemplateNotFound
from kazoocommission import config
from kazoocommission.services import KazooDeviceService

app = Flask(__name__)


def authenticate(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        device_service = kwargs.get('device_service')

        kwargs.pop('device_service', None)

        mac_address_delimited = ':'.join(
            a+b for a, b in zip(kwargs['mac_address'][::2],
                                kwargs['mac_address'][1::2])).lower()

        if device_service is None:
            device_service = KazooDeviceService()

        kwargs['device_data'] = device_service.get_device_by_mac_address(
            kwargs['account'], mac_address_delimited)

        if kwargs['device_data'] is None:
            abort(404)

        if not config.DISABLE_SSL_CLIENT_SUBJECT_VALIDATION:
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
                          device_data):

    template_path = manufacturer + '/' + model + '.xml'

    try:
        phone_config = render_template(template_path, config=config,
                                       account=account, device=device_data,
                                       mac_address=mac_address)
        response = make_response(phone_config)
        response.headers['Content-Type'] = 'application/xml'

        return response
    except TemplateNotFound:
        abort(404)
