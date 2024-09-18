Recon Nmap Script
Este script, recon_nmap.py, é uma ferramenta de automação de reconhecimento que combina a funcionalidade das ferramentas Amass e Nmap para realizar varreduras em domínios, capturar IPs e realizar uma análise detalhada das portas e serviços abertos.

Funcionalidades
Amass Enumeration:
A ferramenta inicia fazendo uma enumeração de subdomínios com o Amass.
Todos os subdomínios encontrados são salvos em um arquivo.

Validação de Domínio:
Após a enumeração, o script valida se o domínio é válido (verifica se possui IPs públicos associados).
Caso o domínio seja válido, os IPs correspondentes são extraídos e salvos em um arquivo separado.

Varredura com Nmap:
O Nmap é então executado em todos os IPs válidos encontrados, utilizando uma das 15 opções de varredura especificadas pelo usuário.
O resultado da varredura é salvo em um arquivo de saída que pode ser especificado ou gerado automaticamente.

Como usar
Argumentos
O script aceita os seguintes argumentos de linha de comando:

-u (obrigatório): O domínio alvo para o reconhecimento.
-d (opcional): Diretório onde os resultados serão salvos. Se não especificado, o diretório atual será usado.
-o (opcional): Arquivo de saída para salvar o resultado da varredura Nmap. Se não informado, será gerado um arquivo com o nome do domínio.
-n (obrigatório): Seleção do tipo de varredura Nmap a ser realizada. O usuário pode escolher entre 15 opções pré-definidas.
Opções de Varredura Nmap
O argumento -n determina a varredura do Nmap que será realizada. As opções são:

-sS -Pn -p-: TCP SYN Scan em todas as portas, ignorando hosts não acessíveis.
-sP -p-: Ping Scan em todas as portas.
-sS -f -p-: TCP SYN Scan com fragmentação de pacotes.
-sS -D RND:10 -p-: TCP SYN Scan com 10 endereços de IP falsos.
-sS -g 53 -p-: TCP SYN Scan, fingindo ser uma solicitação de DNS (porta 53).
-sS -T2 -p-: TCP SYN Scan com timing lento (T2).
-sS -p- --script firewall-bypass: TCP SYN Scan com script para bypass de firewall.
-sS -Pn -D RND:10 -p- -f: TCP SYN Scan com 10 IPs falsos, ignorando hosts inacessíveis e com fragmentação.
-p- -sV: Varredura de portas e detecção de versões.
-sC -sV -p-: Varredura com scripts padrão e detecção de versões.
-sV: Detecção de versões de serviços.
-sC -sV: Varredura com scripts padrão e detecção de versões.
nmap: Varredura padrão.
-p22,21,5432,80,8080: Varredura de portas específicas (SSH, FTP, PostgreSQL, HTTP e HTTP alternativo).
-sU: Varredura UDP.
Exemplo de Uso
python3 recon_nmap.py -u example.com -d /path/to/directory -o result.txt -n 1
Neste exemplo, o script fará uma varredura TCP SYN Scan em todas as portas do domínio example.com, salvará os IPs válidos e o resultado do Nmap no arquivo result.txt no diretório especificado.

Ajuda
Para exibir a ajuda com detalhes sobre como usar o script:
python3 recon_nmap.py --help
Esse código é útil para pentesters e pesquisadores de segurança que buscam automatizar o processo de reconhecimento de subdomínios, coleta de IPs e varredura de portas e serviços usando Amass e Nmap. O script é flexível, permitindo a customização de varreduras e a organização de saídas em diretórios e arquivos, facilitando o gerenciamento de grandes volumes de dados durante a fase de reconhecimento.
