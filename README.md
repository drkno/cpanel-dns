## Cpanel DNS

Automation of Cpanel in node and python3, enabling automated issuing of wildcard certificates from letsencrypt.

This tool expects to be installed to `/opt/cpanel-dns`

### Creating Initial Certificates

1. Create a file called `secrets.json` containing:
```js
{
        "cpanelHost": "http://cpanel.example.com",
        "cpanelDomain": "example.com",
        "cpanelUsername": "username",
        "cpanelPassword": "password"
}
```
2. Configure nginx as required.
3. Run `CERT_EMAIL=myemail@example.com CERT_DOMAIN=example.com ./issue_cert.sh

### Renewing Certificates

Call `CERT_EMAIL=myemail@example.com ./renew_cert.sh`.

