import threading

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import dpid as dpid_lib

'''
ryu-manager lab3ryu.py ryu.app.ofctl_rest
'''

def add_flow_mine(datapath, priority, match, actions, buffer_id=None):
    ofproto = datapath.ofproto
    parser = datapath.ofproto_parser

    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                         actions)]
    if buffer_id:
        mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                priority=priority, match=match, command=ofproto.OFPFC_ADD,
                                instructions=inst)
    else:
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, command=ofproto.OFPFC_ADD,
                                match=match, instructions=inst)
    datapath.send_msg(mod)
    print('add_flow_mine')


class L2Switch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(L2Switch, self).__init__(*args, **kwargs)

    # execute when get switch features
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def Switch_Features_handler(self, ev):
        global sumofs
        msg = ev.msg
        dp = msg.datapath
        dpid_str = dpid_lib.dpid_to_str(dp.id)
        dpid_int = int(dpid_str)
        ofproto = dp.ofproto
        parser = dp.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        print('new switch comes')
        add_flow_mine(dp, 0, match, actions)  # match nothing in flow table, send to control, priority=0
        print('added to controller')

        print('---------------------add flow for:', dpid_str, '---------------------')
        if dpid_int % 10 == 1:

            match = parser.OFPMatch(in_port=1, eth_type=0x0800, ip_proto=6)  # match: protocol = TCP
            actions = [parser.OFPActionOutput(2)]  # action: to port 2 (switch 2)
            add_flow_mine(dp, 1000, match, actions)  # add flow
            print('flow added: match=protocol is TCP, in_port=1 | action=to port 2')

            match = parser.OFPMatch(in_port=1, eth_type=0x0800, ip_proto=17)  # match: protocol = UDP
            actions = [parser.OFPActionOutput(3)]  # action: to port 3 (switch 3)
            add_flow_mine(dp, 1000, match, actions)  # add flow
            print('flow added: match=protocol is UDP, in_port=1 | action=to port 3')

            match = parser.OFPMatch(in_port=1)  # match: protocol not TCP or UDP
            actions = [parser.OFPActionOutput(4)]  # action: to port 4 (switch 4)
            add_flow_mine(dp, 100, match, actions)  # add flow
            print('flow added: match=protocol is not TCP or UDP, in_port=1 | action=to port 4')

            match = match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=('10.0.0.1', '255.255.255.255'))  # match: dst h1
            actions = [parser.OFPActionOutput(1)]  # action: to port 4 (switch 4)
            add_flow_mine(dp, 10, match, actions)  # add flow
            print('flow added: match=dst h1 | action=to port 1')

        elif dpid_int % 10 == 5:

            match = parser.OFPMatch(in_port=1, eth_type=0x0800, ip_proto=6)  # match: protocol = TCP
            actions = [parser.OFPActionOutput(2)]  # action: to port 2 (switch 2)
            add_flow_mine(dp, 1000, match, actions)  # add flow
            print('flow added: match=protocol is TCP, in_port=1 | action=to port 2')

            match = parser.OFPMatch(in_port=1, eth_type=0x0800, ip_proto=17)  # match: protocol = UDP
            actions = [parser.OFPActionOutput(3)]  # action: to port 3 (switch 3)
            add_flow_mine(dp, 1000, match, actions)  # add flow
            print('flow added: match=protocol is UDP, in_port=1 | action=to port 3')

            match = parser.OFPMatch(in_port=1)  # match: protocol not TCP or UDP
            actions = [parser.OFPActionOutput(4)]  # action: to port 4 (switch 4)
            add_flow_mine(dp, 100, match, actions)  # add flow
            print('flow added: match=protocol is not TCP or UDP, in_port=1 | action=to port 4')

            match = match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=('10.0.0.2', '255.255.255.255'))  # match: dst h2
            actions = [parser.OFPActionOutput(1)]  # action: to port 4 (switch 4)
            add_flow_mine(dp, 10, match, actions)  # add flow
            print('flow added: match=dst h2 | action=to port 1')

        else:
            match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=('10.0.0.1', '255.255.255.255'))  # match: dst h1
            actions = [parser.OFPActionOutput(1)]  # action: to port 1 (switch 1)
            add_flow_mine(dp, 100, match, actions)  # add flow
            print('flow added: match= dst h1 | action=to port 1')

            match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=('10.0.0.2', '255.255.255.255'))  # match: dst h2
            actions = [parser.OFPActionOutput(2)]  # action: to port 2 (switch 5)
            add_flow_mine(dp, 100, match, actions)  # add flow
            print('flow added: match= dst h2 | action=to port 2')

