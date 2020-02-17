#!/usr/bin/python

from ansible.errors import AnsibleError
from ansible.module_utils.basic import to_native, AnsibleModule
import datetime
ANSIBLE_METADATA = {
    'metadata_version': '1.0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: irr_prefix

short_description: Generater IRR prefix-list

version_added: "0.0.1"

description:
    - "This modules runs bgpq3 to generate model based prefix-list"

options:
    asn32Safe:
        description:
            - "assume that your device is asn32-safe"
        required: false
        default: false
    IPv:
        description:
            - "IP protocol version"
        required: true
        choices: [ 4 , 6]
    aggregate:
        description:
            - "If true aggregate the prefix"
        required: false
        default: false
    asSet:
        descriptio:
            - "The ASN IRR AS-SET"
        required: true
requirements:
    - bgpq3
author:
    - Renato Almeida de Oliveira (renato.a.oliveira@pm.me)
'''

EXAMPLES = '''
# Get as prefix-list
- name: Get prefix-list
  irr_prefix:
    asn32_safe: true
    IPv: 4
    as-set: AS1234

'''


def bgpq3Query(module, path):
    args = module.params["IPv"]
    if module.params["asn32Safe"]:
        args = args + "3"
    if module.params["aggregate"]:
        args = args + "A"
    cmd = "%s -%s -l irr_prefix %s", (path, args, module.params["asSet"])
    rc, stdout, stderr = module.run_command(cmd, cwd=repo_path)
    if stderr != "":
        raise AnsibleError(" bgpq3 error: %s " % to_native(stderr))
    return stdout


def main():

    fields = {
        "asn32Safe":    {"default": False, "type": "bool"},
        "IPv":          {"required": True, "type": "str", "choices": ['4', '6']},
        "aggregate":    {"default": False, "type": "bool"},
        "asSet":        {"required": True, "type": "str"}

    }
    module = AnsibleModule(argument_spec=fields)
    path = module.get_bin_path('bgpq3', True)
    result = dict(changed=False, warnings=list())
    try:
        response = bgpq3Query(module, path)
        result.update(changed=True, message=to_native(response))
    except Exception as e:
        module.fail_json(msg=to_native(e))
    module.exit_json(**result)


if __name__ == '__main__':
    main()
