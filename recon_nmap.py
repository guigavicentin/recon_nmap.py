import argparse
import os
import subprocess
import sys

# Função para validar se o domínio é válido (possui IP)
def validar_dominio(dominio):
    try:
        resultado = subprocess.check_output(['host', dominio], stderr=subprocess.STDOUT).decode()
        if "has address" in resultado:
            ips = [linha.split()[-1] for linha in resultado.splitlines() if "has address" in linha]
            return ips
        return []
    except subprocess.CalledProcessError:
        return []

# Função para executar Amass e salvar a saída
def executar_amass(dominio, diretorio):
    amass_output = os.path.join(diretorio, f"{dominio}_amass.txt")
    subprocess.run(['amass', 'enum', '-d', dominio, '-o', amass_output], check=True)
    return amass_output

# Função para ler domínios do arquivo de saída do Amass e validar
def validar_ips_amass(amass_output):
    ips_validos = set()
    with open(amass_output, 'r') as f:
        dominios = f.read().splitlines()
        for dominio in dominios:
            ips = validar_dominio(dominio)
            ips_validos.update(ips)
    return list(ips_validos)

# Função para executar Nmap com a lista de IPs
def executar_nmap(nmap_opcao, arquivo_ips, output_file):
    nmap_opcoes = {
        '1': ['-sS', '-Pn', '-p-'],
        '2': ['-sP', '-p-'],
        '3': ['-sS', '-f', '-p-'],
        '4': ['-sS', '-D', 'RND:10', '-p-'],
        '5': ['-sS', '-g', '53', '-p-'],
        '6': ['-sS', '-T2', '-p-'],
        '7': ['-sS', '-p-', '--script', 'firewall-bypass'],
        '8': ['-sS', '-Pn', '-D', 'RND:10', '-p-', '-f'],
        '9': ['-p-', '-sV'],
        '10': ['-sC', '-sV', '-p-'],
        '11': ['-sV'],
        '12': ['-sC', '-sV'],
        '13': [],
        '14': ['-p22,21,5432,80,8080'],
        '15': ['-sU']
    }

    if nmap_opcao not in nmap_opcoes:
        print("Opção de Nmap inválida!")
        sys.exit(1)

    comando_nmap = ['nmap', '-iL', arquivo_ips] + nmap_opcoes[nmap_opcao]
    with open(output_file, 'w') as saida:
        subprocess.run(comando_nmap, stdout=saida)

# Função principal
def main():
    parser = argparse.ArgumentParser(description="Script de Recon com Nmap e Amass")
    
    parser.add_argument('-u', required=True, help="Domínio alvo")
    parser.add_argument('-d', default='.', help="Diretório para salvar os arquivos (padrão: diretório atual)")
    parser.add_argument('-o', default=None, help="Arquivo de saída do Nmap (padrão: target.txt)")
    parser.add_argument('-n', required=True, help="Opção do Nmap (1 a 15)")

    args = parser.parse_args()

    # Criar diretório se não existir
    if not os.path.exists(args.d):
        os.makedirs(args.d)

    # Nome do arquivo de saída
    output_file = args.o if args.o else os.path.join(args.d, f"{args.u}.txt")

    # Executar Amass e verificar se o domínio é válido
    amass_output = executar_amass(args.u, args.d)

    # Validar os IPs dos domínios gerados pelo Amass
    ips_validos = validar_ips_amass(amass_output)

    if not ips_validos:
        print(f"Domínio {args.u} não possui IPs válidos.")
        sys.exit(1)

    # Remover IPs duplicados
    ips_unicos = list(set(ips_validos))

    # Salvar os IPs encontrados em um arquivo
    arquivo_ips = os.path.join(args.d, f"{args.u}_ips.txt")
    with open(arquivo_ips, 'w') as f:
        for ip in ips_unicos:
            f.write(ip + '\n')

    # Executar Nmap
    executar_nmap(args.n, arquivo_ips, output_file)
    print(f"Resultado salvo em: {output_file}")

if __name__ == '__main__':
    main()
