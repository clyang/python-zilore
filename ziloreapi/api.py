import requests
import logging

logger = logging.getLogger(__name__)

class Api(object):
    def __init__(self, x_auth_key):
        self._http_header = {'X-Auth-Key': x_auth_key}
        self._urlbase = 'https://api.zilore.com/dns/v1/{0}?{0}'.format('{}')

    def _do_request(self, function, params='', method='get'):
        method = method.upper()
        logger.debug("Performing request using method {}".format(method))
        response = self._do_raw_request(function, params, method)
        logger.debug("Response: %s", format(response))

        return response.json()

    def _do_raw_request(self, function, params='', method='get'):
        if method == 'GET':
            return requests.get(self._urlbase.format(function, params), headers=self._http_header)
        elif method == 'POST':
            return requests.post(self._urlbase.format(function, params), headers=self._http_header)
        elif method == 'DELETE':
            return requests.delete(self._urlbase.format(function, params), headers=self._http_header)
        elif method == 'PUT':
            return requests.put(self._urlbase.format(function, params), headers=self._http_header)


    def test_login(self):
        response = self._do_raw_request('domains')
        result = response.json()
        if 'status' in result and result['status'] == 'ok':
            return True
        else:
            return False

    def list_domains(self, offset=0, limit=1000, order_by='', order_param='', search_text=''):
        params = 'offset={}&limit={}&order_by={}&order_param={}&search_text={}'.format(offset, limit, order_by, order_param, search_text)
        return self._do_request('domains', params)

    def list_tlds(self, version='', tlds=''):
        params = 'version={}&tlds={}'.format(version, tlds)
        return self._do_request('tlds', params)

    def list_nameservers(self, domain_name=''):
        return self._do_request('domains/{}/nameservers'.format(domain_name))

    def list_statistics(self, domain_name='', period=''):
        params = 'period={}'.format(period)
        return self._do_request('domains/{}/statistics'.format(domain_name))

    def add_domain(self, domain_name=[]):
        params = 'domain_name={}'.format(','.join(domain_name))
        return self._do_request('domains', params, 'post')

    def delete_domain(self, domain_id=[], domain_name=[]):
        if isinstance(domain_id, int):
            domain_id = [domain_id]

        params = 'domain_id={}&domain_name={}'.format(','.join(str(x) for x in domain_id), ','.join(domain_name))
        return self._do_request('domains', params, 'delete')

    def list_records(self, domain_name='', offset=0, limit=10000, order_by='', order_param='', search_text=''):
        params = 'offset={}&limit={}&order_by={}&order_param={}&search_text={}'.format(offset, limit, order_by, order_param, search_text)
        return self._do_request('domains/{}/records'.format(domain_name), params)

    def list_valid_record_ttl(self):
        return self._do_request('settings/ttl')

    def add_record(self, domain_name='', record_type='', record_ttl=300, record_name='', record_value=''):
        record_type = record_type.upper()

        if not record_name.endswith(domain_name):
            record_name = '{}.{}'.format(record_name, domain_name)
        if record_type == 'TXT':
            record_value = '"{}"'.format(record_value)

        params = 'record_type={}&record_ttl={}&record_name={}&record_value={}'.format(record_type, record_ttl, record_name, record_value)
        return self._do_request('domains/{}/records'.format(domain_name), params, 'post')

    def update_record(self, domain_name='', record_id=None, record_type='', record_ttl=300, record_name='', record_value=''):
        record_type = record_type.upper()

        if not record_name.endswith(domain_name):
            record_name = '{}.{}'.format(record_name, domain_name)
        if record_type == 'TXT':
            record_value = '"{}"'.format(record_value)

        params = 'record_type={}&record_ttl={}&record_name={}&record_value={}'.format(record_type, record_ttl, record_name, record_value)
        return self._do_request('domains/{}/records/{}'.format(domain_name, record_id), params, 'put')

    def update_record_status(self, domain_name='', record_id=None, record_status=''):
        params = 'record_status={}'.format(record_status)
        return self._do_request('domains/{}/records/{}/status'.format(domain_name,record_id), params, 'put')

    def delete_record(self, domain_name='', record_id=[]):
        if isinstance(record_id, int):
            record_id = [record_id]

        params = 'record_id={}'.format(','.join(str(x) for x in record_id))
        return self._do_request('domains/{}/records'.format(domain_name), params, 'delete')

    def list_snapshots(self, domain_name=''):
        return self._do_request('domains/{}/snapshots'.format(domain_name), '', 'get')

    def list_snapshots_records(self, domain_name='', snapshot_id=''):
        return self._do_request('domains/{}/snapshots/{}/records'.format(domain_name, snapshot_id), '', 'get')

    def restore_snapshot(self, domain_name='', snapshot_id=''):
        return self._do_request('domains/{}/snapshots/{}/restore'.format(domain_name, snapshot_id), '', 'post')
