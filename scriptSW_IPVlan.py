from netmiko import ConnectHandler
from getpass import getpass


print('Consulte a Tabela de Padronizacao de nomes.\n')
switch = str(input('Qual o ID do Switch(Com a numeracao) pela nova Topologia?'))
local = str(input('Em qual localizacao se encontra o switch?'))
rack = str(input('Em qual Rack se encontra o switch?'))
user = input('Qual o usuario? ')
password = print("Digite a Senha\n") + getpass()

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

for device in (swsaccess):
    setCfgSWA = ConnectHandler(**device)
    config_commands = ['hostname {}.{}.{}'.format(local).format(rack).format(switch),
                        #Acrescentar os comandos de SNMP Zabbix
                       'ip default-gateway 192.168.236.199',
                       'interface vlan 200',
                        'description IP de GERENCIAMENTO',
                        'ip address 192.168.236.{} 255.255.255.128'.format(''.join(filter(str.isdigit, switch)))
                    ]
    output = setCfgSWA.send_config_set(config_commands)
    output += setCfgSWA.save_config()
    print(output)
print('Fim do Script')    