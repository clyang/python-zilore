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

    def add_record(self, domain_name='', record_type='', record_ttl=600, record_name='', record_value=''):
        record_type = record_type.upper()

        if not record_name.endswith(domain_name):
            record_name = '{}.{}'.format(record_name, domain_name)
        if record_type == 'TXT':
            record_value = '"{}"'.format(record_value)

        params = 'record_type={}&record_ttl={}&record_name={}&record_value={}'.format(record_type, record_ttl, record_name, record_value)
        return self._do_request('domains/{}/records'.format(domain_name), params, 'post')

    def update_record(self, domain_name='', record_id=None, record_type='', record_ttl=600, record_name='', record_value=''):
        record_type = record_type.upper()

        if record_name != '' and not record_name.endswith(domain_name):
            record_name = '{}.{}'.format(record_name, domain_name)
        if record_type == 'TXT':
            record_value = '"{}"'.format(record_value)

        args = locals()
        params = ''
        for k, v in args.items():
            if k in ['self', 'domain_name', 'record_id']:
                continue
            if v != '' and v is not None:
                params += '&{}={}'.format(k, v)

        return self._do_request('domains/{}/records/{}'.format(domain_name, record_id), params, 'put')

    def update_record_status(self, domain_name='', record_id=None, record_status=None):
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

    def geo_records(self, domain_name=''):
        return self._do_request('domains/{}/geo/defaults'.format(domain_name), '', 'get')

    def list_geo_records(self, domain_name='', offset=0, limit='', order_by='', order_param='', search_text=''):
        params = 'offset={}&limit={}&order_by={}&order_param={}&search_text={}'.format(offset, limit, order_by, order_param, search_text)
        return self._do_request('domains/{}/geo'.format(domain_name), params, 'get')

    def add_geo_record(self, domain_name='', record_name='', record_type='', geo_region='', record_value=''):
        params = 'record_name={}&record_type={}&geo_region={}&record_value={}'.format(record_name, record_type, geo_region, record_value)
        return self._do_request('domains/{}/geo'.format(domain_name), params, 'post')

    def update_geo_record(self, domain_name='', record_id=None, geo_region='', record_value=''):
        args = locals()
        params = ''
        for k, v in args.items():
            if k in ['self', 'domain_name', 'record_id']:
                continue
            if v != '' and v is not None:
                params += '&{}={}'.format(k, v)

        return self._do_request('domains/{}/geo/{}'.format(domain_name, record_id), params, 'put')

    def failover_records(self, domain_name=''):
        return self._do_request('domains/{}/failovers/available'.format(domain_name), '', 'get')

    def list_failover_records(self, domain_name='', offset=0, limit='', order_by='', order_param=''):
        params = 'offset={}&limit={}&order_by={}&order_param={}'.format(offset, limit, order_by, order_param)
        return self._do_request('domains/{}/failovers'.format(domain_name), params, 'get')

    def add_failover_record(self, domain_name='', record_id=None, failover_check_type='', failover_check_interval='', failover_return_to_main_value='', failover_additional_port='', failover_record_backup_value=[], failover_use_fws='', failover_additional_response='', failover_additional_request='', failover_notification_email='', failover_notification_sms=''):
        backup_value_str = ''
        if isinstance(failover_record_backup_value, list) and failover_record_backup_value:
            max_val = min(len(failover_record_backup_value) ,3)
            for i in range(max_val):
                backup_value_str += 'failover_record_backup_value[{}]={}&'.format(i, failover_record_backup_value[i])

        params = 'record_id={}&failover_check_type={}&failover_check_interval={}&failover_return_to_main_value={}&failover_additional_port={}&failover_use_fws={}&failover_notification_email={}&failover_notification_sms={}'.format(record_id, failover_check_type, failover_check_interval, failover_return_to_main_value, failover_additional_port, failover_use_fws, failover_notification_email, failover_notification_sms)
        if failover_check_type == 'TCP':
            params = '{}&failover_additional_respons={}&failover_additional_request={}'.format(params, failover_additional_respons, failover_additional_request)
        params = '{}&{}'.format(params, backup_value_str)

        return self._do_request('domains/{}/failovers'.format(domain_name), params, 'post')

    def update_failover_record(self, domain_name='', record_id=None, failover_check_type='', failover_check_interval='', failover_return_to_main_value='', failover_additional_port='', failover_record_backup_value=[], failover_use_fws='', failover_additional_response='', failover_additional_request='', failover_notification_email='', failover_notification_sms=''):
        backup_value_str = ''
        if isinstance(failover_record_backup_value, list) and failover_record_backup_value:
            max_val = min(len(failover_record_backup_value) ,3)
            for i in range(max_val):
                backup_value_str += 'failover_record_backup_value[{}]={}&'.format(i, failover_record_backup_value[i])

        params = 'failover_check_type={}&failover_check_interval={}&failover_return_to_main_value={}&failover_additional_port={}&failover_use_fws={}&failover_notification_email={}&failover_notification_sms={}'.format(record_id, failover_check_type, failover_check_interval, failover_return_to_main_value, failover_additional_port, failover_use_fws, failover_notification_email, failover_notification_sms)
        if failover_check_type == 'TCP':
            params = '{}&failover_additional_respons={}&failover_additional_request={}'.format(params, failover_additional_respons, failover_additional_request)
        params = '{}&{}'.format(params, backup_value_str)

        return self._do_request('domains/{}/failovers/{}'.format(domain_name, record_id), params, 'put')

    def delete_failover_record(self, domain_name='', record_id=[]):
        if isinstance(record_id, int):
            record_id = [record_id]

        params = 'record_id={}'.format(','.join(str(x) for x in record_id))
        return self._do_request('domains/{}/failovers'.format(domain_name), params, 'delete')

    def list_mf_addresses(self, domain_name='', offset=0, limit='', order_by='', order_param=''):
        params = 'offset={}&limit={}&order_by={}&order_param={}'.format(offset, limit, order_by, order_param)
        return self._do_request('domains/{}/mail_forwarding'.format(domain_name), params, 'get')

    def add_mf_address(self, domain_name='', source='', destination=''):
        suffix = '@{}'.format(domain_name)
        source = source.replace(suffix, '')

        params = 'source={}&destination={}'.format(source, destination)
        return self._do_request('domains/{}/mail_forwarding'.format(domain_name), params, 'post')

    def update_mf_address(self, domain_name='', mf_address_id='', source='', destination=''):
        args = locals()
        params = ''
        for k, v in args.items():
            if k in ['self', 'domain_name']:
                continue
            if v != '':
                params += '&{}={}'.format(k, v)

        params = params[1:]
        suffix = '@{}'.format(domain_name)
        params = params.replace(suffix, '')

        return self._do_request('domains/{}/mail_forwarding/{}'.format(domain_name, mf_address_id), params, 'put')

    def update_mf_address_status(self, domain_name='', mf_address_id=None, status=None):
        params = 'status={}'.format(status)
        return self._do_request('domains/{}/mail_forwarding/{}/status'.format(domain_name,mf_address_id), params, 'put')

    def delete_mf_address(self, domain_name='', mf_address_id=[]):
        if isinstance(mf_address_id, int):
            mf_address_id = [mf_address_id]

        params = 'mf_address_id={}'.format(','.join(str(x) for x in mf_address_id))
        return self._do_request('domains/{}/mail_forwarding'.format(domain_name), params, 'delete')

    def list_wf_addresses(self, domain_name='', offset=0, limit='', order_by='', order_param=''):
        params = 'offset={}&limit={}&order_by={}&order_param={}'.format(offset, limit, order_by, order_param)
        return self._do_request('domains/{}/web_forwarding'.format(domain_name), params, 'get')

    def add_wf_address(self, domain_name='', https=None, code=None, source='', destination=''):
        destination = destination.replace('http://', '')
        destination = destination.replace('https://', '')

        params = 'https={}&code={}&destination={}'.format(https, code, destination)
        if source != '':
            suffix = '.{}'.format(domain_name)
            source = source.replace(suffix, '')
            params = '{}&source={}'.format(params, source)

        return self._do_request('domains/{}/web_forwarding'.format(domain_name), params, 'post')

    def update_wf_address(self, domain_name='', wf_address_id=None, https=None, code=None, source='', destination=''):
        destination = destination.replace('http://', '')
        destination = destination.replace('https://', '')

        if source != '':
            source = source.replace('.{}'.format(domain_name), '')

        args = locals()
        params = ''
        for k, v in args.items():
            if k in ['self', 'domain_name', wf_address_id]:
                continue
            if v != '' and v is not None:
                params += '&{}={}'.format(k, v)
        params = params[1:]

        return self._do_request('domains/{}/web_forwarding/{}'.format(domain_name, wf_address_id), params, 'put')

    def update_wf_address_status(self, domain_name='', wf_address_id=None, status=None):
        params = 'status={}'.format(status)
        return self._do_request('domains/{}/web_forwarding/{}/status'.format(domain_name,wf_address_id), params, 'put')

    def delete_wf_address(self, domain_name='', wf_address_id=[]):
        if isinstance(wf_address_id, int):
            wf_address_id = [wf_address_id]

        params = 'wf_address_id={}'.format(','.join(str(x) for x in wf_address_id))
        return self._do_request('domains/{}/web_forwarding'.format(domain_name), params, 'delete')

    def list_custom_templates(self):
        return self._do_request('templates', '', 'get')

    def create_custom_template(self, custom_template_name='', custom_template_description=''):
        params = 'custom_template_name={}'.format(custom_template_name)
        if custom_template_description != '':
            params = '{}&custom_template_description={}'.format(params, custom_template_description)

        return self._do_request('templates', params, 'post')

    def update_custom_template(self, template_id=None, custom_template_name='', custom_template_description=''):
        args = locals()
        params = ''
        for k, v in args.items():
            if k in ['self', 'template_id']:
                continue
            if v != '' and v is not None:
                params += '&{}={}'.format(k, v)
        params = params[1:]

        return self._do_request('templates/{}'.format(template_id), params, 'put')

    def delete_custom_template(self, template_id=None):
        return self._do_request('templates/{}'.format(template_id), '', 'delete')

    def restore_custom_template(self, domain_name='', template_id=None):
        params = 'domain_name={}'.format(domain_name)

        return self._do_request('templates/{}/restore'.format(template_id), params, 'post')

    def list_custom_templates_records(self, template_id=None, domain_name=''):
        params = ''
        if domain_name != '':
            params = 'domain_name={}'.format(domain_name)

        return self._do_request('templates/{}/records'.format(template_id), params, 'get')

    def add_custom_template_record(self, template_id=None, record_type='', record_ttl=600, record_name='', record_value=''):
        record_type = record_type.upper()

        if not record_name.endswith('.{{domain_name}}'):
            record_name = '{}.{{domain_name}}'.format(record_name)
        if record_type == 'TXT':
            record_value = '"{}"'.format(record_value)

        params = 'record_type={}&record_ttl={}&record_name={}&record_value={}'.format(record_type, record_ttl, record_name, record_value)
        return self._do_request('templates/{}/records'.format(template_id), params, 'post')

    def update_custom_template_record(self, template_id=None, record_id=None, record_type='', record_ttl='', record_name='', record_value=''):
        record_type = record_type.upper()

        if not record_name.endswith('.{{domain_name}}'):
            record_name = '{}.{{domain_name}}'.format(record_name)
        if record_type == 'TXT':
            record_value = '"{}"'.format(record_value)

        args = locals()
        params = ''
        for k, v in args.items():
            if k in ['self', 'template_id', 'record_id']:
                continue
            if v != '' and v is not None:
                params += '&{}={}'.format(k, v)

        return self._do_request('templates/{}/records/{}'.format(template_id, record_id), params, 'put')

    def delete_custom_template_record(self, template_id='', record_id=[]):
        if isinstance(record_id, int):
            record_id = [record_id]

        params = 'record_id={}'.format(','.join(str(x) for x in record_id))
        return self._do_request('template/{}/records'.format(template_id), params, 'delete')
