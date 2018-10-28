const request = require('request');
const { promisify } = require('util');

const requestp = promisify(request);

class CpanelDnsUpdater {
	constructor(host, domain, username, password) {
		this._cpanelHost = host;
		this._cpanelDomain = domain;
        this._cpanelUsername = username;
        this._cpanelPassword = password;
	}

	async addRecord(params) {
		const recordParams = Object.assign({}, {
			cpanel_jsonapi_module: 'ZoneEdit',    
			cpanel_jsonapi_func: 'add_zone_record',
			domain: this._cpanelDomain,
			type: 'A',
			class: 'IN',
			ttl: 14400
		}, params);
		return !!(await this._cpanelRequest(recordParams));
	}

	async removeRecord(filterParams) {
		const hosts = await this.getRecord(filterParams);
		const results = [];
		for (let hostInfo of hosts) {
			const deleteParams = {
				cpanel_jsonapi_module: 'ZoneEdit',    
				cpanel_jsonapi_func: 'remove_zone_record',
				domain: this._cpanelDomain,
				line: hostInfo.line || hostInfo.Line
			};
			results.push(!!(await this._cpanelRequest(deleteParams)));
		}
		return results.every(r => r);
	}

	async editRecord(filterParams, updatedParams) {
		const hosts = await this.getRecord(filterParams);
		const results = [];
		for (let hostInfo of hosts) {
			const updateParams = Object.assign({}, {
				cpanel_jsonapi_module: 'ZoneEdit',    
				cpanel_jsonapi_func: 'edit_zone_record',
				domain: this._cpanelDomain
			}, hostInfo, updatedParams);
			results.push(!!(await this._cpanelRequest(updateParams)));
		}
		return results.every(r => r);
	}
	
	async getRecord(filter) {
		const fetchzoneParams = {
			cpanel_jsonapi_module: 'ZoneEdit',    
			cpanel_jsonapi_func: 'fetchzone_records',
			domain: this._cpanelDomain,
			customonly: 1
		};
		
		const result = await this._cpanelRequest(fetchzoneParams);

		if (!!result && result.data.length === 0) {
			return [];
		}
		
		const zoneFile = result.data;
		const hosts = [];
		for (let line of zoneFile) {
			if (!filter || Object.keys(filter).every(k => line[k] === filter[k])) {
				hosts.push(line);
			}
		}
		return hosts;
	}
	
	async _cpanelRequest(params) {
		if (!params) {
			return null;
		}
		try {
			const response = await requestp({
				method: 'GET',
				uri: `${this._cpanelHost}/json-api/cpanel?${Object.keys(params).map(k => `${k}=${params[k]}`).join('&')}`,
				auth: {
					user: this._cpanelUsername,
					pass: this._cpanelPassword
				}
			});

			const jsonResult = JSON.parse(response.body);
			if (jsonResult.cpanelresult) {
				return jsonResult.cpanelresult;
			}
			else {
				console.log(jsonResult.error || 'Unknown error');
				throw new Error();
			}
		}
		catch(e) {
			return null;
		}
	}
}

module.exports = CpanelDnsUpdater;

// const cpanelHost = 'https://cpanel.example.com';
// const cpanelDomain = 'example.com';
// const cpanelUsername = 'username';
// const cpanelPassword = 'password';
// const dns = new CpanelDnsUpdater(cpanelHost, cpanelDomain, cpanelUsername, cpanelPassword);

// dns.addRecord({
// 	name: 'foobarbaz.example.com.',
// 	type: 'TXT',
// 	ttl: 600,
// 	txtdata: 'helloworld'
// }).then(val => console.log(val));

// dns.getRecord({
// 	name: 'foobarbaz.example.com.',
// 	type: 'TXT'
// }).then(val => console.log(val));

// dns.editRecord({
// 	name: 'foobarbaz.example.com.',
// 	type: 'TXT'
// },{
// 	name: 'foobarbaz.example.com.',
// 	type: 'TXT',
// 	txtdata: 'forceupdate'
// }).then(val => console.log(val));

// dns.removeRecord({
// 	name: 'foobarbaz.example.com.',
// 	type: 'TXT'
// }).then(val => console.log(val));
