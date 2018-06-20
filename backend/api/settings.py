import ssl

# Axis Specific LDAP configuration
LDAP_SERVER = 'ldap://ldap.example.com'
LDAP_PORT = 8080

LDAP_USE_TLS = False
LDAP_REQUIRE_CERT = ssl.CERT_NONE
AUTH_LDAP_INITIAL_PATTERN = "{}@example.com"
LDAP_AUTH_BASEDN = 'dc=example,dc=com'
LDAP_SAMACCOUNT_FILTER = "(sAMAccountName={})"
LDAP_GROUP_SEARCH_FILTER = "(&" + LDAP_SAMACCOUNT_FILTER + "(memberOf={}))"
LDAP_CN_MATCH = 'CN=([^,]+),.*'

LDAP_TOOLS_ADMIN_GROUPS = \
    ["cn=org-example,ou=role,ou=groups,dc=example,dc=com"]
LDAP_AUTH_ENDPOINTS = {r"api/all": False,
                       r"api/all/.+": False,
                       r"api": True}

############################################################
# Python Eve configuration http://python-eve.org/config.html
############################################################

# Database configuration
MONGO_HOST = 'db'
MONGO_PORT = 27028
MONGO_DBNAME = 'aliases_db'
# Database features to not expose on url params
MONGO_QUERY_BLACKLIST = ['$where']

# Turn off XML response and use JSON
XML = False
JSON = True
# Allowed methods for entire resources, note that delete should not be allowed
RESOURCE_METHODS = ['GET', 'PATCH', 'POST']
# Allowed methods for single items
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
# If single item lookup should be available
ITEM_LOOKUP = True
# Disables concurrency control http://python-eve.org/features.html#concurrency
IF_MATCH = False
# Disables bulk inserts
BULK_ENABLED = False
# Turns off soft delete feature
SOFT_DELETE = False
# Makes development easier can be deleted for increased security
X_DOMAINS = '*'
X_ALLOW_CREDENTIALS = True
X_HEADERS = ['Authorization', 'Content-Type']
X_EXPOSE_HEADERS = ['Authorization', 'Content-Type']
# Tells frontend how long the data should be keept on multiple equal requests
CACHE_CONTROL = 'max-age=6'
CACHE_EXPIRES = 6

# Data validation http://python-eve.org/validation.html
schema = {
    'pattern': {
        'type': 'urlpattern',
        'required': True,
        'unique': True,
    },
    'target': {
        'type': 'string',
        'required': True
    },
    'ldapuser': {
        'type': 'string'
    }
}
all_alias = {
    'item_title': 'all',
    'resource_methods': ['GET'],
    'datasource': {
        'source': 'aliases_db',
        'projection': {
            'pattern': 1,
            'target': 1,
            'ldapuser': 1}
    }
}
get_ldapuser_alias = {
    'url': 'api/all/<regex("[\w\s]+"):ldapuser>',  # pylint: disable=anomalous-backslash-in-string
    'item_title': 'ldapuser/alias',
    'resource_methods': ['GET'],
    'datasource': {
        'source': 'aliases_db'
    },
    'schema': schema
}
alias = {
    'item_title': 'alias',
    'resource_methods': ['POST'],
    'item_methods': ['DELETE', 'PATCH', 'PUT'],
    'datasource': {
        'source': 'aliases_db'
    },
    'schema': schema
}
DOMAIN = {
    'api/all': all_alias,
    'api/all/user': get_ldapuser_alias,
    'api': alias
}
