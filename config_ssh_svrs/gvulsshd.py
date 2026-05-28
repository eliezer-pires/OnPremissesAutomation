import paramiko
import getpass
import json
import re
import os
import time


# Carrega o arquivo de servidores
def load_serverjson(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Carrega o arquivo de comandos  
def load_cmds(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

# Faz a conexão ssh e executa os comandos
def execute_ssh_command(host, port, username, password, commands, get_pty=False):
    try:
        # Tenta a conexão inicial
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conecta ao servidor
        client.connect(hostname=host, port=port, username=username, password=password)
    except paramiko.ssh_exception.SSHException as e:
        error_message = str(e)
        if "no matching host key type found" in error_message:
            # Extrai os algoritmos de chave oferecidos
            offerred_keys = error_message.split("Their offer: ")[-1]
            offerred_keys = offerred_keys.strip()
            # Configura para usar os algoritmos oferecidos
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, port=port, username=username, password=password, disabled_algorithms={'keys': offerred_keys.split(',')})
        elif "no matching cipher found" in error_message:
            offerred_ciphers = error_message.split("Their offer: ")[-1]
            offerred_ciphers = offerred_ciphers.strip()
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, port=port, username=username, password=password, disabled_algorithms={'ciphers': offerred_ciphers.split(',')})
        else:
            return [(None, str(e), None)]
        # Executa os comandos se a conexão for bem-sucedida
    try:
        results = []
        for command in commands:
            stdin, stdout, stderr = client.exec_command(command, get_pty=get_pty)
            # Captura a saída
            output = stdout.read().decode()
            error = stderr.read().decode()
            results.append((command, output, error))
        return results
    except Exception as e:
        return [(None, str(e), None)]
    finally:
        client.close()
# Função para dividir a versão em partes
def div_version(version):
    match = re.match(r'(\d+)\.(\d+)([a-z])(\d+)', version)
    if not match:
        return None, None, None, None
    return int(match.group(1)), int(match.group(2)), match.group(3), int(match.group(4))

# Condições para verificar a versão
def version_valid(version):
    if version is None:
        return False
    first, second, letra, ultmo = div_version(version)
    # Verificar se a versão é anterior a 4.4p1
    if (first < 4) or (first == 4 and second < 4) or (first == 4 and second == 4 and letra <'p') or (first == 4 and second == 4 and letra == 'p' and ultmo < 1):
        return True
    # Verificar se a versão é a partir de 8.5p1, exceto 9.8p1
    if (first > 8 or (first == 8 and second >= 5)) and not (first == 9 and second == 8 and letra == 'p' and ultmo == 1):
            return True
    return False

def wait_for_ssh(host, port, username, password, timeout=120):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, port=port, username=username, password=password)
            client.close()
            return True
        except Exception as e:
            time.sleep(5)
    return False

print("Este Script vai fazer conexões remotas de uma lista de servidores.\nE executar comandos contidos no arquivo grimorio.\n")

# Carregar a lista de servidores e comandos dos arquivos JSON
servers = load_serverjson('svrs.json')
add_commands = load_cmds('grimorio')

for server in servers:
    # Solicita a senha do usuário
    username = server["username"]
    comentario = server["_comentario"]
    print(f"Conectando ao {comentario}.\n")
    hotdog = getpass.getpass(prompt=f'Enter SSH password para o Usuário {username}: ')   
    hootdog = getpass.getpass(prompt=f'Enter root password: ')
    results = execute_ssh_command(server["host"], server["port"], server["username"], hotdog, [server["command"]])
    for command, output, error in results:
        print(f"Output do {server['host']} (Comando: {command}):\n{output}")
        # Define o padrão de busca
        pattern = r'\b[0-9]\.[0-9][a-z][0-9]\b'
        match = re.search(pattern, output)
        if match:
            version = match.group(0)
            print("Versao encontrada:", version)
            # Verifica a condição da função se True executa comandos e mostra as saídas
            if version_valid(version):
                # Cria um script temporário com os comandos adicionais
                script_content = "\n".join(add_commands)
                local_script = "/tmp/temp_script.sh"
                with open (local_script, 'w') as file:
                    file.write(script_content)
                # Copia o script temporário para o servidor remoto
                transport = paramiko.Transport((server["host"], server["port"]))
                transport.connect(username=username, password=hotdog)
                sftp = paramiko.SFTPClient.from_transport(transport)
                remote_script = "/tmp/temp_script.sh"
                sftp.put(local_script, remote_script)
                sftp.close()
                transport.close()
                # Executa o script temporário com su no servidor remoto
                su_command = f'echo "{hootdog}" | su -c "sh {remote_script}"'
                cmd_to_display = su_command.split('|', 1)[-1].strip()
                add_results = execute_ssh_command(server["host"], server["port"], server["username"], hotdog, [su_command], get_pty=True)
                # Remove o script temporário local
                os.remove(local_script)

                for add_cmd, add_output, add_error in add_results:
                    if add_cmd is not None:
                        print(f"Saída do {server['host']} (Comando adicional: {cmd_to_display}):\n{add_output}")
                        if add_error:
                            print(f"Erro do {server['host']} (Comando adicional: {cmd_to_display}):\n{add_error}")
                
                # Verifica se a conexão foi perdida e tenta reconectar
                if "systemctl restart ssh" in add_commands:
                    print(f"Aguardando reinício do serviço SSH no {server['host']}...")
                    if wait_for_ssh(server["host"], server["port"], server["username"], hotdog):
                        print(f"Conexão restabelecida com {server['host']}.")
                        #Executa o comando para verificar se a alteração foi realizada 
                        verify_command = 'cat /etc/ssh/sshd_config | grep LoginGraceTime'
                        verify_results = execute_ssh_command(server["host"], server["port"], server["username"], hotdog, [verify_command])
                        for verify_cmd, verify_output, verify_error in verify_results:
                            print(f"Verificação de {server['host']} (Comando: {verify_cmd}):\n{verify_output}")
                            if verify_error:
                                print(f"Erro de verificação em {server['host']} Comando: {verify_cmd}):\n{verify_error}")
                        # Remove o script temporário no servidor remoto
                        execute_ssh_command(server["host"], server["port"], server["username"], hotdog, [f'rm {remote_script}'])
                    else:
                        print(f"Falha ao restabelecer conexão com {server['host']}.")
                else:
                    print(f"Erro de autenticação no servidor {server['host']}")
        else:            
            print("Versao nao encontrada.")
            version = None
        if error:
            print(f"Erro do {server['host']} (Comando: {command}):\n{error}")