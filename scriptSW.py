from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint

global user, password, stp_netsw

def swDIST_stp (vlanx):
    global config_commands
    config_commands = ['spanning-tree mode rapid-stp','spanning-tree vlan {} priority 12288'.format(vlanx)]
    return config_commands

def swACCESS_stp (vlanx):
    global config_commands
    config_commands = ["spanning-tree vlan {} priority 24576".format(vlanx), "spanning-tree mode rapid-stp"]
    return config_commands

def connSWVerVlan(device):
    global stp_netsw
    stp_netsw = ConnectHandler(**device)
    #comandos para verificacao da vlan 
    see_vlan_command = "show vlan brief"
    out1 = stp_netsw.send_command(see_vlan_command, use_txtfsm=True)
    return out1

def vlanExist(out1):
    # Verificar se a variavel vlanx esta presente em algum campo 'vlan'  
    global vlan_encontrada
    vlan_encontrada = any(vlan['vlan'] == str(vlanx) for vlan in out1)
    return vlan_encontrada

def setConfigDist():
    swDIST_stp(vlanx)
    for device in (swsditributions):
        out1 = connSWVerVlan(device)
        vlan_encontrada = vlanExist(out1)
        if vlan_encontrada:
            output = stp_netsw.send_config_set(config_commands)
            output += stp_netsw.save_config()
            print(output)
        else:
            stp_netsw.disconnect()
            continue

def setConfigAcc():
    swACCESS_stp(vlanx)
    for device in (swsaccess):
        out1 = connSWVerVlan(device)
        vlan_encontrada = vlanExist(out1)
        if vlan_encontrada:
            output = stp_netsw.send_config_set(config_commands)
            output += stp_netsw.save_config()
            print(output)
        else:
            stp_netsw.disconnect()
            continue

switch = input('O switch e de distribuicao ou de acesso?')
user = input('Qual o usuario? ')
password = print("Digite a Senha\n") + getpass()
vlanx = int(input('Qual a vlan?'))
prior = int(input('Qual a prioridade?'))

swsditributions = [
#    SWD203 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.203',
        'username': user,
        'password': password
    },
#    SWD204 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.204',
        'username': user,
        'password': password
    },
#    SWD205 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.205',
        'username': user,
        'password': password
    },
#    SWD206 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.206',
        'username': user,
        'password': password
    }
]
#Esse script vai utilizar o enderecamento de antes da migracao.
# Apos a migracao TEM QUE SER ATUALIZADO
swsaccess = [
    #SWA201 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.201',
        'username': user,
        'password': password
    },
    #SW236 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.236',
        'username': user,
        'password': password
    },
    #SWA192 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.192',
        'username': user,
        'password': password
    },
    #SWA221 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.221',
        'username': user,
        'password': password
    },
    #SWA211 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.211',
        'username': user,
        'password': password
    },
    #SWA220 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.220',
        'username': user,
        'password': password
    },
    #SWA224 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.224',
        'username': user,
        'password': password
    },
    #SWA216 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.216',
        'username': user,
        'password': password
    },
    #SWA207 = 
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.236.207',
        'username': user,
        'password': password
    }
]

if switch[0].lower() == 'd':
    setConfigDist()
elif switch[0].lower() == 'a':
    setConfigAcc()
        
    

