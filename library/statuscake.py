import requests
from ansible.module_utils.basic import *

class StatusCake:
    URL_UPDATE_TEST = "https://app.statuscake.com/API/Tests/Update"
    URL_ALL_TESTS = "https://app.statuscake.com/API/Tests"
    URL_DETAILS_TEST = "https://app.statuscake.com/API/Tests/Details"

    def __init__(self, module, username, api_key, name, url, state, test_tags, check_rate, test_type, contact_group, user_agent, paused, node_locations, confirmation, timeout, status_codes):
        self.headers = {"Username": username, "API": api_key}
        self.module = module
        self.name = name
        self.url = url
        self.state = state
        self.test_tags = test_tags
        self.test_type = test_type
        self.contact_group = contact_group
        self.user_agent = user_agent
        self.paused = paused
        self.node_locations = node_locations
        self.confirmation = confirmation
        self.timeout = timeout
        self.status_codes = status_codes

        if not check_rate:
            self.check_rate = 300
        else:
            self.check_rate = check_rate

    def check_response(self,response):
        if response['Success'] == False:
            self.module.exit_json(changed=False, meta= response['Message'])
        else:
            self.module.exit_json(changed=True, meta= response['Message'])
            
    def check_test(self):
        response = requests.put(self.URL_ALL_TESTS, headers=self.headers)
        json_resp = response.json()

        for item in json_resp:
            if item['WebsiteName'] == self.name:
                return item['TestID']

    def delete_test(self):
        test_id = self.check_test()

        if not test_id:
            self.module.exit_json(changed=False, msg="This test doens't exists")
        else:
            data = {'TestID': test_id}
            response = requests.delete(self.URL_DETAILS_TEST, headers=self.headers,data=data)
            self.check_response(response.json())
                    
    def create_test(self):
        data = {"WebsiteName": self.name,
                "WebsiteURL": self.url,
                "CheckRate": self.check_rate,
                "TestType": self.test_type,
                "TestTags": self.test_tags,
                "ContactGroup": self.contact_group,
                "UserAgent": self.user_agent,
                "Paused": self.paused,
                "NodeLocations": self.node_locations,
                "Confirmation": self.confirmation,
                "Timeout": self.timeout,
                "StatusCodes": self.status_codes}

        test_id = self.check_test()
        
        if not test_id:
            response = requests.put(self.URL_UPDATE_TEST, headers=self.headers, data=data)    
            self.check_response(response.json())
        else:
            data['TestID'] = test_id
            response = requests.put(self.URL_UPDATE_TEST, headers=self.headers, data=data)
            self.check_response(response.json())

def run_module():

    module_args = dict(
        username=dict(type='str', required=True),
        api_key=dict(type='str', required=True),
        name=dict(type='str', required=True),
        url=dict(type='str', required=True),
        state = dict(default='present', choices=['absent', 'present']),
        test_tags=dict(type='str', required=False),
        check_rate=dict(type='int', required=False),
        test_type=dict(type='str', required=False),
        contact_group=dict(type='int', required=False),
        user_agent=dict(type='str', required=False),
        paused=dict(type='int', required=False),
        node_locations=dict(type='str', required=False),
        confirmation=dict(type='int', required=False),
        timeout=dict(type='int', required=False),
        status_codes=dict(type='str', required=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    
    username = module.params['username']
    api_key = module.params['api_key']
    name = module.params['name']
    url = module.params['url']
    state = module.params['state']
    test_tags = module.params['test_tags']
    check_rate = module.params['check_rate']
    test_type = module.params['test_type']
    contact_group = module.params['contact_group']
    user_agent = module.params['user_agent']
    paused = module.params['paused']
    node_locations = module.params['node_locations']
    confirmation = module.params['confirmation']
    timeout = module.params['timeout']
    status_codes = module.params['status_codes']

    test = StatusCake(module, username, api_key, name, url, state, test_tags, check_rate, test_type, contact_group, user_agent, paused, node_locations, confirmation, timeout, status_codes)

    if state == "absent":
        test.delete_test()
    else:
        test.create_test()

def main():
    run_module()

if __name__ == '__main__':  
    main()
