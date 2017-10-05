# Ansible-statuscake

Ansible module for manage tests on statuscake API. 

## Requirements

Ansible 2.2+

## Documentation

### Module options

[StatusCake API Documentation](https://www.statuscake.com/api)

| Name                 | Required | Description                                                                                   | Default        |
|:---------------------|:---------|:----------------------------------------------------------------------------------------------|:---------------|
| username             | true     | StatusCake username                                                                           |                |
| api_key              | true     | StatusCake API Key                                                                            |                |
| name                 | true     | Test name                                                                                     |                |
| url                  | true     | Test location, either an IP or a FQDN                                                         |                |
| state                | false    | Indicates the desired test state. It must be present or absent                                | present        |
| test_tags            | false    | Tags should be seperated by a comma. e.g.: this,is,a,set,of,tags                              |                |
| check_rate           | false    | The number of seconds between checks                                                          | 300            |
| test_type            | false    | Test type to use                                                                              | HTTP           |
| contact_group        | false    | Contact group ID                                                                              |                |
| user_agent           | false    | Custom user agent                                                                             |                |
| paused               | false    | 0 to unpause, 1 to pause                                                                      | 0 (unpaused)   |
| node_locations       | false    | Node locations ID seperated by a comma                                                        |                |
| confirmation         | false    | Alert delay rate                                                                              | 300            |
| timeout              | false    | Timeout in seconds                                                                            | 30             |
| status_codes         | false    | Comma seperated list of StatusCodes to trigger error on                                       | Stantard codes |

### Example usage:

``` yml
---
- hosts: localhost
  vars_files:
    - "vars.yml"

  tasks:
    - name: Create statuscake test
      statuscake: 
        username: "username"
        api_key: "api_key"
        state: present
        name: google
        url: www.google.com
        test_type: HTTP
        confirmation: 6
        paused: 0
        check_rate: 300
        status_codes: '204,205,206,303,400,401,404,405,406,408,410,444,429,494,495,496,499,500,501,502,504,505,506,507,511,598,599'
        timeout: 500
        test_tags: "GoogleWeb"
        user_agent: "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
      with_items: "{{ tests }}"
```

``` bash
$ ansible-playbook -i localhost, example.yml
```
