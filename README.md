# 🖥️ On-Premises Automation & Systems Hardening

Bem-vindo ao repositório centralizado de **Automação de Sistemas e Infraestrutura Local**.

Este workspace é dedicado ao desenvolvimento de ferramentas, scripts de gerenciamento de sistemas operacionais, orquestração de serviços locais (on-premises), monitoramento e mitigação automatizada de vulnerabilidades em servidores Linux.

---

## 🧭 Filosofia de Organização do Código

Para mantermos a máxima coesão e responsabilidade única de nossos repositórios, a nossa infraestrutura foi estruturalmente modularizada:

*   **Este Repositório (`OnPremissesAutomation`):** Focado exclusivamente em automação ao nível de sistema operacional (OS), servidores físicos/virtuais (hipervisores como Proxmox e XCP-ng), hardening de segurança e serviços internos (Zabbix, NTP, TACACS+, WWW).
*   **Repositório de Redes (`InfrastructureTImigration-and-Improve`):** Centraliza todos os scripts de configuração e migração de switches ativos e dispositivos de rede Cisco (gerenciados via Netmiko e TextFSM).

---

## 📁 Estrutura dos Projetos Atuais

### 1. 🛡️ [`config_ssh_svrs/`](file:///home/eliezerpires/OnPremissesAutomation/config_ssh_svrs/) (Hardening SSH contra CVE-2024-6387)
Uma solução robusta e automatizada em Python (`gvulsshd.py`) que realiza a varredura, validação de versões vulneráveis do OpenSSH (regreSSHion) e aplicação remota e segura da diretiva recomendada de segurança (`LoginGraceTime 0`) em larga escala.
*   **Mitigação Centralizada:** Usa SFTP e elevação de privilégios (`su`) interativa.
*   **Auditoria Integrada:** Aguarda o reinício do serviço SSH, confirma a restauração da conectividade e inspeciona se a alteração foi aplicada com sucesso no arquivo `/etc/ssh/sshd_config` do servidor de destino.
*   Para mais detalhes de arquitetura e uso, consulte o [README interno do projeto](file:///home/eliezerpires/OnPremissesAutomation/config_ssh_svrs/README.md).

### 🚀 [`initservers.sh`](file:///home/eliezerpires/OnPremissesAutomation/initservers.sh)
Script utilitário em Shell para provisionamento e inicialização rápida de novos servidores no ambiente local, automatizando parametrizações de pacotes, configurações de base e políticas locais iniciais.

---

## 📈 Planos Futuros e Evolução

Estamos constantemente evoluindo e aprimorando nossas rotinas operacionais locais:
*   Integração com ferramentas de automação e orquestração de infraestrutura como código (IaC).
*   Expansão de scripts de hardening de segurança baseados no CIS Benchmark para Linux.
*   Automação de rotinas de backup local de bases de dados críticas (InfluxDB, Netbox, Zabbix).
