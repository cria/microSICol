#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para auto configurar permissões do usuário MySQL com base no IP real da máquina.
Isso resolve o erro "Host 'X.X.X.X' is not allowed to connect".

Autor: microSICol Setup
Uso: python3 setup_mysql_permissions.py
"""

import socket
import mysql.connector as mysql
from sys import exit


class MySQLPermissionSetup:
    """Configura as permissões MySQL na máquina com o IP real para o usuário sicol"""

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
            if e.args[0] == 1045:  # Acesso negado - tenta com senha
                print("⚠️  Autenticação unix_socket falhou, solicitando senha...")
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

            # Flushes privileges
            print("\n⏳ Aplicando privilégios...")
            cursor.execute("FLUSH PRIVILEGES")
            print("✅ Privilégios aplicados com sucesso\n")

            # Verifica os grants
            print("🔍 Verificando permissões...")
            cursor.execute(f"SHOW GRANTS FOR `{self.sicol_user}`@'{self.local_ip}'")
            grants = cursor.fetchall()
            for grant in grants:
                print(f"   ✅ {grant[0]}")

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
        print(f"\nO usuário '{self.sicol_user}' agora tem acesso a partir do IP: {self.local_ip}")
        print("Você pode executar sua aplicação sem o erro 1130.\n")


if __name__ == '__main__':
    setup = MySQLPermissionSetup()
    setup.configure_permissions()
