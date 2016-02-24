import pytest
from marcopolo import objects as obj

SCHEMAS = {
  'v1.0.0': ["""
---
- schema_version: 1.0.0
  name: Service API
  aliases:
    - api
  summary: My service API
  description: long description
  source: https://github.com/examplecom/api
  tracker: https://issues.example.com/api
  website: https://api.example.com
  owner: johndoe
  environment_name_template: "{{name}} {{tier}}"
  environments:
    - tier: dev
      datacenters:
        - dc2
      aliases:
	- api.dev.dc2.example.com
        - https://api.dev.dc2.example.com
        - https://api.dev.dc2.example.com/v1
      dependencies:
        - https://idm.staging.example.com/v1
      infrastructure: publiccloud
    - tier: staging
      datacenters:
        - dc2
      aliases:
	- api.staging.example.com
        - https://api.staging.example.com
        - https://api.staging.example.com/v1
      dependencies:
        - https://idm.staging.example.com/v1
      infrastructure: privatecloud
""", """
---
- schema_version: 1.0.0
  name: Service idm
  aliases:
    - idm
  summary: My service idm
  description: long description
  source: https://github.com/examplecom/idm
  tracker: https://issues.example.com/idm
  website: https://idm.example.com
  owner: gregswift
  environment_name_template: "{{name}} {{tier}}"
  environments:
    - tier: dev
      datacenters:
        - dc2
      aliases:
	- idm.dev.dc2.example.com
        - https://idm.dev.dc2.example.com
        - https://idm.dev.dc2.example.com/v1
      dependencies:
        - https://api.staging.example.com/v1
      infrastructure: publiccloud
    - tier: staging
      datacenters:
        - dc2
      aliases:
	- idm.staging.example.com
        - https://idm.staging.example.com
        - https://idm.staging.example.com/v1
      dependencies:
        - https://api.staging.example.com/v1
      infrastructure: privatecloud
"""
  ]
}

@pytest.fixture(scope='function',
                params=SCHEMAS)
def data(request):
  return obj.parse(request.param)
