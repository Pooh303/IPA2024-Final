from ncclient import manager
import xmltodict

m = manager.connect(
    host="10.0.15.183",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

def create(name):
    netconf_config = f"""
        <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
        <Loopback>
            <name>{name}</name>
            <description>Loopback{name}</description>
            <ip>
            <address>
            <primary>
            <address>172.30.182.1</address>
            <mask>255.255.255.0</mask>
            </primary>
            </address>
            </ip>
        </Loopback>
        </interface>
        </native>
        </config>
        """

    if status(name) == f"Interface Loopback {name} is enabled" or status(name) == f"Interface Loopback {name} is disabled":
        return f"Cannot create: Interface loopback {name}"
    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        # print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {name} is created successfully"
    except Exception as e:
        return f"An error occurred: {e}"
    
    # try:
    #     netconf_reply = netconf_edit_config(netconf_config)
    #     xml_data = netconf_reply.xml
    #     print(xml_data)
    #     if '<ok/>' in xml_data:
    #         return "<!!!REPLACEME with proper message!!!>"
    # except:
    #     print("Error!")


def delete(name):
    netconf_config = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="delete">
                <name>Loopback{name}</name>
            </interface>
        </interfaces>
    </config>
    """

    if status(name) != f"Interface Loopback {name} is enabled" and status(name) != f"Interface Loopback {name} is disabled":
        return f"Cannot delete: Interface loopback {name}"
    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        # print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {name} is deleted successfully"
    except Exception as e:
        return f"An error occurred: {e}"
    
    # try:
    #     netconf_reply = netconf_edit_config(netconf_config)
    #     xml_data = netconf_reply.xml
    #     print(xml_data)
    #     if '<ok/>' in xml_data:
    #         return "<!!!REPLACEME with proper message!!!>"
    # except:
    #     print("Error!")


def enable(name):
    netconf_config = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback{name}</name>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
    """

    if status(name) != f"Interface Loopback {name} is enabled" and status(name) != f"Interface Loopback {name} is disabled":
        return f"Cannot delete: Interface loopback {name}"
    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        # print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {name} is enabled successfully"
    except Exception as e:
        return f"An error occurred: {e}"
    
    # try:
    #     netconf_reply = netconf_edit_config(netconf_config)
    #     xml_data = netconf_reply.xml
    #     print(xml_data)
    #     if '<ok/>' in xml_data:
    #         return "<!!!REPLACEME with proper message!!!>"
    # except:
    #     print("Error!")


def disable(name):
    netconf_config = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback{name}</name>
                <enabled>false</enabled>
            </interface>
        </interfaces>
    </config>
    """

    if status(name) != f"Interface Loopback {name} is enabled" and status(name) != f"Interface Loopback {name} is disabled":
        return f"Cannot delete: Interface loopback {name}"
    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        # print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {name} is shutdowned successfully"
    except Exception as e:
        return f"An error occurred: {e}"
    
    # try:
    #     netconf_reply = netconf_edit_config(netconf_config)
    #     xml_data = netconf_reply.xml
    #     print(xml_data)
    #     if '<ok/>' in xml_data:
    #         return "<!!!REPLACEME with proper message!!!>"
    # except:
    #     print("Error!")

def netconf_edit_config(netconf_config):
    return m.edit_config(target="running", config=netconf_config)

def status(name):
    netconf_filter = f"""
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback{name}</name>
            </interface>
        </interfaces-state>
    </filter>
    """

    try:
        # Use the 'get' operation to fetch the status of the interface
        netconf_reply = m.get(filter=netconf_filter)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
        data = netconf_reply_dict.get('rpc-reply', {}).get('data', {})
        interfaces_state = ""

        # Check if the interface status is present
        if data :
            interfaces_state = data.get('interfaces-state')

        # print(interfaces_state)
            
        if 'interface' in interfaces_state:
            interface = interfaces_state['interface']
            admin_status = interface.get('admin-status')
            oper_status = interface.get('oper-status')
            
            # print(admin_status, oper_status)

            if admin_status == 'up' and oper_status == 'up':
                return f"Interface Loopback {name} is enabled"
            elif admin_status == 'down' and oper_status == 'down':
                return f"Interface Loopback {name} is disabled"
            else:
                return f"Interface Loopback {name} has inconsistent states."
        else:
            return f"No Interface Loopback {name}"

    except Exception as e:     
        return f"An error occurred: {e}"
    # try:
    #     # Use Netconf operational operation to get interfaces-state information
    #     netconf_reply = m.<!!!REPLACEME with the proper Netconf operation!!!>(filter=<!!!REPLACEME with netconf_filter!!!>)
    #     print(netconf_reply)
    #     netconf_reply_dict = xmltodict.<!!!REPLACEME with the proper method!!!>(netconf_reply.xml)

    #     # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
    #     if <!!!REPLACEME with the proper condition!!!>:
    #         # extract admin_status and oper_status from netconf_reply_dict
    #         admin_status = <!!!REPLACEME!!!>
    #         oper_status = <!!!REPLACEME !!!>
    #         if admin_status == 'up' and oper_status == 'up':
    #             return "<!!!REPLACEME with proper message!!!>"
    #         elif admin_status == 'down' and oper_status == 'down':
    #             return "<!!!REPLACEME with proper message!!!>"
    #     else: # no operation-state data
    #         return "<!!!REPLACEME with proper message!!!>"
    # except:
    #    print("Error!")
