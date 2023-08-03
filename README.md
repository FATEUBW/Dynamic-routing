# Dynamic-routing
2023 T2 TELE4642 Lab3 Group4
Check list:
Ubuntu system.
The version of python is 3.8.
Have installed ryu.
Have installed mininet.
Have installed wire shark(optional).

First, generate the topo by typing in the terminal: "mn --custom lab3topo.py --topo mytopo --controller=remote,ip=127.0.0.1,port=6653 --switch ovs,protocols=OpenFlow13 --arp --mac". 

Then, start the ryu controller by typing in the terminal: "ryu-manager lab3ryu.py ryu.app.ofctl_rest".

Finally run lab3RESTapp.py by "python3 lab3RESTapp.py" to change the route table.
