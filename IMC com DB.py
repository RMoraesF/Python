import sqlite3

def conectar_bd():
    conexao = sqlite3.connect('imc_database.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            altura REAL NOT NULL,
            peso REAL NOT NULL,
            imc REAL NOT NULL
        )
    ''')
    conexao.commit()
    return conexao, cursor

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def classificar_obesidade(imc):
    if imc < 17:
        return 'Muito abaixo do peso'
    elif 17 <= imc < 18.5:
        return 'Abaixo do peso'
    elif 18.5 <= imc < 24.9:
        return 'Peso normal'
    elif 25 <= imc < 29.9:
        return 'Acima do peso'
    elif 30 <= imc < 34.9:
        return 'Obesidade I'
    elif 35 <= imc < 39.9:
        return 'Obesidade II (severa)'
    else:
        return 'Obesidade III (mórbida)'

def adicionar_paciente(nome, altura, peso, imc):
    conexao, cursor = conectar_bd()
    cursor.execute('INSERT INTO pacientes (nome, altura, peso, imc) VALUES (?, ?, ?, ?)', (nome, altura, peso, imc))
    conexao.commit()
    conexao.close()

def exibir_pacientes():
    conexao, cursor = conectar_bd()
    cursor.execute('SELECT * FROM pacientes')
    pacientes = cursor.fetchall()
    conexao.close()

    if not pacientes:
        print("Nenhum paciente encontrado.")
    else:
        print("\nLista de Pacientes:")
        print("{:<5} {:<15} {:<10} {:<10} {:<10} {:<15}".format("ID", "Nome", "Altura", "Peso", "IMC", "Classificação"))
        for paciente in pacientes:
            id, nome, altura, peso, imc = paciente[0], paciente[1], paciente[2], paciente[3], paciente[4]
            classificacao = classificar_obesidade(imc)
            print("{:<5} {:<15} {:<10} {:<10} {:<10.1f} {:<15}".format(id, nome, altura, peso, imc, classificacao))

def main():
    print("Bem-vindo à aplicação de IMC!")

    nome = input("Digite o nome do paciente: ")
    altura = float(input("Digite a altura do paciente (em metros): "))
    peso = float(input("Digite o peso do paciente (em quilogramas): "))

    imc = calcular_imc(peso, altura)
    classificacao = classificar_obesidade(imc)

    print(f"O IMC de {nome} é: {imc:.1f}")
    print(f"Classificação: {classificacao}")

    adicionar_paciente(nome, altura, peso, imc)
    exibir_pacientes()

if __name__ == "__main__":
    main()