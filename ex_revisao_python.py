"""
Lista de exercícios de revisão de Python
Disciplina: Programação para Análise de Dados
Nome do aluno: Danilo Barcelos
Matrícula: 202308875965
Email: 202308875965@alunos.ibmec.edu.br

Orientações:
- Resolva cada exercício separadamente.
- Execute o arquivo após cada solução para conferir o resultado.
- Use apenas os comandos básicos estudados em aula.
- Não use IA para resolver os exercícios, pois o objetivo é relembrar e praticar os conceitos aprendidos.
- Duvidas, mande um e-mail para o professor: laerte.takeuti@professores.ibmec.edu.br
- Se quiser mais exercícios, consulte o site: https://www.w3schools.com/python/default.asp
- Se quiser aulas em vídeo, consulte o canal: https://www.youtube.com/watch?v=S9uPNppGsGo&list=PLHz_AreHm4dlKP6QQCekuIPky1CiwmdI6
"""
# ============================================================================
# 1. VARIÁVEIS — EXERCÍCIOS 1 A 10
# ============================================================================

# Exercício 1 — Dados pessoais
# Crie quatro variáveis para armazenar seu nome, sua idade, sua altura e se você
# é estudante. Mostre o valor e o tipo de cada variável usando print() e type().
nome = "danilo"
idade = 25 
altura = 1.78
eh_estudante = False

# Exercício 2 — Saudação
# Peça ao usuário seu nome e sua cidade. Depois, mostre a mensagem:
# "Olá, <nome>! Você mora em <cidade>."

name = input("digite o seu nome")
cidade = input ("Digite a sua cidade")
print(f"O nome é {nome} e a cidade é {cidade}")



# Exercício 3 — Soma de dois números
# Leia dois números inteiros usando input(), converta-os com int() e mostre
# a soma dos valores.

N1 = input("digite um numero")
N2 = input("digite um numero")
N1 = int(N1)
N2 = int(N2)
total = N1 + N2
print(total)

# Exercício 4 — Operações básicas
# Leia dois números e mostre o resultado da soma, subtração, multiplicação
# e divisão entre eles.

N1 = 10 
N2 = 30
resultado_subtracao = N1 - N2
resultado_soma = N1 + N2
resultado_multiplicacao = N1 * N2
resultado_divisao= N1 / N2
total_subtracao = N1 - N2
print(total_subtracao)


# Exercício 5 — Média de três notas
# Leia três notas do tipo float, calcule a média aritmética e mostre o resultado
# com duas casas decimais.

nota1 = 10.0
nota2 = 9.0
nota3 = 6.0
media = (nota1 + nota2 + nota3) / 3
total= (nota1 + nota2 + nota3) / 3
print(total)


# Exercício 6 — Idade no futuro
# Peça a idade atual do usuário e informe quantos anos ele terá daqui a 10 anos.
idade_atual = int(input("Digite a sua idade: "))
print(f"Daqui a 10 anos você terá {idade_atual + 10} anos.")

# Exercício 7 — Conversão de temperatura
# Leia uma temperatura em graus Celsius e converta para Fahrenheit.
# Fórmula: fahrenheit = (celsius * 9 / 5) + 32
celsius = 45 
fahrenheit = (celsius * 9 / 5) + 32
print(fahrenheit)

# Exercício 8 — Área de um retângulo
# Leia a largura e a altura de um retângulo. Calcule e mostre sua área.
# Fórmula: area = largura * altura
largura = float(input("Digite a largura do retângulo: "))
altura = float(input("Digite a altura do retângulo: "))
area = largura * altura
print(f"A área do retângulo é {area:.2f}")

# Exercício 9 — Manipulação de texto
# Peça uma frase ao usuário e mostre:
frase = input("Digite uma frase: ")
# a) a frase em letras maiúsculas;
print(f"Maiúsculas: {frase.upper()}")
# b) a frase em letras minúsculas;
print(f"Minúsculas: {frase.lower()}")
# c) a quantidade de caracteres da frase.
print(f"Quantidade de caracteres: {len(frase)}")

# Exercício 10 — Preço com desconto
# Leia o nome de um produto, seu preço e um percentual de desconto.
# Calcule e mostre o nome do produto, o valor do desconto e o preço final.
produto = input("Digite o nome do produto: ")
preco = float(input("Digite o preço do produto: "))
desconto = float(input("Digite o percentual de desconto: "))

valor_desconto = preco * desconto / 100
preco_final = preco - valor_desconto

print(f"Produto: {produto}")
print(f"Valor do desconto: R$ {valor_desconto:.2f}")
print(f"Preço final: R$ {preco_final:.2f}")

# ============================================================================
# 2. ESTRUTURA CONDICIONAL — EXERCÍCIOS 11 A 20
# ============================================================================

# Exercício 11 — Positivo, negativo ou zero
# Leia um número e informe se ele é positivo, negativo ou igual a zero.
numero = int(input("Digite o número: "))

if numero > 0:
    print("O número é positivo")
elif numero < 0:
    print("O número é negativo")
else:
    print("O número é zero")
 

# Exercício 12 — Par ou ímpar
# Leia um número inteiro e informe se ele é par ou ímpar.
# Dica: use o operador de resto da divisão (%).
numero = int(input("Digite o número: "))
resto = numero % 2

if resto == 0:
  print("O número é par")
else:
   print("O número é ímpar")

# Exercício 13 — Aprovação
# Leia a média de um aluno. Mostre "Aprovado" se a média for maior ou igual
# a 7 e "Reprovado" caso contrário.
media = float(input("Digite a média do aluno: "))

if media >= 7:
    print("Aprovado")
else:
    print("Reprovado")


# Exercício 14 — Aprovação com recuperação
# Leia a média de um aluno e mostre:
# - "Aprovado", se a média for maior ou igual a 7;
# - "Recuperação", se a média estiver entre 5 e 6.9;
# - "Reprovado", se a média for menor que 5.

media = float(input("Digite a média do aluno: "))

if media >= 7:
    print("Aprovado")
elif media >= 5:
    print("Recuperação")
else:
    print("Reprovado")

# Exercício 15 — Maior entre dois números
# Leia dois números e mostre qual é o maior. Se forem iguais, informe isso.
n1 = float(input("Digite o primeiro número: "))
n2 = float(input("Digite o segundo número: "))

if n1 > n2:
    print(f"O maior número é {n1}")
elif n2 > n1:
    print(f"O maior número é {n2}")
else:
    print("Os números são iguais")

# Exercício 16 — Faixa etária
# Leia a idade de uma pessoa e classifique-a como:
# - "Criança": até 11 anos;
# - "Adolescente": de 12 a 17 anos;
# - "Adulto": de 18 a 59 anos;
# - "Idoso": 60 anos ou mais.
idade = int(input("Digite a idade: "))

if idade <= 11:
    print("Criança")
elif idade <= 17:
    print("Adolescente")
elif idade <= 59:
    print("Adulto")
else:
    print("Idoso")

# Exercício 17 — Desconto na compra
# Leia o valor de uma compra. Se o valor for maior que R$ 100,00, aplique
# desconto de 10%. Caso contrário, mantenha o valor original. Mostre o total.
valor = float(input("Digite o valor da compra: "))

if valor > 100:
    total = valor * 0.9
else:
    total = valor

print(f"Total a pagar: R$ {total:.2f}")

# Exercício 18 — Acesso ao sistema
# Leia o nome de usuário e a senha. Mostre "Acesso permitido" somente quando
# o usuário for "admin" e a senha for "1234". Caso contrário, mostre
# "Acesso negado".

usuario = input("Digite o usuário: ")
senha = input("Digite a senha: ")

if usuario == "admin" and senha == "1234":
    print("Acesso permitido")
else:
    print("Acesso negado")


# Exercício 19 — Número dentro do intervalo
# Leia um número e informe se ele está entre 10 e 50, incluindo os limites.
# Use os operadores and, >= e <=.
numero = float(input("Digite um número: "))

if numero >= 10 and numero <= 50:
    print("O número está no intervalo")
else:
    print("O número está fora do intervalo")

# Exercício 20 — Calculadora simples
# Leia dois números e uma operação (+, -, * ou /). Use if/elif/else para
# realizar a operação escolhida e mostrar o resultado. Não permita divisão
# por zero.
# Exercício 20 — Calculadora simples
n1 = float(input("Digite o primeiro número: "))
n2 = float(input("Digite o segundo número: "))
operacao = input("Digite a operação (+, -, * ou /): ")

if operacao == "+":
    print(f"Resultado: {n1 + n2}")
elif operacao == "-":
    print(f"Resultado: {n1 - n2}")
elif operacao == "*":
    print(f"Resultado: {n1 * n2}")
elif operacao == "/":
    if n2 == 0:
        print("Não é possível dividir por zero")
    else:
        print(f"Resultado: {n1 / n2}")
else:
    print("Operação inválida")

# ============================================================================
# 3. LISTAS — EXERCÍCIOS 21 A 30
# ============================================================================

# Exercício 21 — Criando uma lista
# Crie uma lista com as frutas "maçã", "banana", "laranja" e "uva".
# Mostre a lista completa.
frutas = ["maçã", "banana", "laranja"]


# Exercício 22 — Acessando elementos
# Usando a lista abaixo, mostre o primeiro e o último elemento.
# cores = ["azul", "verde", "amarelo", "vermelho"]
cores = ["azul", "verde", "rosa"]
cores [0]
cores [-1]

# Exercício 23 — Adicionando elementos
# Crie uma lista com três nomes. Peça outro nome ao usuário, adicione-o ao
# final da lista com append() e mostre a lista atualizada.
nomes = ["Danilo", "Laerte", "Fred"]

novo_nome = input("Digite outro nome: ")

nomes.append(novo_nome)

print("Lista atualizada:", nomes)


# Exercício 24 — Removendo elementos
# Dada a lista abaixo, remova "banana" com remove() e mostre o resultado.
# frutas = ["maçã", "banana", "laranja", "uva"]
frutas = ["maçã", "banana", "laranja", "uva"]

frutas.remove("banana")

print(frutas)

# Exercício 25 — Alterando um elemento
# Dada a lista abaixo, substitua "laranja" por "abacaxi" usando seu índice.
# frutas = ["maçã", "banana", "laranja", "uva"]
frutas = ["maçã", "banana", "laranja", "uva"]

frutas[2] = "abacaxi"

print(frutas)


# Exercício 26 — Tamanho e presença
# Dada a lista abaixo, mostre a quantidade de elementos e verifique se
# o número 30 pertence à lista.
# numeros = [10, 20, 30, 40, 50]
numeros = [10, 20, 30, 40, 50]

print(len(numeros))

print(30 in numeros)


# Exercício 27 — Soma, maior e menor
# Dada a lista abaixo, mostre a soma, o maior valor e o menor valor usando
# sum(), max() e min().
# valores = [12, 5, 28, 9, 17]
valores = [12, 5, 28, 9, 17]

print(sum(valores))
print(max(valores))
print(min(valores))

# Exercício 28 — Ordenação
# Coloque a lista abaixo em ordem alfabética usando sort() e mostre o resultado.
# cidades = ["Curitiba", "Salvador", "Recife", "Goiânia", "Manaus"]
cidades = ["Curitiba", "Salvador", "Recife", "Goiânia", "Manaus"]

cidades.sort()

print(cidades)

# Exercício 29 — Concatenação
# Una as duas listas abaixo em uma terceira lista e mostre o resultado.
# lista_a = [1, 2, 3]
# lista_b = [4, 5, 6]
lista_a = [1, 2, 3]
lista_b = [4, 5, 6]

lista_c = lista_a + lista_b

print(lista_c)


# Exercício 30 — Fatiamento
# Dada a lista abaixo, use fatiamento para mostrar:
# a) os três primeiros números;
# b) os três últimos números;
# c) os números do índice 2 ao índice 5.
# numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numeros[:3])
print(numeros[-3:])
print(numeros[2:6])

# ============================================================================
# 4. ESTRUTURAS DE REPETIÇÃO — EXERCÍCIOS 31 A 40
# ============================================================================

# Exercício 31 — Números de 1 a 10
# Use um laço for e range() para mostrar os números de 1 a 10.
for n in range (0,11): 
          print(n)

# Exercício 32 — Números pares
# Use um laço for para mostrar apenas os números pares de 2 a 20.
for numero in range(2, 21, 2):
    print(numero)

# Exercício 33 — Percorrendo nomes
# Use um laço for para mostrar cada nome da lista abaixo em uma linha.
# nomes = ["Ana", "Bruno", "Carla", "Diego"]
nomes = ["Ana", "Bruno", "Carla", "Diego"]

for nome in nomes:
    print(nome)

# Exercício 34 — Quadrados
# Use um laço for para criar uma nova lista contendo o quadrado de cada número.
# numeros = [1, 2, 3, 4, 5]
numeros = [1, 2, 3, 4, 5]

quadrados = []

for numero in numeros:
    quadrados.append(numero ** 2)

print(quadrados)

# Exercício 35 — Soma com for
# Use um laço for e uma variável acumuladora para somar os valores abaixo.
# Não use a função sum().
# valores = [10, 20, 30, 40, 50]
valores = [10, 20, 30, 40, 50]

soma = 0

for valor in valores:
    soma = soma + valor

print(soma)


# Exercício 36 — Contando aprovados
# Percorra a lista e conte quantas notas são maiores ou iguais a 7.
# notas = [8.0, 5.5, 7.0, 9.2, 4.0, 6.8]
notas = [8.0, 5.5, 7.0, 9.2, 4.0, 6.8]

aprovados = 0

for nota in notas:
    if nota >= 7:
        aprovados = aprovados + 1

print(aprovados)


# Exercício 37 — Contagem com while
# Use um laço while para mostrar os números de 1 a 10.
numero = 1

while numero <= 10:
    print(numero)
    numero = numero + 1


# Exercício 38 — Contagem regressiva
# Use um laço while para fazer uma contagem regressiva de 10 até 1.
# Ao terminar, mostre a mensagem "Fim!".
numero = 10

while numero >= 1:
    print(numero)
    numero = numero - 1

print("Fim!")

# Exercício 39 — Senha correta
# Peça uma senha ao usuário repetidamente usando while. O programa deve parar
# somente quando a senha digitada for "python123".
senha = ""

while senha != "python123":
    senha = input("Digite a senha: ")

print("Senha correta!")

# Exercício 40 — Somando até zero
# Peça números inteiros ao usuário e some os valores digitados. Use while para
# continuar a leitura até que o usuário digite 0. Ao final, mostre a soma.
soma = 0
numero = int(input("Digite um número: "))

while numero != 0:
    soma = soma + numero
    numero = int(input("Digite outro número: "))

print("Soma:", soma)


# ============================================================================
# 5. DICIONÁRIOS — EXERCÍCIOS 41 A 50
# ============================================================================

# Exercício 41 — Criando um dicionário
# Crie um dicionário chamado aluno com as chaves "nome", "idade" e "curso".
# Preencha com valores fictícios e mostre o dicionário completo.
aluno = {
    "nome": "Danilo Barcelos",
    "idade": 25,
    "curso": "Análise de Dados"
}
print(aluno)

# Exercício 42 — Acessando valores
# Dado o dicionário abaixo, mostre separadamente o nome e o preço do produto.
# produto = {"nome": "Teclado", "preco": 150.0, "estoque": 8}

produto = {"nome": "Teclado", "preco": 150.0, "estoque": 8}

print(f"Nome: {produto['nome']}")
print(f"Preço: R$ {produto['preco']:.2f}")

# Exercício 43 — Adicionando uma chave
# Adicione a chave "marca" ao dicionário abaixo e mostre o resultado.
# produto = {"nome": "Mouse", "preco": 80.0}
produto = {"nome": "Mouse", "preco": 80.0}

produto["marca"] = "Logitech"

print(produto)

# Exercício 44 — Atualizando um valor
# Altere o estoque do produto abaixo para 15 unidades e mostre o dicionário.
# produto = {"nome": "Monitor", "preco": 900.0, "estoque": 5}
produto = {"nome": "Monitor", "preco": 900.0, "estoque": 5}

produto["estoque"] = 15

print(produto)

# Exercício 45 — Removendo uma chave
# Remova a chave "cor" do dicionário abaixo usando pop() e mostre o resultado.
# carro = {"marca": "Ford", "modelo": "Ka", "ano": 2020, "cor": "prata"}
# Exercício 45 — Removendo uma chave
carro = {"marca": "Ford", "modelo": "Ka", "ano": 2020, "cor": "prata"}

carro.pop("cor")

print(carro)


# Exercício 46 — Verificando uma chave
# Verifique se a chave "telefone" existe no dicionário abaixo. Mostre uma
# mensagem informando o resultado.
# contato = {"nome": "Marina", "email": "marina@email.com"}

contato = {"nome": "Marina", "email": "marina@email.com"}

if "telefone" in contato:
    print("A chave 'telefone' existe")
else:
    print("A chave 'telefone' não existe")

# Exercício 47 — Chaves e valores
# Use keys() para mostrar todas as chaves e values() para mostrar todos os
# valores do dicionário abaixo.
# capitais = {"Brasil": "Brasília", "Argentina": "Buenos Aires", "Chile": "Santiago"}

capitais = {"Brasil": "Brasília", "Argentina": "Buenos Aires", "Chile": "Santiago"}

print(f"Chaves: {capitais.keys()}")
print(f"Valores: {capitais.values()}")


# Exercício 48 — Percorrendo um dicionário
# Use um laço for e items() para mostrar o nome de cada produto e seu preço.
# produtos = {"caderno": 25.0, "caneta": 4.5, "mochila": 120.0}
produtos = {
    "caderno": 25.0,
    "caneta": 4.5,
    "mochila": 120.0
}

for produto, preco in produtos.items():
    print(produto, preco)


# Exercício 49 — Soma dos valores
# Calcule a soma de todas as quantidades do dicionário abaixo e mostre o total.
# estoque = {"notebook": 5, "mouse": 20, "teclado": 12, "monitor": 4}
estoque = {
    "notebook": 5,
    "mouse": 20,
    "teclado": 12,
    "monitor": 4
}

total = sum(estoque.values())

print(total)


# Exercício 50 — Frequência de palavras
# Percorra a lista abaixo e crie um dicionário que conte quantas vezes cada
# palavra aparece. Ao final, mostre o dicionário de frequências.
# palavras = ["python", "dados", "python", "lista", "dados", "python"]
palavras = ["python", "dados", "python", "lista", "dados", "python"]

frequencia = {}

for palavra in palavras:
    if palavra in frequencia:
        frequencia[palavra] = frequencia[palavra] + 1
    else:
        frequencia[palavra] = 1

print(frequencia)