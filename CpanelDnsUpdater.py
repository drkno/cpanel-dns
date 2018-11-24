import urllib.request, urllib.error, urllib.parse, base64, json

class CpanelDnsUpdater:
    def __init__(self, host, domain, username, password):
        self._cpanelHost = host
        self._cpanelDomain = domain
        self._cpanelUsername = username
        self._cpanelPassword = password

    def addRecord(self, params):
        recordParams = {
            'cpanel_jsonapi_module': 'ZoneEdit',    
            'cpanel_jsonapi_func': 'add_zone_record',
            'domain': self._cpanelDomain,
            'type': 'A',
            'class': 'IN',
            'ttl': 14400
        }
        recordParams.update(params)
        result = self._cpanelRequest(recordParams)
        return result is not None

    def removeRecord(self, filterParams):
        hosts = self.getRecord(filterParams)
        results = []
        for hostInfo in hosts:
            deleteParams = {
                'cpanel_jsonapi_module': 'ZoneEdit',    
                'cpanel_jsonapi_func': 'remove_zone_record',
                'domain': self._cpanelDomain,
                'line': hostInfo['line']
            }
            results.append(self._cpanelRequest(deleteParams) is not None)
        return all(results)

    def editRecord(self, filterParams, updatedParams):
        hosts = self.getRecord(filterParams)
        results = []
        for hostInfo in hosts:
            updateParams = {
                'cpanel_jsonapi_module': 'ZoneEdit',    
                'cpanel_jsonapi_func': 'edit_zone_record',
                'domain': self._cpanelDomain
            }
            updateParams.update(hostInfo)
            updateParams.update(updatedParams)
            results.append(self._cpanelRequest(updateParams) is not None)
        return all(results)
    
    def getRecord(self, filter):
        fetchzoneParams = {
            'cpanel_jsonapi_module': 'ZoneEdit',    
            'cpanel_jsonapi_func': 'fetchzone_records',
            'domain': self._cpanelDomain,
            'customonly': 1
        }
        
        result = self._cpanelRequest(fetchzoneParams)

        if (result is None or len(result['data']) == 0):
            return []
        
        zoneFile = result['data']
        hosts = []
        for line in zoneFile:
            if filter is None or all([line[key] == val for (key, val) in filter.items()]):
                hosts.append(line)
        return hosts
    
    def _cpanelRequest(self, params):
        if params is None:
            return None
        try:
            url = self._cpanelHost + '/json-api/cpanel?' + '&'.join((key + '=' + str(val)) for (key,val) in params.items())
            request = urllib.request.Request(url)
            b64auth = base64.encodestring((self._cpanelUsername + ':' + self._cpanelPassword).encode()).decode('utf-8').replace('\n', '')
            request.add_header('Authorization', 'Basic %s' % b64auth)

            result = urllib.request.urlopen(request)
            jsonResult = json.load(result)

            if jsonResult['cpanelresult'] is not None:
                return jsonResult['cpanelresult']
            else:
                print((jsonResult['error']))
                raise Exception('Return was invalid json') 
        except:
            return None

# cpanelHost = 'https://cpanel.example.com'
# cpanelDomain = 'example.com'
# cpanelUsername = 'username'
# cpanelPassword = 'password'
# dns = CpanelDnsUpdater(cpanelHost, cpanelDomain, cpanelUsername, cpanelPassword)

# print(dns.addRecord({
#     'name': 'foobarbaz.example.com.',
#     'type': 'TXT',
#     'ttl': 600,
#     'txtdata': 'helloworld'
# }))

# print(dns.getRecord({
#     'name': 'foobarbaz.example.com.',
#     'type': 'TXT'
# }))

# print(dns.editRecord({
#     'name': 'foobarbaz.example.com.',
#     'type': 'TXT'
# },{
#     'name': 'foobarbaz.example.com.',
#     'type': 'TXT',
#     'txtdata': 'forceupdate'
# }))

# print(dns.removeRecord({
#     'name': 'foobarbaz.example.com.',
#     'type': 'TXT'
# }))
