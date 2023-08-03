import json
import requests

U_head = 'http://0.0.0.0:8080'


def get_switches():
    url = U_head + '/stats/switches'
    switch_req = requests.get(url=url).json()
    switch_id = []
    for i in switch_req:
        switch_id.append(i)
    return switch_id


def get_flow(switch):
    url = U_head + '/stats/flow/' + str(switch)
    print(url)
    flow_tabel_req = requests.get(url=url).json()
    # flow = json.loads(flow_tabel_req)
    # print(flow_tabel_req)
    for i in flow_tabel_req[str(switch)]:
        print('match:', i['match'], '  |  actions:', i['actions'])


def modify_flow(ip_proto, sw):
    url = U_head + '/stats/flowentry/modify'  # make modify url
    if ip_proto == 6 or ip_proto == 17:  # change tcp or udp sw
        data = {
            "dpid": 1,
            "cookie": 0,
            "cookie_mask": 1,
            "table_id": 0,
            "idle_timeout": 0,
            "hard_timeout": 0,
            "priority": 1000,
            "flags": 0,
            "match": {
                "in_port": 1,
                "eth_type": 0x0800,
                "ip_proto": int(ip_proto)
            },
            "actions": [
                {
                    "type": "OUTPUT",
                    "port": int(sw)
                }
            ]
        }
        requests.post(url=url, json=data)
        data = {
            "dpid": 5,
            "cookie": 0,
            "cookie_mask": 1,
            "table_id": 0,
            "idle_timeout": 0,
            "hard_timeout": 0,
            "priority": 1000,
            "flags": 0,
            "match": {
                "in_port": 1,
                "eth_type": 0x0800,
                "ip_proto": int(ip_proto)
            },
            "actions": [
                {
                    "type": "OUTPUT",
                    "port": int(sw)
                }
            ]
        }
        requests.post(url=url, json=data)
    else:  # change normal sw
        data = {
            "dpid": 1,
            "cookie": 0,
            "cookie_mask": 1,
            "table_id": 0,
            "idle_timeout": 0,
            "hard_timeout": 0,
            "priority": 100,
            "flags": 0,
            "match": {
                "in_port": 1,
            },
            "actions": [
                {
                    "type": "OUTPUT",
                    "port": int(sw)
                }
            ]
        }
        requests.post(url=url + '_strict', json=data)
        data = {
            "dpid": 5,
            "cookie": 0,
            "cookie_mask": 1,
            "table_id": 0,
            "idle_timeout": 0,
            "hard_timeout": 0,
            "priority": 100,
            "flags": 0,
            "match": {
                "in_port": 1,
            },
            "actions": [
                {
                    "type": "OUTPUT",
                    "port": int(sw)
                }
            ]
        }
        requests.post(url=url + '_strict', json=data)


if __name__ == "__main__":
    print(get_switches())
    try:
        while 1:
            invalid = 0
            ip_p = 0
            ip_pro_str = input("Please enter tcp, udp or normal:")
            if ip_pro_str == 'tcp' or ip_pro_str == 'TCP':
                ip_p = 6
            elif ip_pro_str == 'udp' or ip_pro_str == 'UDP':
                ip_p = 17
            elif ip_pro_str == 'normal' or 'NORMAL':
                ip_p = 0
            else:
                invalid = 1
            switch = input("Please enter switch number 2, 3 or 4:")
            if switch != '2' and switch != '3' and switch != '4':
                invalid = 1
            if invalid == 1:
                print('Error: Invalid value')
            else:
                modify_flow(ip_p, switch)
                print('Modified ', ip_pro_str, ' to ', switch)
                print(' ')
                get_flow('1')
                print(' ')
                get_flow('5')
                print(' ')


    except KeyboardInterrupt as e:
        print(e)
