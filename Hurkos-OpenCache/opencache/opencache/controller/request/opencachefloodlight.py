#!/usr/bin/env python2.7

"""opencachefloodlight.py - Sends JSON-RPC commands to the Floodlight controller."""

import opencache.lib.opencachelib as lib
import httplib
import json

TAG = 'request'

class Request:

    _config = None
    _controller = None

    def __init__(self, controller):
        """Initialise redirection instance with useful objects.

        Instantiated controller and configuration objects are passed for use within this instance.

        """
        self._controller = controller

    def stop(self):
        """Stop redirection object."""
        pass

    class StaticFlowEntryPusher:
        """Represents calls made to the Floodlight's Static Flowpusher API."""

        def __init__(self, host, port):
            """Initialise object with hostname and port of Floodlight controller."""
            self.host = host
            self.port = port

        def get(self, data):
            """Send HTTP GET request to Floodlight API."""
            ret = self._rest_call({}, 'GET')
            return json.loads(ret[2])

        def set(self, data):
            """Send HTTP POST request to Floodlight API."""
            ret = self._rest_call(data, 'POST')
            return ret[0] == 200

        def remove(self,data):
            """Send HTTP DELETE request to Floodlight API."""
            ret = self._rest_call(data, 'DELETE')
            return ret[0] == 200

        def _rest_call(self, data, action):
            """Send REST call to Floodlight controller's Static Flowpusher API."""
            path = '/wm/staticflowentrypusher/json'
            headers = {
                'Content-type': 'application/json',
                'Accept': 'application/json',
                }
            body = json.dumps(data)
            conn = httplib.HTTPConnection(self.host, self.port)
            conn.request(action, path, body, headers)
            response = conn.getresponse()
            ret = (response.status, response.reason, response.read())
            conn.close()
            return ret

    class Device:
        """Represents calls made to the Floodlight's Device API."""

        def __init__(self, host, port):
            """Initialise object with hostname and port of Floodlight controller."""
            self.host = host
            self.port = port

        def get(self, data):
            """Send HTTP GET request to Floodlight API."""
            ret = self._rest_call(data, 'GET')
            result = json.loads(ret[2])
            if result != []:
                try:
                    port = str(result[0]['attachmentPoint'][0]['port'])
                    dpid = str(result[0]['attachmentPoint'][0]['switchDPID'])
                    mac = str(result[0]['mac'][0])
                except IndexError:
                    raise
                try:
                    vlan = str(result[0]['vlan'][0])
                except:
                    vlan = '-1'
                return (port, dpid, mac, vlan)
            else:
                raise KeyError

        def _rest_call(self, data, action):
            """Send REST call to Floodlight controller's Device API."""
            path = '/wm/device/?ipv4=' + data
            conn = httplib.HTTPConnection(self.host, self.port)
            conn.request('GET', path)
            response = conn.getresponse()
            ret = (response.status, response.reason, response.read())
	    conn.close()
            return ret

    def add_redirect(self, expr, node_host, node_port, openflow_host, openflow_port, ovs_dpid, of_dpid, to_ovs, to_server, from_ovs, to_ocn, to_client):
        """Add a redirect for content requests matching given expression to a given node."""
        pusher = self.StaticFlowEntryPusher(openflow_host, openflow_port)
        device = self.Device(openflow_host, openflow_port)
	"""try:
            (_, connected_dpid, node_mac, node_vlan) = device.get(node_host)
        except KeyError:
            raise"""
	"""print "*******************************ovs_dpid:" + ovs_dpid
	print "*******************************of_dpid:" + of_dpid
	print "*******************************to_ovs:" + to_ovs
	print "*******************************to_server:" + to_server
	print "*******************************from_ovs:" + from_ovs
	print "*******************************to_ocn:" + to_ocn
	print "*******************************to_ocn:" + to_client"""
        modify_node_src_ovs = {
            "switch": ovs_dpid,
            "name":"modify_node_src_ovs-" + node_host + "-" + node_port + "-" + expr,
            "cookie":"0",
            "priority":"32766",
            "ether-type":"0x0800",
            "protocol":"0x06",
            "src-ip":node_host,
            "src-mac":"74:ea:3a:80:2c:0d",
            "src-port":node_port,
            "active":"true",
            "actions":"set-src-port=80,set-src-ip=" + expr + ",output=2"
        }
    	modify_server_dst_ovs = {
            "switch": ovs_dpid,
            "name":"modify_server_dst_ovs-" + node_host + "-" + node_port + "-" + expr,
            "priority":"32766",
            "ether-type":"0x0800",
            "protocol":"0x06",
            "dst-ip":expr,
            "dst-port":"80",
            "active":"true",        
            "actions":"set-dst-mac=74:ea:3a:80:2c:0d,set-dst-ip=" + node_host + ",set-dst-port=" + node_port +",output=2"
        }
        server_dst_go_ovs = {
            "switch": of_dpid,
            "name":"server_dst_go_ovs-" + node_host + "-" + node_port + "-" + expr,
            "priority":"1",
            "ether-type":"0x0800",
            "protocol":"0x06",
            "dst-ip":expr,
            "dst-port":"80",
            "active":"true",        
            "actions":"output=" + to_ovs
        }
        node_to_server = {
            "switch":  of_dpid,
            "name":"node_to_server-" + node_host + "-" + node_port + "-" + expr,
            "priority":"5",
            "ether-type":"0x0800",
            "protocol":"0x06",
            "src-ip":node_host,
            "dst-ip":expr,
            "dst-port":"80",
            "active":"true",        
            "actions":"output=" + to_server
        }
        node_src_go_ovs = {
            "switch": of_dpid,
            "name":"node_src_go_ovs-" + node_host + "-" + node_port + "-" + expr,
            "priority":"1",
            "ether-type":"0x0800",
            "protocol":"0x06",
            "src-ip":node_host,
            "active":"true",        
            "actions":"output=" + to_ovs
        }
        ovs_output_to_OCN = {
            "switch": of_dpid,
            "name":"ovs_output_to_OCN-" + node_host + "-" + node_port + "-" + expr,
            "priority":"1",
            "ether-type":"0x0800",
            "ingress-port": from_ovs,
            "dst-ip":node_host,
            "active":"true",        
            "actions":"output=" + to_ocn
        }
    	ovs_output_to_client = {
            "switch": of_dpid,
            "name":"ovs_output_to_client-" + node_host + "-" + node_port + "-" + expr,
            "priority":"1",
            "ether-type":"0x0800",
            "ingress-port": from_ovs,
            "src-ip":expr,
            "active":"true",        
            "actions":"output=" + to_client
        }
        pusher.remove({"name":"modify_node_src_ovs-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"modify_server_dst_ovs-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"server_dst_go_ovs-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"node_to_server-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"node_src_go_ovs-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"ovs_output_to_OCN-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"ovs_output_to_client-" + node_host + "-" + node_port + "-" + expr})
	pusher.set(modify_node_src_ovs)
	pusher.set(modify_server_dst_ovs)
	pusher.set(server_dst_go_ovs)
	pusher.set(node_to_server)
	pusher.set(node_src_go_ovs)
	pusher.set(ovs_output_to_OCN)
	pusher.set(ovs_output_to_client)
	
    def remove_redirect(self, expr, node_host, node_port, openflow_host, openflow_port, ovs_dpid, of_dpid, to_ovs, to_server, from_ovs, to_ocn, to_client):
        """Remove a redirect for content requests matching given expression to given node."""
        pusher = self.StaticFlowEntryPusher(openflow_host, openflow_port)
        pusher.remove({"name":"modify_node_src_ovs-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"modify_server_dst_ovs-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"server_dst_go_ovs-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"node_to_server-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"node_src_go_ovs-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"ovs_output_to_OCN-" + node_host + "-" + node_port + "-" + expr})
	pusher.remove({"name":"ovs_output_to_client-" + node_host + "-" + node_port + "-" + expr})
