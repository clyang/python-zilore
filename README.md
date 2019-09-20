# python-zilore
[Zilore DNS](https://zilore.com/en/dns) API Python Wrapper. It was implemented by following [Zilore DNS API](https://zilore.com/en/help/api) document.

## Installaion
The easiest way to install `python-zilore` and get updates is by using `pip`

```bash
$ pip install python-zilore
```

## Test installation
You can test your install by using following steps:

1. Log into Zilore DNS management console via Browser
2. Get your own API key in `Setting` page
3. Test if your API key is working with the following Python code

	```python
	import ziloreapi
	
	zdns = ziloreapi.Api('YOUR_API_KEY')
	result = zdns.test_login()
	print(result)
	```

4. Once you see `True` on console, you're all set and ready to rock 'n' roll.

## Usage
It's simple to use the library to interact witgh Zilore DNS.

* Creating a `doamin` called `example.com`

	```python
	import ziloreapi
	
	zdns = ziloreapi.Api('YOUR_API_KEY')
	result = zdns.add_domain('example.com')
	print(result)
	```

* Creating an A record called `test.example.com` with `TTL = 600 seconds` and point it to `10.0.0.1`

	```python
	import ziloreapi
	
	zdns = ziloreapi.Api('YOUR_API_KEY')
	result = zdns.add_record('example.com', 'A', 600,'test', '10.0.0.1')
	print(result)
	```

* Creating a CNAME record called `cname.example.com` with `TTL = 300 seconds` and point it to `www.google.com`

	```python
	import ziloreapi
	
	zdns = ziloreapi.Api('YOUR_API_KEY')
	result = zdns.add_record('example.com', 'CNAME', 300,'cname', 'www.google.com')
	print(result)
	```



* Changing A record `test.example.com` value. Set TTL to 3600 and re-pointing to `192.168.1.1`

	```python
	import ziloreapi
	
	zdns = ziloreapi.Api('YOUR_API_KEY')
	result = zdns.update_record('csie.io', RECORD_ID, 'A', 3600, 'test', '192.168.1.1')
	print(result)
	```

## Current supported API
All API are **FULL SUPPORTED** by python-zilore

* DOMAINS
	* list_domains
	* list_tlds
	* list_nameservers
	* list_statistics
	* add_domain
	* delete_domain

* RECORDS
	* list_records
	* list_valid_record_ttl
	* add_record
	* update_record
	* update_record_status
	* delete_record

* SNAPSHOTS
	* list_snapshots
	* list_snapshots_records
	* restore_snapshot

* GEO RECORDS
	* geo_records
	* list_geo_records
	* add_geo_record
	* update_geo_record

* FAILOVER RECORDS
	* failover_records
	* list_failover_records
	* add_failover_record
	* update_failover_record
	* delete_failover_record

* WEB AND MAIL FORWARDING
	* list_mf_addresses
	* add_mf_address
	* update_mf_address
	* update_mf_address_status
	* delete_mf_address
	* list_wf_addresses
	* add_wf_address
	* update_wf_address
	* update_wf_address_status
	* delete_wf_address

* CUSTOM TEMLATES
	* list_custom_templates
	* create_custom_template
	* update_custom_template
	* delete_custom_template
	* restore_custom_template
	* list_custom_templates_records
	* add_custom_template_record
	* update_custom_template_record
	* delete_custom_template_record

## License
MIT License	
	
