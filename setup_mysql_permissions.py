#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para auto configurar permissões do MySQL com base no IP real da máquina.
Isso resolve o erro "Host 'X.X.X.X' is not allowed to connect".

Configura:
  - o usuário 'sicol'@'<ip>' com acesso às bases da aplicação;
  - o usuário 'root'@'<ip>' com ALL PRIVILEGES ON *.* WITH GRANT OPTION, para que o
    root também possa conectar/administrar a partir do IP da máquina (caso em que o
    root só estava autorizado em 'localhost').

Autor: microSICol Setup
Uso: python3 setup_mysql_permissions.py
"""

import socket
import mysql.connector as mysql
from sys import exit


class MySQLPermissionSetup:
    """Configura as permissões MySQL na máquina com o IP real para os usuários sicol e root"""

    def __init__(self):
        self.local_ip = self.get_local_ip()
        self.mysql_root_user = 'root'
        self.mysql_root_password = None
        self.sicol_user = 'sicol'
        self.sicol_password = 'sicol'
        self.databases = ['sicol_v110', 'sicol_v110_log']

    def get_local_ip(self):
        """Pega o endereço IP real da máquina, mesmo em ambientes com NAT ou múltiplas interfaces"""
        try:
            # Conecta a um socket UDP externo para detectar o IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            # Fallback
            return socket.gethostbyname(socket.gethostname())

    def get_mysql_root_password(self):
        """Solicita a senha do usuário root do MySQL"""
        import getpass
        password = getpass.getpass(
            f"Digite a senha do MySQL para o usuário '{self.mysql_root_user}' (ou pressione Enter se não houver): "
        )
        return password

    def connect_as_root(self):
        """Conecta ao MySQL como usuário root"""
        # Primeira tentativa: conecta sem senha (autenticação unix_socket)
        try:
            print("🔄 Tentando conectar como root (sem senha)...")
            connection = mysql.connect(
                host='localhost',
                user=self.mysql_root_user,
                password='',
                port=3306,
                use_unicode=True,
                charset='utf8'
            )
            print("✅ Conectado como root (usando autenticação unix_socket)")
            return connection
        except mysql.Error as e:
            # 1045 = acesso negado por senha; 1698 = root configurado com auth via
            # unix_socket (precisa rodar com 'sudo'). Em ambos tentamos com senha.
            if e.args[0] in (1045, 1698):
                if e.args[0] == 1698:
                    print("⚠️  O root usa autenticação via socket (unix_socket).")
                    print("   Dica: rode com elevação -> sudo python3 setup_mysql_permissions.py")
                else:
                    print("⚠️  Autenticação sem senha falhou, solicitando senha...")
                self.mysql_root_password = self.get_mysql_root_password()
                try:
                    connection = mysql.connect(
                        host='localhost',
                        user=self.mysql_root_user,
                        password=self.mysql_root_password,
                        port=3306,
                        use_unicode=True,
                        charset='utf8'
                    )
                    print("✅ Conectado como root (usando autenticação por senha)")
                    return connection
                except mysql.Error as e2:
                    print(f"❌ Erro ao conectar com senha: {e2.args[0]}: {e2.args[1]}")
                    if e2.args[0] == 1698:
                        print("   O root só aceita conexão via socket: rode 'sudo python3 setup_mysql_permissions.py'.")
                    else:
                        print("   Verifique sua senha do root do MySQL.")
                    exit(1)
            else:
                print(f"❌ Erro ao conectar ao MySQL como root: {e.args[0]}: {e.args[1]}")
                exit(1)

    def configure_permissions(self):
        """Configura as permissões do MySQL para o usuário sicol"""
        print("\n" + "="*70)
        print("Configuração de Permissões MySQL para microSICol")
        print("="*70)
        print(f"IP da máquina detectado: {self.local_ip}")
        print(f"Usuário sicol a configurar: {self.sicol_user}")
        print(f"Bases de dados: {', '.join(self.databases)}")
        print("="*70 + "\n")

        # Conecta como root
        print("🔄 Conectando ao MySQL como root...")
        connection = self.connect_as_root()
        cursor = connection.cursor()

        try:
            # Verifica se o usuário já existe para este IP
            user_exists_query = (
                f"SELECT user FROM mysql.user WHERE user='{self.sicol_user}' AND host='{self.local_ip}'"
            )
            cursor.execute(user_exists_query)
            user_exists = cursor.fetchone()

            # Se o usuário não existe, cria
            if not user_exists:
                print(f"\n⏳ Criando usuário {self.sicol_user}@{self.local_ip}...")
                create_user_sql = (
                    f"CREATE USER `{self.sicol_user}`@'{self.local_ip}' "
                    f"IDENTIFIED BY '{self.sicol_password}'"
                )
                print(f"   SQL: {create_user_sql}")
                cursor.execute(create_user_sql)
                print(f"   ✅ Usuário criado com sucesso")
            else:
                print(f"\n✅ Usuário {self.sicol_user}@{self.local_ip} já existe")

            # Concede permissões para o IP detectado
            for db in self.databases:
                sql = (
                    f"GRANT ALL PRIVILEGES ON `{db}`.* "
                    f"TO `{self.sicol_user}`@'{self.local_ip}'"
                )
                print(f"\n⏳ Concedendo permissões na base {db}...")
                print(f"   SQL: {sql}")
                cursor.execute(sql)
                print(f"   ✅ Permissão concedida para {self.sicol_user}@{self.local_ip}")

            # Garante que o root também conecte/administre a partir do IP da máquina
            # (resolve casos em que o root só está autorizado em 'localhost').
            cursor.execute(
                f"SELECT user FROM mysql.user "
                f"WHERE user='{self.mysql_root_user}' AND host='{self.local_ip}'"
            )
            if not cursor.fetchone():
                # '' quando o root atual conecta via unix_socket (sem senha)
                root_pwd = self.mysql_root_password or ''
                create_root_sql = (
                    f"CREATE USER `{self.mysql_root_user}`@'{self.local_ip}' "
                    f"IDENTIFIED BY '{root_pwd}'"
                )
                print(f"\n⏳ Criando usuário {self.mysql_root_user}@{self.local_ip}...")
                print(f"   SQL: CREATE USER `{self.mysql_root_user}`@'{self.local_ip}' IDENTIFIED BY '***'")
                cursor.execute(create_root_sql)
                print(f"   ✅ Usuário criado com sucesso")
            else:
                print(f"\n✅ Usuário {self.mysql_root_user}@{self.local_ip} já existe")

            grant_root_sql = (
                f"GRANT ALL PRIVILEGES ON *.* "
                f"TO `{self.mysql_root_user}`@'{self.local_ip}' WITH GRANT OPTION"
            )
            print(f"\n⏳ Concedendo ALL PRIVILEGES (WITH GRANT OPTION) ao root...")
            print(f"   SQL: {grant_root_sql}")
            cursor.execute(grant_root_sql)
            print(f"   ✅ Permissão concedida para {self.mysql_root_user}@{self.local_ip}")

            # Flushes privileges
            print("\n⏳ Aplicando privilégios...")
            cursor.execute("FLUSH PRIVILEGES")
            print("✅ Privilégios aplicados com sucesso\n")

            # Verifica os grants
            print("🔍 Verificando permissões...")
            for who in (
                f"`{self.sicol_user}`@'{self.local_ip}'",
                f"`{self.mysql_root_user}`@'{self.local_ip}'",
            ):
                print(f"   • {who}:")
                cursor.execute(f"SHOW GRANTS FOR {who}")
                for grant in cursor.fetchall():
                    print(f"       ✅ {grant[0]}")

        except mysql.Error as e:
            print(f"\n❌ Erro ao executar SQL: {e.args[0]}: {e.args[1]}")
            print(f"   Mensagem completa: {e}")
            exit(1)
        finally:
            cursor.close()
            connection.close()

        print("\n" + "="*70)
        print("✅ Configuração concluída com sucesso!")
        print("="*70)
        print(f"\nOs usuários '{self.sicol_user}' e '{self.mysql_root_user}' agora têm acesso a partir do IP: {self.local_ip}")
        print("Você pode executar sua aplicação sem o erro 1130.\n")


if __name__ == '__main__':
    setup = MySQLPermissionSetup()
    setup.configure_permissions()
