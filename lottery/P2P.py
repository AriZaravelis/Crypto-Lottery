from p2pnetwork.node import Node
#We got this package from: https://github.com/macsnoeren/python-p2p-network/tree/dfb68533df63d281a48e8ec531843f133f947ee7


class P2P(Node):

    def __init__(self, host, port, var):
        super(P2P, self).__init__(host, port, var)
        print(var,": Started")

    def outbound_node_connected(self, node):
        return node.id

    def outbound_node_disconnected(self, node):
        return node.id
        
    def inbound_node_connected(self, node):
        return node.id

    def inbound_node_disconnected(self, node):
        return node.id

    def node_message(self, node, data):
        print("node_message from " + node.id + ": " + str(data) + "\n")
   
    def node_disconnect_with_outbound_node(self, node):
        return node.id
        
    def node_request_to_stop(self):
        print("node is requested to stop!")