#!/bin/bash
# Ativa o modo seguro: para o script se qualquer comando falhar
set -e

# Função para exibir mensagens no terminal
log(){
    echo -e "\n========= $1 ==========\n"
}

# Verificar se o script está sendo executado como root
if [ "$(id -u)" -ne 0 ]; then
    echo "Este script deve ser executado como root."
    exit 1
fi

log "Atualizando repositórios e pacotes"
apt-get update && apt-get upgrade -y

# Definindo Lista de pacotes
packages=("vim" "net-tools" "htop" "debian-goodies" "tcptraceroute" "mtr" "nmon" "lynis" "debsecan" "unzip" "ca-certificates" "curl" "gnupg")

# Loop para instalar lista de pacotes
for pkg in "${packages[@]}"; do
    if ! dpkg -l | grep -qw "$pkg"; then
        log "Instalando o $pkg..."
        apt-get install "$pkg" -y
    else
        log "O pacote $pkg já está instalado, ignorando."
    fi
done

# Instalação do Docker Engine
log "Preparando para instalar o Docker Engine"

# Adicionar a Chage GPG Oficial do Docker
log "Adicionando a chave GPG oficial do Docker"
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar o repositório do docker
log "Configurando o repositório do Docker"
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Atualizar o indice de pacotes APT
log "Atualizando índice de pacotes APT com o novo repositório do Docker"
apt-get update

# Instalar o Docker Engine, containerd e Docker Compose (plugin)
log "Instalando Docker Engine, containerd e Docker Compose (plugin)"
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Verificar o status do Docker
log "Verificando o status do serviço Docker"
systemctl status docker --no-pager || true # O '|| true' evita que o script pare se o serviço não estiver totalmente ativo ainda

# Habilitar o Docker para iniciar no boot
log "Habilitando o Docker para iniciar no boot"
systemctl enable docker

# Adicionar o usuário atual (se não for root) ao grupo docker para executar comandos sem sudo
# O 'logname' pega o nome do usuário logado na sessão atual. 'SUDO_USER' pode ser usado, mas é menos confiável se o usuário troca de contexto.
# Vamos pegar o usuário que EXECUTOU o `sudo` ou o `su` para rodar este script.
# Se o script está sendo executado como root diretamente, a variável $SUDO_USER pode estar vazia.
# Usaremos 'who am i | awk '{print $1}'' que geralmente funciona para o usuário que iniciou a sessão.
# Mas como estamos num script que é 'sudo', o $SUDO_USER é mais apropriado para o usuário "real".
# Se $SUDO_USER estiver vazio, vamos usar quem_sou_eu
if [ -n "${SUDO_USER:-}" ]; then
    CURRENT_USER="$SUDO_USER"
else
    # Se o script foi executado diretamente como root, não haverá SUDO_USER
    # Tenta obter o usuário logado de outras formas
    CURRENT_USER=$(who am i | awk '{print $1}' 2>/dev/null || echo "root")
fi

if [ "$CURRENT_USER" != "root" ]; then
    log "Adicionando o usuário '$CURRENT_USER' ao grupo 'docker'"
    usermod -aG docker "$CURRENT_USER"
    log "Por favor, faça logout e login novamente (ou reinicie o terminal) para que as permissões do grupo 'docker' sejam aplicadas ao '$CURRENT_USER'."
else   
    log "Script executado como root. Nenhuma alteração de grupo para usuários comuns é necessária."
fi

log "Instalação do Docker Engine e Docker Compose concluída com Sucesso!"