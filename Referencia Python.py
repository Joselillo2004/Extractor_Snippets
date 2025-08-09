# Ingreso por teclado básico -------------------------------------------------------------------------

	print("Ingresa tu nombre:")
	numero = input()

# Los ingresos siempre son cadenas que tienen que convertidas a números para ser procesados:

	float(numero) + 5
	
# Entrada por teclado: --------------------------------------------------------------------------------
# Almacenando 5 números en una lista:

# Creando una lista vacía:

	listas  = []

	print("Ingresa 5 números")
	for i in range(5):
		listas.append(input("Ingresa número: "))
	print("Numeros ingresados:",listas)

# Salidas por teclado: --------------------------------------------------------------------------------
# La más básica es por medio de un print.

	print("Hola a todos mis amigos")

# Pero existe otra manera más creativa para hacerlo por medio de format incrustando la salida en una cadena de caracteres:
# fromas de impresiòn:

	variable = 'Joselillo Castillo'
	otra = 'Genios estudiantes'

	forma = "El profesor '{}' y sus '{}'".format(variable,otra)
	
	# Retorna lo siguiente:
	
		# "El profesor 'Joselillo Castillo' y sus 'Genios estudiantes'"

# Para ponerlo de forma inversa:

	forma = "El profesor '{1}' y sus '{0}'".format(variable,otra)
	
	# Retorna lo siguiente:
		# "El profesor 'Genios estudiantes' y sus 'Joselillo Castillo'"


# Manejando una impresión con espacios:

	print('{:>50}'.format('Joselillo Castillo'))
	
	# Retorna:
		# 								Joselillo Castillo

# Sintaxis completa para print:

	print(object(s), sep=separator, end=end, file=file, flush=flush)
	
# Para imprimir un "*" con print en una sola línea:

		print("*",end="")

# Imprimiendo mensajes para efectos de debugging: --------------------------------------------------------------------------------

	from icecream import ic                # Importamos la libreria para imprimir informacion en consola útil para debuguear
	
	class Dog():
	    num_legs = 4
	    tail = True
	dog = Dog()
	
	print(dog.tail)         # Esto solo imprime el valor del atributo
	
	ic(dog.tail)            # Esto imprime igualmente de donde está saliendo el valor del atributo.


# Listas: -----------------------------------------------------------------------------------------

	lista = [1,2,3]

# Imprimir el primer número de la lista (print):

	lista[0]

# Imprimir un rango de la lista (print):

	lista[0:3]


# Mostrando todos menos el primer elemento de una lista:

	lista[1:]


# Agregar el numero 10 a la parte final de la lista(print):

	lista.append(10)

# Eliminando el número 3 contenido dentro de una lista llamada lista:

	lista.remove(3)

#Para remover el primer elemento de una lista:

	del lista[0]
	
# Ordenando de forma ascendente los elementos de una lista:

	sorted(lista)

# Ordenando una lista de forma descendente:

	sorted(lista, reverse = True)

# Insertando un elemento en una lista:

	animals = ['dog', 'cat', 'rat']
	
	# 'rabbit' is inserted at the third position (index 2)
	animals.insert( 2, 'rabbit')
	
	print(animals)     
	
	# Output:
	# ['dog', 'cat', 'rabbit', 'rat']

# Copiando un elemento de una lista:

	animals1 = ['dog', 'cat', 'rat']
	
	animals2 = animals1.copy()
	
	print(animals2)
	
	# Output:
	['dog', 'cat', 'rat']

# concatenación de listas:

	lista + lista2

# Una lista mixta

	lista_mixta = ['Pedro','Pablo',1,2,3,4.5]

# Consultando el último elemento de la lista:

	lista_mixta[-1]

# Consultando el tipo de último elemento de una lista:

	type(lista_mixta[-1])

# Consultando longitud de una lista:

	len(lista_mixta)

# Listas anidadas:

	a=[1,2,3]
	b=[4,5,6]
	c=[7,8,9]

	d=[a,b,c]

	print(d)

# Resultado: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Buscar un elemento "n" en una lista (la primer coincidencia):

	lista.index(n)
	
# Imprimiendo cada uno de los elementos de una lista: -----------------

	for i in lista:
		print(i)

# String o cadenas de caractéres: -----------------------------------------------------------------------------------------------------------

	nombre = "persona"
	nombres = 'personas'

# Imprimiendo en mayusculas o minúsculas:

	cadena = "Joselillo"
	print(cadena.upper())		# Todo se hace mayusculas
	print(cadena[0].upper())	# Solo imprime un caracter
	print(cadena.lower())		# Todo se hace minusculas
	print(cadena.title())


	print(cadena.split())		# Guarda dentro de una lista la cadena
	print(cadena.split("o"))	# Usa la O como separador, agrupando las secciones en listas.


	uno = "aprender"
	dos = "python"
	espacio = " ".join([uno,dos])		# Para unir dos o mas cadenas en una sola cadena de caracteres. Coloca un espacio como separador


	print(cadena.find())		# similar a index


	print(cadena.replace("bueno","malo"))		# Reemplaza "bueno" por "malo" en la cadena "cadena" (Edición de texto)

# Multiples ediciones de una cadena de la siguiente manera:

	cadena = "Si la implementación es difícil de explicar, puede que sea una mala idea."

	cadena1 = cadena.replace("difícil","fácil")
	cadena2 = cadena1.replace("mala","buena")

	print(cadena2)


# Concatenación

var1 + var2

# Indices de cadenas: --------------------------------------------------------------------------------

	alumno = "Joselillo Castillo Madrid"

# Para buscar el primer caracter de la cadena:

	alumno[0]

# Para buscar un rango de caracteres de la cadena

	alumno[0:5]
	
# Para buscar el último caracter en la cadena:

	alumno[-1]
	
# Buscar y obtener los últimos 4 caracteres de la cadena:

	alumno[-4:]


#Extrayendo un fragmento de texto pero saltándose un caracter a la vez (ejecutando cada 2 caracteres)

TEXTO = "ABCDEFGHIJK"

FRAGMENTO = [2:10:2]


# extrayendo un texto al revez del original: (ejecutando de -1 en -1)

Framneto_al_revez = [::-1]




# Cambiando el elemento de una cadena, no se puede, pero se puede asignar el cambio a una nueva variable:

	animal = 'Rat Master'
	
	new_animal = 'C' + animal[1: ]
	print(new_animal)

# Otra manera de obtener un cambio en la cadena, igual, en una nueva variable:

	text = 'bat ball'
	
	# replace 'ba' with 'ca'
	replaced_text = text.replace('ba', 'ca')
	
	print(replaced_text)    # cat call


# Indice de una cadena:

mi_texto = "Esta es una prueba"
resultado = mi_texto.index("n")			# Busca e imprime la posición de "n" dentro de la cadena mi_texto

print(resultado)		# Imprime la posición.


# Guiando la busqueda, pidiendo que se busque un caracter a partir de n posición.

mi_texto = "Esta es una prueba"
resultado = mi_texto.index("n", 5)			# Busca e imprime la posición de "n" dentro de la cadena mi_texto pero buscando a partir del índice 5.

print(resultado)		# Imprime la posición.


# Buscando desde y hasta el índice n un determinado caracter:

mi_texto = "Esta es una prueba"
resultado = mi_texto.index("n", 5, 11)			# Busca e imprime la posición de "n" dentro de la cadena mi_texto pero buscando a partir del índice 5.

print(resultado)		# Imprime la posición.


# Busqueda en reversa de un determinado caracter:

mi_texto = "Esta es una prueba"
resultado = mi_texto.rindex("n")			# Busca e imprime la posición de "n" BUSCANDO DESDE EL FINAL DE LA CADENA.

print(resultado)		# Imprime la posición.




# Imprimiendo la posición de una cadena de texto

mi_texto = "Esta es una prueba"
resultado = mi_texto.index("prueba")			# Busca e imprime la posición de "n" dentro de la cadena mi_texto

print(resultado)		# Imprime la posición.







# Buscando y encontrando secciones de texto en una cadena:

	message = 'Avengers'
	
	# get the index of 'nge'
	print(message.find('nge'))   # 3

# Imprimiendo o cambando una cadena a mayusculas:

	message = 'Python Is Fun'
	
	result = message.lower()
	print(result)   # python is fun
	
	result = message.upper()
	print(result)   # PYTHON IS FUN

# Imprimiendo los primeros 4 caracteres de una cadena concatenando con los últimos 4 caracteres de otra cadena:

	text1 = input()
	text2 = input()

	# create the result string
	# Hint: Use slicing
	result  = text1[:4] + text2[-4:]

	# print the result
	print(result)


# Obtener la longitud de la cadena:

	len(alumno)

# Para invertir una cadena:

	nombrei = nombre[::-1]

# ----- Ejemplo slicing:

nums = [10, 20, 30, 40, 50, 60, 70, 80, 90]
print(nums[1::2])

# 	Output [20, 40, 60, 80]

# ------------------ Otro ejemplo slicing:

nums = [10, 20, 30, 40, 50, 60, 70, 80, 90]
print(nums[::2])

# 	Output[10, 30, 50, 70, 90]

# -------------------------------

# Darle formato a una cadena (Mayusculas Al Principio)

	pais = input("¿Cual es la capital que busca?: ")
	corregido = pais.capitalize()

	# Resultado:  guatemala ------> Guatemala

# Formato de comillas para una cadena:

	text = '\"What\'s there?\", asked Paul'
	print(text)

	# Output: "What's there?", asked Paul

# Otra forma de imprimir bonita una cadena:

	name = 'Joe'
	country = 'US'
	
	print(f'name: {name} country: {country}')

# Bucles o iteraciones en una cadena (igual que en las listas):

	series = 'Dark'
	
	for character in series:
		print(character)

# Pruebas lógicas en una cadena, booleanos básicos en una cadena:

	text = 'Python'
	
	result =  'Py' in text
	print(result)   # True 
	
	result = 'PY' in text
	print(result)   # False


# Condicionales en Listas:

	fruits = ['apple','banana','mango']
	
	if 'apple' in fruits:
		print('apple is tasty')
	
	if 'potato' in fruits:
		print('Whaaaat?')

# Booleanos en listas:

	fruits = ['apple','banana','mango']
	
	print('Kiwi' in fruits)   # False
	print('Kiwi' not in fruits)   # True


# Operadores lógicos: ----------------------------------------------------------------------------------------------------------------------

# Test básico que puede resultar en True o False:

	2+4 == 7

# Test de una negación:

	not False == True
	
# Negación simple:

	not True
	
# Uso de operadores AND

	False and False
	
# Uso de números en los test:

	numero > 5 and numero <15

# Otras maneras de poner True o False:

	True == 1
	False == 0

# Operadores matemáticos:----------------------------------------------------------------------------

# Potencia:

	4**2
	pow(4,2)

# Raiz cuadrada:

	4 ** (1/2)

# Módulo:

	4 % 4
	
# Unicamente conocer la diviciòn exacta sin decimales ni residuos:

	4 // 3

# Suma 10 a la variable (válido para todas las operaciones):

	var += 10


# Operadores relacionales: -----------------------------------------------------------------------------
# Operadores booleanos simples:

# Distinto a:

	1 != 2
	
# Otro test de mayor que:

	4 >= 2

# Condicionales o Controles de flujo:

# Operadores relacionales compuestos:
# Booleanos compuestos:


	def is_even(number):
		if number % 2 == 0:
			return True
		else:
			return False
			
	n = int(input('Enter an integer: '))
	
	# result will contain either True or False
	result = is_even(n)
	
	if result:
		print(n, 'is even')
	else:
		print(n, 'is odd')


# If básico

letra = input("Ingrese una letra")

	if letra == "a" or letra == "e" or letra == "i" or letra == "o" or letra == "u":
	    print("Letra es una vocal")
	else:
	    print("Letra es una consonante")

# Elif básico:

	edad = int(input("Escribe tu edad: "))

	if edad >= 18 and edad < 65:
	    print("Eres un adulto.")
	elif edad >= 65:
	    print("Eres un adulto mayor.")
	else:
	    print("Aún no eres un adulto.")

# Listas:
# Funciones incluidas en Python para listas:

# Imprimiento la longitud de una lista:

	scores = [55, 64, 75, 80]

	count = len(scores)

# Obteniendo la suma de los elementos de una lista:

	scores = [55, 64, 75, 80]

	total = sum(scores)

#

# Impresión de Listas:

# FOR para multiplicar cada miembro de una lista x 10, incremento manual de índice: ---------------------------------------------------------

	lista = [1,2,3,4,5] # Este siempre al principio
	indice = 0 # Este va a ser mi índice
				# i va a recibir cada uno de los valores de la lista

	for i in lista:
		print(lista[indice]) # Imprimiendo cada uno de los elementos
		lista[indice] *= 10 # Multiplico cada miembro por 10
		indice += 1 # Sumo 1 al índice para pasar al siguiente elemento
		
# Haciendo lo mismo con Enumerate, el incremento del índice contador se hace automáticamente

	lista = [1,2,3,4,5]
	indice = 0

	for indice,i in enumerate(lista): # indice es mi índice, i no se ocupa esta vez (salvo en la sintaxis)
		lista[indice] *= 10 # Sumo 1 al índice para pasar al siguiente elemento
							# Aquí la suma de 1 al índice en cada repetición es automática
							
# Uso For cadenas de caracteres: Imprimiendo cada caracter

	nombre = "Joselillo"
	for i in nombre:
		print(i)
		
# Buble simple de 5 repeticiones:

	for i in range(5):
		print(i)

# Generando o creando una lísta de 12 posiciones llamada lista:

	lista = list(range(12))
	
	print(lista)		# Imprimiendo el resultado

# Lo mismo de una manera un poco mas entendible:

	# numbers from 0 to 4
	numbers = range(5)
	
	# converting numbers to list for printing
	numbers = list(numbers)
	
	print(numbers)
	
	# Output
	# [0, 1, 2, 3, 4]


# Obteniendo el factorial de un nùmero:


	n = int(input())

	for i in range(1,n):
	    n = n * i

	print(n)



# Generando una lista metiendo elementos manualmente:

	listas  = []
	print("Ingresa 5 números")
	for i in range(5):
	    listas.append(input("Ingresa número: "))
	print("Numeros ingresados:",listas)				# Los elementos almacenados son caracteres

# Convirtiendo cada elemto generado anterior a numero flotante (si lo que introdujiste antes fueron nùmeros):

	indice = 0
	for i in listas:
	    listas[indice] =float(listas[indice])
	    print(type(lista[indice]))
	    print(listas[indice])
	    indice +=1

# Verificando el tipo de el primer elemento de la lista anterior:

	print(listas)
	print(type(listas[0]))

# Verificando cada uno de los elementos de la lista anterior:

	indice = 0
	for i in listas:
	    print(type(listas[indice]))
	    indice +=1


# Sintaxis de range():-----------------

	range(start, stop, step)    #NOTA: Step también puede ser negativo para una cuenta regresiva.

# Imprimiendo una lista que inicia en 4, termina en 12 y que va sumando de 2 en 2 la secuendia de los elementos:

	lista = list(range(4,12,2))	# El último elemento no lo imprime
	print(lista)

# Así si imprime el ultimo elemento:

	lista = list(range(4,13,2))
	print(lista)

# Imprimiendo una cuenta regresiva simple:

	numbers = range(5, 0, -1)
	
	# convert to list and print it
	print(list(numbers))
	
	# Output
	# [5, 4, 3, 2, 1]

# cuenta cuantas veces aparece el 4 en la lista lista

	lista.count(4)

# Devuelve en que posición aparece el 12 en la lista

	lista.index(12)

# Agrega el elemento 155 al final de la lista:

	lista.append(155) # (Esta no sirve para tuplas)

# Obteniendo el último elemento de una lista:

	last_language = languages[-1]

# Obteniendo toda una lisa menos el primer y último elemento

	lista_recortada = lista_original[1:-1]

# Eliminando el segundo elemento de una lista:

	del animals[1]

# Eliminando una lista completa:

	del animals



# Lo anterior también sirve para tuplas.

Here's a summary of different data types we learned.
Data Type	Ordered?	Mutable?	Duplicates?
List		yes			yes			yes
Tuple		yes			no			yes
String		yes			no			yes
Dictionary	yes			yes			no (keys must be unique)
Set			no			yes			no


# WHILE --------------------------------------------------------------------

# Uso básico de WHILE:

	conteo = 0
	while conteo <= 5:
		print ("El conteo es:",conteo)
		conteo = conteo + 1
		
# Puede usar también ELSE:

	conteo = 0
	while conteo <= 5:
		print ("El conteo es:",conteo)
		conteo += 1
	else:
		print ("Se terminó el conteo")
		
# Se admite meter un BRAKE para romper el bucle:
# Break rompe el buble en curso

	conteo = 0
	while conteo <= 5:
		print ("El conteo es:",conteo)
		conteo = conteo + 1
		break
	else:
		print ("Se terminó el conteo")

# Continue hace algo màs parecido, pero de una manera más limitada:
# Unicamente es una instrucción para saltarse una iteración:
# Este código únicamente imprimirá los números pares en un rango de 1 a 11 (10)

	for number in range(1, 11):

		# condition to check odd number
		if number % 2 != 0:
			continue

		print(number)



# Tuplas: --------------------------------------------------------------------------------------------------------

# Estructuras como listas pero son inmutables, se delimitan por ( ).

	t = ('Joselillo','Castillo','Estudiante','Testing')

	p = (1,2,3,'pez','dorado')

# Consultando el elemento 3 de la tupla p:

	p[3]
	
# Consultando la longitud de una tupla:

	len(p)
	
# Buscando el elemento 'pez' en una tupla. (Registra solo la primer coincidencia):

	p.index('pez')


# Conteos en tuplas:
# Contando cuantos elementos = 'Joselillo' existen en la tupla t:

	t.count('Joselillo')
	
# Conjuntos, se delimitan con { } : -------------------------------------------------------------------------------------------------

# Forma básica de un conjunto:

	con = {1,2,3}

# Agregando el no 0.5 al conjunto (el elemento lo agrega y lo ordena dentro del conjunto):

	con.add(0.5)
	
# Quitando un elemento de un conjunto:

	animals = {'tiger', 'cat', 'dog'}
	
	# Remove the 'cat' item
	animals.discard('cat')
	
	print(animals)   # {'dog','tiger'}

# Verificando la pertenencia de un elemento a un conjunto:

	otrocon = {'Joselillo','Yo','Tu'}		# Conjunto
	
	'Joselillo' in otrocon					# Pregunta
	
	# Respuesta: True

# Otro ejemplo de lo anterior:

	animals = {'tiger', 'cat', 'dog'}
	
	print('pig' in animals)   # False
	print('pig' not in animals)   # True

# No se permiten elementos repetidos d entro de un conjunto:

	repetido = {'repetido','repetido','repetido'}
	
	# Devuelve:
	
	repetido = {'repetido'}

# Agregando lista de elementos a un conjunto:

	animals = {'dog', 'cat'}
	wild_animals = ['tiger', 'lion', 'lion']
	
	animals.update(wild_animals)							# <--------------- Tambièn aplica para diccionarios (update)
	print(animals)    # {'tiger', 'cat', 'lion', 'dog'}

# Se pueden eliminar elementos repetidos detro de una lista convirtiéndolos en un conjunto:
# Convertir lista en conjunto:

	lista = [1,1,2,2,3,3]

# Convirtiendo una lista en un conjunto:

	lista = set(lista)
	
	# Devuelve: 
		lista = {1,2,3}

# Por lo tanto, tambien se pueden eliminar elementos repetidos de ésta manera:
# Eliminando elementos repetidos:

	numbers = [1, 1, 2, 3, 4, 1, 1]
	
	numbers = list(set(numbers))
	print(numbers)   # [1, 2, 3, 4]

# Crear un conjunto vacío:

	conjunto = set()	# VERIFICAR
	
# También se pueden eliminar elementos repetidos en una cadena al convertirla a un conjunto:

	cadena = 'Una mas y me muero'
	
	cadena = set(cadena)
	cadena
	
	# Devuelve sus elementos componentes sin repetir:
	
		{' ', 'U', 'a', 'e', 'm', 'n', 'o', 'r', 's', 'u', 'y'}
	
# Unión de conjuntos:

	domestic_animals = {'dog', 'cat', 'elephant'}
	wild_animals = {'lion', 'tiger', 'elephant'}
	
	# union of sets
	animals = domestic_animals | wild_animals
	print(animals)
	
	# Output:
	# {'dog', 'tiger', 'elephant', 'lion', 'cat'}

# Intersección de conjuntos:

	domestic_animals = {'dog', 'cat', 'elephant'}
	wild_animals = {'lion', 'tiger', 'elephant'}
	
	# intersection of sets
	animals = domestic_animals&  wild_animals				# El amperson es la clave.
	print(animals)
 
# Output:
# {'elephant'}

# conjuntoides:

	letra = input("Ingrese una letra")

	if letra in "aeiou":			# Una cadena tambien puede considerarse un "conjunto" de elementos.
	    print("Es una vocal")
	else:
	    print("Es una consonante")

# Misma consulta en un diccionario:

	diccionario = {"Guatemala": "Ciudad de Guatemala", "El Salvador": "San Salvador", "Honduras": "Tegucigalpa","Nicaragua": "Managua", "Costa Rica": "San Jose", "Panama": "Panama", "Argentina": "Buenos Aires", "Colombia": "Bogota", "Venezuela": "Caracas", "España": "Madrid"}

	pais = input("¿Cual es la capital que busca?: ")
	corregido = pais.capitalize()

	if corregido in diccionario:
	    print(diccionario[corregido])
	else:
	    print("Elecciòn no se encuentra en diccionario")


# También se pueden evaluar números, pero tiene que estar en un string para ser validados:

	numero = "55466"
	otro_numero = input("Ingrese un digito: ")

	if otro_numero in numero:
		print("Incliye éste caracter")
	else:
		print("No está incluido")




# Diccionarios:	-----------------------------------------------------------------------------------------------------

# Forma básica de un dicicionario:

	diccionario = {'Joselillo':'Castillo','Estudiantes':'Genios'}
	
# Consulta en un diccionario:

	diccionario['Joselillo']
	
	# Respuesta: 
		'Castillo'

# Modificaciòn Simple de un diccionario, cambiando 'Castillo' por 'Madrid':

	diccionario['Joselillo'] = 'Madrid'


# Para eliminar el elemento 'Joselillo' de un diccionario:

	del(diccionario['Joselillo'])
	
# Contando los elementos de un diccionario:

	numbers = {10: 'ten', 20: 'twenty', }
	
	length = len(numbers)
	print(length)    # Output: 2
	
	person_info = {}
	print(len(person_info))   # Output: 0

# Cambiando el valor de un elemento de un diccionario:

	student_info = {
		'name': 'Kyle',
		'major': 'CS',
		'age': 19
	}
 
 
	# changing the value of the 'age' key to 20
	student_info['age'] = 20

# Agregando un elemento a un diccionario: ----------------------------

thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict["color"] = "red"
print(thisdict)


# Construyendo un diccionario de 3 elementos: -------------------------------

	# create an empty dictionary named my_dict
	my_dict = {}

	# use for loop to iterate from 1 to 3, including 3
	for i in range(3):
		# inside the loop, take input for key and value and store them in my_dict
		key = input("Llave de diccionario")
		value = input("Dato de la llave:")
		
		my_dict[key] = value			# <--------- Aquí clave de su construcción.

	# print my_dict
	print(my_dict)


# Modificando un elemento del diccionario: Sumando 1 al elemento Est1

	edades_de_mis_estudiantes['Est1']+=1

# Borrando un elemento de un diccionario:

	student_info = {
		'name': 'Kyle',
		'major': 'CS',
	}
	
	# deleting the item
	del student_info['name']

# Borrando un diccionario completo:

	student_info = {
		'name': 'Kyle',
		'major': 'CS',
	}
	
	# deleting the dictionary
	del student_info


# Uniendo dos diccionarios: 

	marks = {'Physics':67, 'Maths':87}
	internal_marks = {'Practical':48}

	marks.update(internal_marks)


	print(marks)	# A èste diccionario se le agrega el contenido del otro.

	# Output: {'Physics': 67, 'Maths': 87, 'Practical': 48}


# Haciendo operaciones con elementos de un diccionario sumando sus 2 elementos:

	edades_de_mis_estudiantes = {'Est1':20,'Est2':30}
	
	edades_de_mis_estudiantes['Est1']+edades_de_mis_estudiantes['Est2']
	
# Podemos hacer bucles (iteraciones) con los elementos de un diccionario:

	squares = {1: 1, 3: 9, 5: 25}
	
	for key in squares:
		print(key)

# -imprimiendo todos los elementos de una lista en un bucle (iteración):
 
	squares = {1: 1, 3: 9, 5: 25}
	
	for key in squares:
		
		# getting the value of a key
		value = squares[key]
		print(f'{key} -> {value}')

# Para hacer lo mismo pero con otro ejemplo y de una manera más simple:

	for edades in edades_de_mis_estudiantes:
		print(edades,edades_de_mis_estudiantes[edades])
	
# Revisando si un elemento de un diccionario existe:

	squares = {1: 1, 3: 9, 5: 25, 7: 49, 9: 81}
	
	print(1 in squares)   # True
	print(3 in squares)   # True
	print(49 in squares)   # False

# También podemos revisar lo contrario, si un elemento de un diccionario NO existe:

	squares = {1: 1, 3: 9, 5: 25, 7: 49, 9: 81}
	
	print(49 in squares)   # False
	print(49 not in squares)   # True

# Comprobando si un dato no numerico existe en un diccionario:


	my_dict = {"a": "juice", "b": "grill", "c": "corn"}

	# take user input for data
	data = input("Dato a revisar: ")

	# create a flag variable and set it to False
	flag = False

	# loop through my_dict
	for i in my_dict:
		# check if the value entered by the user is in the dictionary or not
		# if yes, set flag to True and terminate the loop
		if(data == my_dict[i]):
			flag = True
			break

	# print value found not found based on the flag status
	if(flag == True):
		print("Value found")
	else:
		print("Value not found")



# Transformando un diccionario (edades_de_mis_estudiastes) en una lista:

	lista = []
	lista.append(edades_de_mis_estudiantes)
	
	# DEvuelve:
		[{'Est1': 21, 'Est2': 30}]


# Metodos de diccionarios:----------------

# Get: 

# Obteniendo el registro de un diccionario. Si el registro no existe solo devuelve "None":

	scores = {'Physics':67, 'Maths':87}
	
	print(scores.get('Physics'))   # 67
	print(scores.get('Biology'))   # None

# Otro método para borrar un diccionario conmpleto:

	scores = {'Physics':67, 'Maths':87}
	
	scores.clear()
	print(scores)   # {}

# Creando una copia de un diccionario con otro nombre:

	original_marks = {'Physics':67, 'Maths':87}
	
	copied_marks = original_marks.copy()

# Conversión entre listas, tuplas, diccionarios, conjuntos y cadenas (strings):

# Convertir cualquier cosa en una lista:

# convert tuple to list
	result = list((1, 2, 3))   # [1, 2, 3]
	print(result)
	
	# convert string to list
	result = list('Hello')   # ['H', 'e', 'l', 'l', 'o']
	print(result)
	
	# convert dictionary to list
	result = list({2: 4, 10: 20})   # [2, 10]
	print(result)
	
	# convert set to list
	result = list({1, 2, 3})   # [1, 2, 3]
	print(result)

# Convierte cualquier cosa en una tupla:

	# convert list to tuple
	result = tuple([1, 2, 3])   # (1, 2, 3)
	print(result)
	
	# convert string to tuple
	result = tuple('Hello')   # ('H', 'e', 'l', 'l', 'o')
	print(result)
	
	# convert dictionary to tuple
	# dictionary's keys will be tuple's items
	result = tuple({2: 4, 10: 20})   # (2, 10)
	print(result)
	
	# convert set to tuple
	result = tuple({1, 2, 3})   # (1, 2, 3)
	print(result)

# Convertir coordenadas a diccionarios:

	# convert to dictionary
	coordinate = dict([('x', 5), ('y', -5)])
	print(coordinate)   # {'x': 5, 'y': -5}
	
	# convert to dictionary
	coordinate = dict(x = 5, y = -5)
	print(coordinate)   # {'x': 5, 'y': -5}

# Comvertir cualquier cosa en un conjunto:

	# convert list to set
	result = set([1, 2, 3])
	print(result) # {1, 2, 3}
	
	#convert string to set
	result = set('abca')
	print(result) # {'a', 'b', 'c'}
	
	# convert tuple to set
	result = set((1, 2, 3, 2, 3))
	print(result) # {1, 2, 3}
	
	# convert dictionary to set
	result = set({2: 4, 10: 20}) # (2, 10)
	print(result)


	# --------------------- Ordenar los elementos de un diccionario por llave o por dato: -----------------------------------


import operator             # Modulo imprescindible para hacer todo ésto

print(diccionario)          # Impresión de diccionario original para comparar

diccionario_sort = sorted(diccionario)
print(diccionario_sort)     # Llaves ordenadas de menor a mayor. (unicamente llaves)

diccionario_sort = sorted(diccionario.items())      # Llaves ordenadas de menor a mayor. (Orden lista completa)
print(diccionario_sort)

diccionario_sort = sorted(diccionario.items(), key = operator.itemgetter(1), reverse = True)    # 
print(diccionario_sort)




# Pilas: -------------------------------------------------------------------------------------------------------------
# Aquí se va el último que llegó
# Las pilas funcionan con listas:

	apilar = [1,2,3,4]
	
# Añadiendo contenido:

	apilar.append(3)
	apilar.append(6)
	apilar.append(8)
	apilar.append(2.5)
	
# La lista queda así:

[1, 2, 3, 4, 3, 6, 8, 2.5]

# Retirando elementos de las pilas iniciando por el último elemento:

	apilar.pop()

# Podemos almacenar en una variable lo que se extraiga:

	Var_extraida = apilar.pop()


# Colas: ------------------------------------------------------------------------------------------------------------

# Aquí se va primero el que primero llegó
# Resulta entonces en una solución más completa que pilas si queremos extraer elementos tanto de adelante como de atrás

# Para usar Colas debemos invocar una librería:

	from collections import deque

# Inicializando una variable donde almacenarémos la cola:

	colas = deque()
	
# Una cola tiene la siguiente forma:

	colas = deque(['Alvaro','Estudiantes','Familia','Genios'])
	
# Retirando el último elemento de una cola como si fuera una pila:

	colas.pop()

# Extrayendo el primer elemento que se almacenó:

	colas.popleft()
	
# Funciones: -------------------------------------------------------------------------------------------------------

# Forma básica de una función:

	def estudiantes():
		print("Genios mis estudiantes parte de mi familia digital")
		
# Invocación de una función:

	estudiantes()

# Función tabla del 7 con format:

	def tabla_del_7():
		for x in range(11):
			print("7 x {} = {}".format(x,x*7))
			
# Las variables que se usen dentro de la función solo existen dentro de la función, a menos que éstas se declaren como variables globales:

	def advierto():
		global variable
		variable = 'Joselillo'

# La variable que contiene 'Joselillo' podrá ser accesible desde el exterior de la función.

		
# Retorno de valores en funciones: ---------------------------------------------------------------------------------
# La formas más básicas:

# Devolviendo una cadena

	def estudiante():
		return "Estudiantes genios"

# Devolviendo una lista:

	def estudiante():
		return [1,2,3,4]

# La salida se puede almacenar en una variable:

	salida = estudiante()
	
# Se puede imprimir solo una parte si la salida es una lista o una cadena:

	print(estudiante()[0:2])
	
# Retornando múltiples cosas en una función:

	def estudiante():
		return [1,2,3,4],'Joselillo Castillo',2.5

# Podemos almacenar esas múltiples consas en multiples variables:

	a,b,c = estudiante()
	
# Envío de valores en funciones: -----------------------------------------------------------------------------------
# Las funciones también pueden recibir parámetros:

	def suma(i,x):
		return i+x

# Podemos hacer que una función admita valores nulos y que no necesariamente genere un error si parámetros no son introducidos:
# Si valores no son introducidos, avisará de manera amable que faltan parámetros.

	def nulos(x=None,i=None):
		if x == None or i == None:
			print("Se deben de ingresar parámetros")
			return
		return x+i

# Al invocar la función con parámetros, lo podemos hacer de manera más específica:

	def funciones(a,b):
		return a-b
		
# Podemos invocar la función anterior de la siguiente manera, especificando donde podemos mandar cada parámetro:

	funciones(b=2,a=1)

# En cuanto a las variables, todo lo que ocurra dentro de una función se queda dentro de la función:

	def estudiantes(valor):
		valor*3

	variable = 15
	estudiantes(variable)
	variable

	# Y la variable seguirá valiendo 15 al final.

# Errores
# Manera bonita de lidiar con errores, para no presentar mensajes de éstos mismos:

	try:
	  variable = float(input("Introduce un numero"))
	  a = 2
	  print("Resultado: ",a*variable)
	except:
	  print("Lo que introdujiste no fue un número")

# Misco código para dar múltiples oportunidades:

while(True):
  try:
    variable = float(input("Introduce un numero"))
    a = 2
    print("Resultado: ",a*variable)
    break									# Break para no entrar en bucle infinito.
  except:
    print("Lo que introdujiste no fue un número, te podemos dar otra oportunidad")
	
# Podemos hacer que una función admita valores nulos y que no necesariamente genere un error si parámetros no son introducidos:
# Si valores no son introducidos, avisará de manera amable que faltan parámetros.

	def nulos(x=None,i=None):
		if x == None or i == None:
			print("Se deben de ingresar parámetros")
			return
		return x+i

# Excepción múltiple, puedes especificar los tipos de errores que pueden suceder y una respuesta específica a cada uno de ellos:

	try:
		a = float(input("Numero: "))
		10/a
	except TypeError:
		print("Esto es una cadena querido")
	except ValueError:
		print("La cadena debe ser un número")
	except ZeroDivisionError:
		print("No se puede dividir entre cero")
	except Exception as x:
		print( type(x).__name__ )

# Podemos nosotros mismos generar más detalles en caso de un error de la siguiente manera por medio de un mensaje personalizado que puede ayudar a debuguear:

	def profesor(estudiantes=None):
	  if estudiantes is None:
		raise ValueError("Debes escribir algo ALGO ALGO AQUI")


# Para comprobar que nos encontramos en la función MAIN: (IGNORA EL CONTENIDO DE LA CONDICIONAL)

if __name__ == "__main__":                          # Esta es una comprobación de que en esta parte nos encontramos en el main
    # Create a workbook an sheets
    filename = "Absolute_relative.xlsx"			# Si nos encontramos en MAIN, se ejecuta el contenido de la condicional
    wb = Workbook()
    create_sheets(wb, ["Sheet2", "Sheet3", "Sheet4"])
    ws1 = wb["Sheet"]

# ----------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# Módulos de python:
#-----------------------------------------------------------------------------------------------------

# Instrumentos útiles para Ciencia de datos por ejemplo:

#If we need to perform tasks related to

    # data analytics, we will use modules such as NumPy, pandas, etc.
    # web development, we will use modules such as Django, Flask, etc.
    # csv files, we will use modules such as csv, pandas, etc.

# Importando módulo math (Matematicas):

	import math

	number = 25
	
	# compute square root
	result = math.sqrt(number)
	
	print(result)   # 5.0

# Creando "alias" de modulos importados:

	import math as m
	
	number = 25
	
	# compute square root
	result = m.sqrt(number)
	
	print(result)   # 5.0

# Si solo queremos importar ciertas funciones concretas, podemos hacerlo de la siguiente manera:

	from math import sqrt, floor		# Aquí solo importando dos funciones.
	
	number = 25
	
	# compute square root
	result = sqrt(number)			# Aquí las uso sin ponerle "prefijo"
	
	print(result)   # 5.0

# Y para usar éstas funciones importadas, solo es suficiente con utilizar su nombre:

	result = sqrt(number)

# CONSULTAR REFERENCIA DE PYTHON PARA OBTENER TODA LA BOLA DE FUNCIONES QUE SE PUEDEN USAR EN PYTHON.

# Modulo Random:
# Generando un número aleatorio entre 1 y 100:

	import random
	
	# random number between 1 and 100 (both inclusive)
	random_number = random.randint(1, 100)				# El 100 también puede aparecer en éste caso.
	
	print(random_number)

# Bucles anidados o bucles dentro de bucles:
# Iteraciones anidadas:

# Ejemplo sencillo:

	# Multiplica por dos el número introducido y lo representa en número de "*" asteriscos:

	# get integer input
	n = int(input())

	# iterate the outer loop n times
	for i in range(n):
		# iterate the inner loop 2 times
		for j in range(2):
			print('*')
			


#Otro Ejemplo:

	attributes = ['Electric', 'Fast']
	cars = ['Tesla', 'Porsche', 'Mercedes']
	
	for attribute in attributes:
		for car in cars:
			print(attribute, car)

# Salida del bucle anterior:

		# Electric Tesla
		# Electric Porsche
		# Electric Mercedes
		# Fast Tesla
		# Fast Porsche
		# Fast Mercedes

# Bucle anidado para imprimir asignación de valores:
# Las variables a imprimir se encierran en {llaves} en este caso:

	# outer loop iterates from i = 0 to 2
	for i in range(3):
		# inner loop iterates from j = 0 to 1
		for j in range(2):
			print(f'i = {i}, j = {j}')

# El buble anterio produce ésta salida:

	# i = 0, j = 0
	# i = 0, j = 1
	# i = 1, j = 0
	# i = 1, j = 1
	# i = 2, j = 0
	# i = 2, j = 1

# Otros operadores que pueden ser de utilidad, forma resumida de ellos:

	# Now, let's take a look at other assignment operators.

	# 	Operator	Example		Equivalent to
	# 	+=		x += 5		x = x + 5
	# 	-=		x -= 5		x = x - 5
	# 	*=		x *= 5		x = x * 5
	# 	/=		x /= 5		x = x / 5
	# 	%=		x %= 5		x = x % 5
	# 	//=		x //= 5		x = x // 5
	# 	**=		x **= 5		x = x ** 5


# La palabra "None" equivalente a "Null" para indicar que una variable no tiene valor:

	x = None
	print(x)    # None


# Truthy and Falsy:
# Comprobar la existencia de una variable:


	x = 5
	
	if x:
		print(x)   # 5 	Si la variable existe y tiene valor distindo de "0" (cero), imprime su valor, si no, no se imprime nada.

# Considerando que:

		# In Python these values are considered falsy.

		#     None
		#     False
		#     0, 0.0


# Sentencia Pass:
# Para dejar vacía una sentencia sun que se genere un error:

	n = 10
	
	# notice the use of pass inside the if statement
	if n > 10:
		pass
	
	print('Hello')

# Miscelanea de proyectos:------------------------------------------------------------------------------------------
# Programita para saber si un programa introducido es primo:

	number = int(input('Enter a number: '))
	
	is_prime = True
	
	# iterating loop from 2 to number-1
	for i in range(2, number):			# El conteo nunca llega a "number", corta antes.
		if (number % i) == 0:			# Aquí está el detalle, si un numero es "perfectamente" divisible entre otro...
			is_prime = False			# No es número primo, y ya para que revisa los otros!
			break
	
	if is_prime:
		print(f'{number} is prime')
	else:
		print(f'{number} is not prime')

# El mismo código como función:

	def check_prime(n):
		for i in range(2, n):
			if (n % i) == 0:
				return False
	
		return True
	
	number = int(input('Enter a number: '))
	
	# call the check_prime function
	is_prime = check_prime(number)
	
	if is_prime:
		print(f'{number} is prime')
	else:
		print(f'{number} is not prime')

# Pequeño codigo para corregir o filtrar la entrada del usuario por tecto:

	# get input until user enters 'rock', 'paper' or scissors
	while True:
		users_pick = get_user_input()
		if users_pick in ['rock', 'paper', 'scissors']:
			break

# Pequeño programa para contar los digitos de un número entero:

	# Replace ___ with your code
	import math

	number = int(input("Number please: "))

	count = int(math.log10(number))+1

	# print count
	print(count)




# List Comprehension: -------------------------------------------------------------------------------------------
# Creación de listas en corto:


# Creando una lista sucesiva de potencias de 2:

	numbers = [2**i for i in range(1, 6)]
	print(numbers)

	# [2, 4, 8, 16, 32]


# Sacando números pares de una lista existente, agregando un condicional

	numbers = [12, 15, 21, 32, 14]
	
	even_numbers = [n for n in numbers if n % 2 == 0]
	print(even_numbers)    # [12, 32, 14]



# Creación de un diccionario en corto, donde el dato es 10 veces el valor de la llave:

	# Replace ___ with your code

	# get integer input
	n = int(input("Enter a number to create a dictionary: "))

	# create the dictionary using comprehension
	numbers = {i : i * 10 for i in range(1, n + 1) if i >= 3}

	print(numbers)

		#Output: {3: 30, 4: 40, 5: 50, 6: 60}


# Funciones Lambda "Sin nombre" --------------------------------------------------------------------------------------------

	double = lambda n: n*2			# Un argumento de entrada, un parámetro de salida.
	print(double(10))    # 20


# Lambda múltiples argumentos:

	# program to find the product of two numbers
	product = lambda x, y: x*y
	
	result = product(5, 10)
	print(result)   # 50


# Keywords arguments en funciones: Los argumentos son asignados por el nombre, mas que por el orden en que entran a la función.

	def display_info(name, age):
		print(f'name = {name}')
		print(f'age = {age}')
	
	display_info(age = '22', name = 'Amanda')


# También se puede hacer una asignación similar al momento que la función es invocada:

	display_info(age = '22', name = 'Amanda')


# Funciones con valores por defecto: --------------------------------------------------------------------------

# Función con un valor por defecto. Cuando se invoca una función que pide un argunemto sin dárselo, entra el valor por defecto:

	def greet(message = 'Howdy'):
		print(message)
	
	greet()				# Sin éste valor, se produciría un error.


# Más ejemplos de funciones con valores por defecto:

	def display(symbol = '*', number = 5):
		print(f'symbol = {symbol}')
		print(f'number = {number}') 
	

# Otro ejemplo con 2 argumentos por default de manera simple:

	# define the call_me() function with arguments a and b
	def call_me(a = 5, b = 10):
		print(a)
		print(b)

	# take integer input
	n = int(input())

	# call call_me() with n as an argument
	call_me(n)

# Función "print" también tiene valores por defecto, aquí el valor por defecto es el espacio entre una palabra y otra:

	print('Hello','there')

# Se puede cambiar éste valor por defecto: Se llama sep

	print('Hello', 'there', sep = '###')

# Valores por defecto de una función para que acepte cualquier cantidad de parámetros sin arrojar un error:

	def greet(*messages):        # Con * puede aceptar cualquier cantidad de parámetros. Texto en éste caso.
		print(messages)
	
	# calling greet() with 1 argument
	greet('Hi')
	
	# calling greet() with 2 arguments
	greet('Hi', 'Hello')


# Función que recibe el ingreso de una tupla tamaño desconocido y devuelve la suma de sus componentes:

	def add_numbers(*numbers):			# Tupla de cualquier número de elementos.
		
		# calculate sum of tuple items
		total = 0
		for number in numbers:
			total = total + number;
			
		return total
	
	# call add_numbers with two arguments
	result = add_numbers(5, 10)
	print(result)    # 15
	
	# call add_numbers with three arguments
	result = add_numbers(5, 10, 20)
	print(result)    # 35

# Función que recibe cualquier cantidad de cadenas de caracteres, e imprime una por una:


	def print_items(*strings):
		# use a for loop to print individual items of the argument
		for i in strings:
			print(i)

	# take two string inputs
	text1 = input("Ingrese cadena 1: ")
	text2 = input("Ingrese cadena 2: ")

	# call print_items with text1 as argument
	print_items(text1)

	# call print_items with text1 and text2 as arguments
	print_items(text1, text2)


# Función que recibe un (((NUMERO INDETERMINADO O VARIABLE DE ARGUMENTOS)))

	def multiply_numbers(*numbers):			# Asterisco especifica número indeterminado de argumentos.
		multiplo = 1
		for i in numbers:
			multiplo = multiplo * i
		
		return multiplo


# Función que recibe un (((NUMERO INDETERMINADO O VARIABLE DE ARGUMENTOS))) keyword (importa nombre y no posición), 
# se usa doble **. El resultado es un diccionario:

	def print_info(**person):
		print(person)

	print_info()
	print_info(name = 'Steve')
	print_info(name = 'Steve', age = 22)

		#{}
		#{'name': 'Steve'}
		#{'name': 'Steve', 'age': 22}


# Recursividad-------------------------------------------------------------------------------------
# Función recursiva para calcular la sumatoria de n números hasta cero (1)

	def calculate_sum(n):
	
		if n != 0:
		# recursive call
			n = n + calculate_sum(n-1)
		
		return n
		
	
	result = calculate_sum(3)
	print(result)


# Función recursiva para calcular el factorial de un número:

	# Replace ___ with your code

	def calculate_factorial(n):

		if n != 1:

			# call calculate_factorial() with appropriate argument
			return n * calculate_factorial(n - 1)
		
		return n

	number = int(input())
	result = calculate_factorial(number)
	print(result)

# ---------------------- POO.---------------------------------------------------
# ----------------------------- Programación Orientada a Objetos: ------------------------------------

# --------------- ((((CLASES)))) -------------------

# ............................ VISTA DE CLASES YA MAS EN FORMA ..........................

# ;;;;;;;;;;		Self: 	;;;;;;;;;;;;;;;;

# Remember: We must always use self as the first argument in the function definition. This self takes the value of the object calling it.


# Forma muy básica de una Clase y la creación de un objeto:

	class MyClass:
		x = 5

	p1 = MyClass()				# ------Creación de un objeo.
	print(p1.x)
#---------------------------------------------------------------------------------------------

#	Clase que toma un solo atributo........ e imprime un mensaje dentro del mètodo:


	# create the person class
	class Person:
		# create the greet() method
		def greet(self, message):
			print(message)

	# get user input
	greeting = input()

	# create object
	person1 = Person()

	# call the greet() method using person1
	# use greeting as an argument
	person1.greet(greeting)


# -------------------------------------------------------------------------------------------------
# The __init__() Function, forma básica: 


# 						Clase que toma 2 atributos y........... la clase solo sirve para crear objetos ...... a falta de un método principal.

    class Person:
		def __init__(self, name, age):
			self.name = name
			self.age = age

    p1 = Person("John", 36)					# ------Creación de un objeto con atributos.

    print(p1.name)					# Imprime atributos por separado a travès del objeto.
    print(p1.age) 




# ---------------- Incluyendo un método en un objeto. Métodos en objetos son funciones que pertenecen al objeto: ------------------------------------------------------------------------------------


								# Clase que toma dos atributos.......... e imprime un atributo desde el mètodo principal:

    class Person:
		def __init__(self, name, age):      # Clase __init__ para agregar atributos.
			self.name = name
			self.age = age

		def myfunc(self):
			print("Hello my name is " + self.name)      # Método de objeto. Este pertenece al objeto.

    p1 = Person("John", 36)         # ------CREANDO el objeto p1 a partir de la clase Person, y agregandole 2 atributos (en corto).
    
	p1.myfunc()                     # Invocando el mètodo (Resultado no se almacena en variable porque imprime de su lado) ---(OBJETO.MÉTODO)---

# ----------------------------------------Objeto.metodo-----------------------------------------


# Se pueden modificar cualquiera de los atributos del objeto de ésta manera:

     p1.age = 40 

     print(p1.age)				# Se imprime manualmente un atributo.
        # Output: 40

# También se puede eliminar un objeto ya existente:

    del p1
        # Output: Va a eliminar todo el objeto "p1 = Person("John", 36)"


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------              --------------------          -------------------           -----------------              --------------            ---------------           --------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------            -----------------        -----------------            -----------------       --------------------            ------------------           ------------------
# COMPORTAMIENTO PECULIAR aprendido en el curso: (Va a ser de utilidad más adelante)--------------------------- SE INGRESAn DOS OBJETOS COMO ARGUMENTOS.
#

	class Test:
		def __init__(self, name):
			self.attr = name
	
		def print_value(self, obj):
			print(self.attr)				# Se imprimen de manera secuencial los atributos de ambos objetos.
			print(obj.attr)

	t1 = Test('Mira')						# ------CREANDO dos objetos con atributos.----------
	t2 = Test('Daniel')						

	t2.print_value(t1)							##############################

# -----------------------------------Objeto.Método-------------------------


# Retornando objetos desde Mètodos: ------- "SUSTITUCION". ------------------------- SE INGRESA UN OBJETO COMO ARGUMENTO. -------- SE RETORNA UN OBJETO DEL MÈTODO PRINCIPAL QUE SE CREA DENTRO DE LA CLASE.

	class Person:
		def __init__(self, name, age):			# Declaraciòn de atributos
			self.name = name
			self.age = age

		def return_another_person(self):		# Mètodo principal, toma un objeto como argumento.

			# creating an object of the Person class
			person = Person('Sara', 20)					# Se crea un objeto dentro del mètodo que serà la SALIDA DEL MÉTODO en éste caso.----------
			
			# returning the object
			return person											# Se retorna el objeto que se creó dentro del método. SALIDA DEL MÉTODO

	# create an object (argumento)
	person1 = Person('Ana', 21)					# ------Se CREA un segundo OBJETO que entra como argumento del método principal.


	another_person = person1.return_another_person()		################################### Es suficiente con cumplir con: "Objeto.Mètodo principal"
															# Para subir un objeto, no se necesita argumento adicional.

	print(another_person.name)    # Sara
	print(another_person.age)    # 20						# Impresiòn simple.


# -----------------------------------------------------------------------------------------------------

# Otro ejemplo de la creación de un objeto dentro de la función de un método:		### Insider ###

class Vehicle:
    def __init__(self, wheels):
        self.wheels = wheels
    
    def run_method(self):					# Debe de contener (self), aunque solo sea para impresión.
        print(f'v1 wheels: {self.wheels}')
 
       # creating an object of Vehicle 
        v2 = Vehicle(2)
        print(f'v2 wheels: {v2.wheels}')
        
v1 = Vehicle(4)
v1.run_method()




# Ejemplo para la suma de dos nùmeros complejos:------------------------------ SE INGRESAN DOS OBJETOS COMO ARGUMENTOS: ------- SE RETORNA UN OBJETO DEL MÈTODO PRINCIPAL.


	class Complex:
		# using __init__() to create attributes
		def __init__(self, real, imag):					# Carga de atributos
			self.real = real
			self.imaginary = imag

		# method to add complex numbers
		def add(self, number):												# Ingresando dos objetos como argumentos de entrada.
			result_real = self.real + number.real							# Sumando cada una de las componentes.
			result_imaginary = self.imaginary + number.imaginary
			
			# create another object of Complex
			result = Complex(result_real, result_imaginary)  	# Preparando la salida en forma de creación de un objeto dentro del método principal.
			return result										# Retornando como objeto el resultado de la suma.

	n1 = Complex(5, 6)							# Creando 2 objetos que serviràn como entrada.
	n2 = Complex(-4, 2)

	# The return value from the add() method
	# is assigned to the n3 variable
	n3 = n1.add(n2)							# Por COMPORTAMIENTO PECULIAR ###########################	Se cumple: "objeto.método principal	"
											


	# printing n3 attributes
	print('real part =', n3.real)
	print('imaginary part =', n3.imaginary)
													

# ----------------------------------------------------------------------------------------------  SE INGRESA UN OBJETO Y SE RETORNA UNA VARIABLE: --------------

class Triangle:
    
    # initialize attributes
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    # method to compute perimeter
    # Hint: you don't need to pass additional arguments to solve this problem
    def get_perimeter(self):
        perimeter = self.a + self.b + self.c
        return perimeter  

# take three integer inputs
a = int(input("Intro a"))
b = int(input("Intro b"))
c = int(input("Intro c"))

# create an object of Triangle
triangle = Triangle(a, b, c)				###	###	###	###	###	###	###	###	###	###

# call the get_perimeter() method using the object
result = triangle.get_perimeter()								############################### Es suficiente con cumplir con: "Objeto.Mètodo principal"
																# Para subir un objeto, no se necesita agregar argumento adicional.
print(result)


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# So here's our suggestion. If you are working on a simple problem, do not use object-oriented programming because you have to write a lot of code.

# However, if you are working on a complex problem where many variables and functions are related, creating objects to solve that problem makes sense.

#----------------------------------------------------------------------------------------------------------------------------------------------------------

# ########### Juego de Piedra, Papel o Tijera ################ 	MAS ABAJO EL CODIGO DEL PROGRAMA COMPLETO.

import random

# class Game:
#     def __init__(self):
#         # call the get_computer_pick() method 
#         self.computer_pick = self.get_computer_pick()         # Aquí la entrada es interna (el lugar de un atributo u objeto externo)
#                                                               # Y se trata de la función de aquí abajo:
# 													# Se coloca así para que se ejecute

    def get_computer_pick(self):                    # Función de "Entrada interna", es declarada en la función __init__ de arriba.
        # get random number among 1, 2 and 3
        random_number = random.randint(1, 3)
        
        # possible options 
        options = {1: 'rock', 2: 'paper', 3: 'scissors'}
        
        # return the value present at random_number
        return options[random_number]


g1 = Game()                           # Con una clase siempre se tiene que crear un objeto, y en base a éste se invocan las funciones.
eleccion = g1.get_computer_pick()		# Si se llama la función manualmente, no hay necesidad de incluir __init__ en la clase.
print("La eleccióon fue: ", eleccion)	


# &&&&&&&&&&&&&&&& Para hacer exactamente lo mismo  sin una clase, solo una función: &&&&&&&&&&&&&&&&&&&

def get_computer_pick():
  # get random number among 1, 2 and 3
  random_number = random.randint(1, 3)

  # possible options 
  options = {1: 'rock', 2: 'paper', 3: 'scissors'}

  # return the value present at random_number
  return options[random_number]


eleccion = get_computer_pick()					# Invocación simple de la función.
print(eleccion)



# --------------------######### CODIGO COMPLETO:: ##########--------------------------


import random

class Game:
    def __init__(self):
        # get the computer's pick 
        self.computer_pick = self.get_computer_pick()			# Ver comentarios arriba. ("Entradas internas")
														# Se colocan así para que se ejecuten automaticamente.
        # get the user's pick
        self.user_pick = self.get_user_pick()				# ("Entdada interna") Invocan la función de abajo.

        # get the result of the game
        self.result = self.get_result()     				# ("Entrada interna")	Invocan la función de abajo.
    
    def get_computer_pick(self):					# Función elección de la computadora.
        # get random number among 1, 2 and 3
        random_number = random.randint(1, 3)
        
        # possible options 
        options = {1: 'rock', 2: 'paper', 3: 'scissors'}
        
        # return the value present at random_number
        return options[random_number]

    def get_user_pick(self):						# Función elección del usuario y conversión a un formato estándar.
        
        # infinite while loop 
        while True:
            user_pick = input('Enter rock/paper/scissors: ')

            # convert to lowercase
            user_pick = user_pick.lower()

            # if user_pick is either rock or paper or scissors,
            # terminate the loop
            if user_pick in ('rock', 'paper', 'scissors'):
                  break
            else:
                print('Wrong input!')

        return user_pick

    def get_result(self):							# Función de determinación del resultado de juego.
        # condition for draw
        if self.computer_pick == self.user_pick:
            return 'draw'
        
        # condition for the user to win
        elif self.user_pick == 'paper' and self.computer_pick == 'rock':
            return 'win'
        elif self.user_pick == 'rock' and self.computer_pick == 'scissors':
            return 'win'
        elif self.user_pick == 'scissors' and self.computer_pick == 'paper':
            return 'win'
        
        # in all other conditions, users lose    
        else:
            return 'lose'

    def print_result(self):									# Esta función solo imprime el resultado.
        print(f"Computer's pick: {self.computer_pick}")		# A partir de su ejecución en la función __init__
        print(f'Your pick: {self.user_pick}')			# Esta és la única que se ejecuta manualmente (no incluida en __init__)
        print(f'You {self.result}')


# create an object of the Game class
game = Game()								# Creación del objeto.


game.print_result()						# Solo resta invocar ésta función (no incluida en__init__).


# Lo anterior se puede ejecutar "n" veces de la siguiente manera:

	for i in range(5):
	game = Game()
	game.print_result()

# O preguntandole al usuario si quiere jugar nuevamene:

	while True:
	game = Game()
	game.print_result()

	play_again = input('Do you want to play again? (y/n): ')

	# if user enter any other character other than y, the game ends
	if play_again != 'y':
		break

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# -------- Clase que obtiene la suma de una lista: -------

# Replace ___ with your code

# create the Student class
class Student:

    # use the __init__() method to initialize the scores attribute  
    def __init__(self, scores):
        self.scores = scores
  
    # create the get_scores_sum() method that returns the sum of scores items
    def get_scores_sum(self):
        result = sum(self.scores)
        return result

# create the scores variable
scores = [55, 75, 80, 62, 77]

# create an object of Student by passing scores as an argument
s1 = Student(scores)

# call the get_scores_sum() method using the s1 object
total = s1.get_scores_sum()

# print total
print(total)

# -------------------------------------------------------------------------------------------------------------

# ---------------- Creación del objeto de una clase dentro de otra clase: --------------------------------------
# ---------------- EJECUCIÓN EN CADENA DE CLASES: ------------------------------------------------
# Este programa crea vehículos de "n" ruedas, pero siempre le pone motor con potencia de "400" desde el punto de vista de clases:


#		OTRA MANERA DE HACER LAS IMPRESIONES DE ABAJO:

print(f'vehicle wheels: {self.wheels}')

print(f'vehicle power: {self.engine.power}')


# # # ----------------------------------------------------------------------------------------
# # # ---------------------------------------------------------------------------------------
# # # ---------------------------------------------------------------------------------------
# --------------------- Esencialmente casi el mismo código anterior en términos mas facilitos:------------------ EJECUCIÓN EN CADENA DE CLASES:

# Replace ___ with your code

# create the Engine class
class Engine:
    # use __init__() to initialize the power attribute 
    def __init__(self, power):
        self.power = power
        

# create the Vehicle class
class Vehicle:
    # use __init__() to initialize the wheels attribute
 
    def __init__(self, wheels):
        self.wheels = wheels
        
        # the engine attribute should be an object of the Engine class with the power attribute 400
        self.engine = Engine(400)
    
    # create the get_power() method
    def get_power(self):
        # print the power attribute of the engine attribute (which is an object of Engine) 
        # print("Power:", self)
        print("wheels:",self.wheels)                # Se imprime un atributo de ésta clase		---ARRIBA MANERA ALTERNATIVA DE HACER ESTAS IMPRESIONES.---
        print("Engine power:",self.engine.power)        # Se imprime un atributo de otra clase (De la clase de arriba, "Engine")

# create an object of Vehicle
v1 = Vehicle(2)                     # Objeto de la clase Vehicle

# call the get_power() method using the object
v1.get_power()                                      # A través del objeto anterior se invoca manualmente el método "get_power" dentro de la clase "Vehicle"




# ----------------------------------------------------------------------------------------------------------------------------

# ------------------- Tik tac toe game project example: ------------------------------------------------

# ---------- Estos serán los componentes: --------------------

    # Board (Clase 1) - to handle the tic-tac-toe board and handle winning/draw logic
    # Player (Clase 2) - to handle the name of players and symbols they are using
    # Game (Clase 3) - to handle the game logic



class Board:				######	((((Board)))) Sirve para imprimir el tablero de juegoen formato de texto.
    def __init__(self):
        self.board = [' ', ' ', ' ', 	# Sin entradas externas a la clase, únicamente se crea una lista que servira 
                      ' ', ' ', ' ', 	# para construir el tablero del tik tok mas adelante.
                      ' ', ' ', ' ']	# En un inicio se tratan de espacios vacíos, mas adelante no será así.

    def print_board(self):		# Método o función para la impresión del tablero con ayuda de la lista de arriba.
        print('\n')
        print(' ' + self.board[0] + ' | ' + self.board[1] + ' | ' + self.board[2])
        print('-----------')
        print(' ' + self.board[3] + ' | ' + self.board[4] + ' | ' + self.board[5])
        print('-----------')
        print(' ' + self.board[6] + ' | ' + self.board[7] + ' | ' + self.board[8])

    def update_board(self, position, type):		# Método para actualizar las posiciones del tablero:

        try :
            # if a player selects position n, n-1 index should be updated
            # if the position is not already filled, update the board 
            if self.board[position - 1]  == ' ':      
                self.board[position - 1] = type
                return True 

            # if the position is already filled, ask user to select another position
            else: 
                 print('Position already selected. Select another position.')
                 return False
        except:
            print('Invalid position! Select another position.')

    # If three symbols appears in a row, returning True		# (((El "type" es el atributo que puede ser X ó O))) (ficha)
															# "\" se usa para un salto de línea en código.
															
    def check_winner(self, type):							# Método para verificar si existe algún ganador. ((Verifica ganador))
															# Reglas de lógica para determinarlo:
        if (self.board[0] == type and self.board[1] == type and self.board[2] == type) or \
           (self.board[3] == type and self.board[4] == type and self.board[5] == type) or \
           (self.board[6] == type and self.board[7] == type and self.board[8] == type) or \
           (self.board[0] == type and self.board[3] == type and self.board[6] == type) or \
           (self.board[1] == type and self.board[4] == type and self.board[7] == type) or \
           (self.board[2] == type and self.board[5] == type and self.board[8] == type) or \
           (self.board[0] == type and self.board[4] == type and self.board[8] == type) or \
           (self.board[2] == type and self.board[4] == type and self.board[6] == type):
            return True				# Si cualquiera de las posibilidades de arriba se cumplen, hay un ganador
        else:
            return False			# De lo contrario, no lo hay en éste punto.

    # If all fields are selected and there is no winner, it's a draw
    # Returning True if it's draw
    def check_draw(self):						# Método que verifica si hay un empate. ((Verifica empate))
        if ' ' not in self.board:				# Si no hay alguno vacío (y no hay ganador), significa que hay un empate.
            return True
        else:
            return False					# De lo contrario, el juego todavía no termina.



class Player:						########## (((((Player)))))		# Identifica a cada jugador por ficha asignada.
    def __init__(self, type):			# Unicamente un atributo de entrada.
        self.type = type
        self.name = self.get_name()		# Se ejecuta automaticamente un método
    
    def get_name(self):			# Se ejecuta automáticamente con un atributo de entrada (Ficha de juego)
        if self.type == 'X':
            name = input('Player selecting X, enter your name: ')
        else:										# Adicionalmente pide por consola el nombre del jugador.
            name = input('Player selecting O, enter your name: ')
        return name			# Una vez que identificó al usuario de la ficha X ó O devuelve su nombre recogido por consopla



class Game:						# Es el método que se encarga de ejecutar la "administración" del juego.
    def __init__(self):
        self.board = Board()					# Se crea un objeto que es el tablero mismo ((Ejecución de métodos en cadena))
												# con la clase "Board()"

        self.player1 = Player('X')				# Cada jugador es representado por un objeto que invoca el método Player
        self.player2 = Player('O')													# ((Ejecución de métodos en cadena))

        self.current_player = self.player1		# Declaración de un atributo para que el jugador 1 siempre sea el primero en turno.

    # updating the play method
    def play(self): 		# Es ejecutado manualmente desde el cuerpo principal del programa (main)
							# Método que se encarga de la ejecución principal del juego.
        try:
            # using an infinite loop to run the game
            # we will later add conditions to terminate the loop
             while True:
                  message = f'{self.current_player.name}, enter the position (1 - 9): '
                  position = int(input(message))				# Pregunta tirada deseada al jugador

                  # the update_board() method return True if
                  # the user selected position is not already filled
                  if self.board.update_board(position, self.current_player.type):		# Actualiza el tablero
                      self.board.print_board()
                    
                      # checking winner each time after updating the board 
                      if self.board.check_winner(self.current_player.type):		# Revisa si ya hay un ganador (en cada jugada)
                          print(self.current_player.name, 'wins!')
                          break

                      # checking draw each time after updating the board	# Si no hay un ganador todavía
                      elif self.board.check_draw():							# revisa si existe un empate (en cada jugada)
                          print('Game is a draw!')
                          break               

                      # changing current player when board is updated 
                      else:
                          if self.current_player == self.player1:		# Intercambio de turnos para cada jugador
                              self.current_player = self.player2		# en caso de que no exista ni empate ni ganador
                          else:
                              self.current_player = self.player1 
        except:
                print('Invalid input! Enter a number between 1 and 9.') 	# Por si el usuario mete una mala posición.


game = Game()			# Se construye un objeto para inciciar el juego
game.play()			# Se ejecuta manualmente el método "Play()" (Encargado de ejecutar el juego)
















##############################################################################################################################################################


# ----- Everything is an object in Python---------------------------------------------------------------------
# --------------------------------------------------------------------------------------
	number = 10
	print(type(number))

# ------------------------------------------------------------------------

# We can check the attributes and methods of an object using the dir() function:

	number = 1
	print(dir(number))

# This means, an integer (which is an object) can access all these methods and attributes:

	number = 5

	result = number + 100
	print(result)

# ------------------------------------------------------------------------------

# The id() function returns the identity of the given object. If the ids of two objects are the same, that means they are referring to the same object.

	number1 = 5
	print(id(number1))   # 9789120

	number2 = 10
	print(id(number2))   # 9789280

# Now, let's see what will happen if we assign one variable to another.

	number1 = 5
	print(id(number1))   # 9789120

	number2 = number1
	print(id(number2))   # 9789120

# ----------------------------------------------------------------------------------

# Como funcionan las variables:

	list1 = [1, 2, 3]

	# assign list1 to list2
	list2 = list1 

	# append an item to list1
	list1.append(4)

	print(list1)
	print(list2)

# copy() method:

	list1 = [1, 2, 3]

	# assign list1 to list2
	list2 = list1.copy()

	list1.append(4)

	print(list1)    # [1, 2, 3, 4]
	print(list2)    # [1, 2, 3]



###############################################################
########### ---------------- HERENCIA---------------------------

	# base class
	class Animal:
		def eat(self):			# Recuerda siempre el "self", si ni lo pones ocasiona errores !!!!
			print("I can eat")			# La primer clase (clase madre)

	# the Dog class is derived from Animal
	# notice Animal inside ()        
	class Dog(Animal):					# La segunda clase (clase hija)
		def bark(self):
			print("I can bark")

	# object of the dog class
	dog1 = Dog()					# Objeto a partir de la clase hija.

	# call the bark() method (of Dog)
	dog1.bark()							

	# call the eat() method (of Animal)
	dog1.eat()							# El objeto invoca un método de la clase madre (Animal) a través de la herencia.


# -----------------------------------------------------------------	Otro ejemplo de herencia: ----------------------------------


	class Polygon:								# Clase madre
		def __init__(self, sides):
			self.sides = sides

		def display_info(self):
			print("A polygon is a two dimensional shape with straight lines.")

		def get_perimeter(self):
			perimeter = sum(self.sides)
			return perimeter

	class Triangle(Polygon):												# Clase Triangle que hereda los métodos de la clase Polygon (Clase madre)
		def display_info(self):
			print("A triangle is a polygon with 3 edges.")

	# create an object of Triangle
	t1 = Triangle([5, 6, 7])										# Se crea objeto a partir de triangulo (Clase hija)

	# call get_perimeter using t1
	perimeter = t1.get_perimeter()							# Se invoca el método principal de Clase Polygon (Clase Madre)

	print("Perimeter:", perimeter)

	# call display_info() using t1
	t1.display_info()										# Se invoca MEt principal de Clase Triangle (Clase hija)


# 3 --------------------------------------------------------------------------------------------------------------

# Using super() ------------------------------------- HERENCIA ESPECIFICA super()-------------------------------------------------------------

	class Polygon:							# Clase madre.
		def __init__(self, sides):
			self.sides = sides

		def display_info(self):
			print("A polygon is a two dimensional shape with straight lines.")

		def get_perimeter(self):
			perimeter = sum(self.sides)
			return perimeter

	class Triangle(Polygon):				# Clase hija, (la herencia se hace normalmente).
		def display_info(self):
			print("A triangle is a polygon with 3 edges.")

			# call the display_info() method of Polygon
			super().display_info()								# Aquí se usa Super() Se invoca desde éste método el método de la clase padre "display_info()"
																# Explícitamente. (A estos NO se les pone "self")
	# create an object of Triangle
	t1 = Triangle([5, 6, 7])						# Creando el objeto.

	# call get_perimeter using t1
	perimeter = t1.get_perimeter()
	print("Perimeter:", perimeter)

	# call display_info() using t1
	t1.display_info()							# Invocando método display_info() de la clase madre.

# -----------------------	Otro ejemplo de super(): -------------------------------

	# Replace ___ with your code

	# create the Animal class
	class Animal:
		def eat(self):
			print("I can eat food")

	# create the Dog class
	class Dog(Animal):
		def bark(self):
			print("I can bark")
			super().eat()           # Invocación explícita sin self

	# create an object of the Dog class
	Mulder = Dog()

	# call the eat() method using the object
	Mulder.eat()


# -----------------------------------------------------------------------------------------

# When to use inheritance?

# If we are working on a large project, it's a good idea to use objects and classes whenever possible.

# If two types of objects in a project have is-a relationship, we can use inheritance. For example,

#     Dog is a Animal
#     Triangle is a Polygon
#     Quadrilateral is a Polygon
#     Student is a Person

# ----------------------------------------------------------------------------------------------------------
# ------------------- Programa para sumar dos distancias en m pies, n pulgadas.......con POO:-------------------------

	class Distance:
		# initialize feet and inches attributes
		def __init__(self, feet, inches):
			self.feet = feet
			self.inches = inches
		
		def add_distances(self, distance):							# Método para suma de componentes
			result_inches = self.inches + distance.inches
			result_feet = self.feet + distance.feet
			
			# while inch is 12 or greater,
			# increase feet by 1 and decrease inches by 12
			while (result_inches >= 12):								# Para poner ajuste de medida en m pies, n pulgadas
				result_feet = result_feet + 1
				result_inches = result_inches - 12 
				
			# create an object of Distance
			result_distance = Distance(result_feet, result_inches)
			return result_distance
			
	# create distance1 object
	distance1 = Distance(12, 8)				# Creando un objeto

	# create distance2 object
	distance2 = Distance(10, 6)				# Creando otro objeto

	# call add_distances using distance1 object
	# distance2 is used as argument
	result = distance1.add_distances(distance2)
	print(f'Result distance: {result.feet} ft {result.inches} inches')




# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------- Manejo de errores: ------- Excepciones: ----------------------------------


	try:
		# code that may cause exception
	except:
		# code to run when exception occurs

# ----- Ejemplo: --------

	try:
		numerator = int(input("Enter numerator: "))
		denominator = int(input("Enter denominator: "))

		result = numerator/denominator						# El denominador no puede ser cero

		print(result)
	except:
		print("Denominator cannot be 0. Try again.")



# ------------------------------------------------- Errores específicos:----------------------------------------


# Se debe consultar el error que genera en la consola para obtener la etiqueta de error específico como en éste caso:
# Se consulta la consola al momento de generarse el error:


IndexError                                Traceback (most recent call last)
~\AppData\Local\Temp/ipykernel_12320/1593889692.py in <module>
      7 index = int(input("Ingresa índice"))
      8 # print the item from the cars list
----> 9 print(cars[index])

IndexError: list index out of range				# De aquí se obtiene el error del cual se desea sacar la excepción.



# ------ Se pueden hacer excepciones para cada error: ------------------------------

	try:
		numerator = int(input("Enter numerator: "))
		denominator = int(input("Enter denominator: "))

		result = numerator/denominator
		print(result)
		
		my_list = [1, 2, 3]
		index = int(input("Enter index: "))

		print(my_list[index])

	# if ZeroDivisonError exception occurs,					# Se pueden poner dos o más excepciones en un código
	# run this code
	except ZeroDivisionError:									# La etiqueta se obtiene de la consola.
		print("Denominator cannot be 0. Try again.")

	# if IndexError exception occurs, run this code
	except IndexError:											# La etiqueta se obtiene de la consola.
		print("Index is wrong.")



# -----------------------------try...finally------------------------
# --------------------------------------------------------------------------------------------------------------------

	try:
		print(1/0)
	except:
		print("Wrong denominator")
	finally:
		print("Always printed")			# Esta parte siempre se ejecuta.


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Try ....catch form: ------			-----------------------------------------			-------------------------------




# ESTE TEMA QUEDA PENDIENTE DE VER......QUERARÁ A LA PRIMERA OPORTUNIDAD.




# -------------------------------------Trabajando con archivos: --------------------------------------------------------

# -----------------INPUT:----------------

	# open a file:
	f = open('message.txt', 'r')			# Abriendo archivo message.txt en modo lectura

	# read the file
	content = f.read()						# Leyendo el contenido y llenando una variable
	print(content)							# Imprimiendo contenido.

	# close the file
	f.close()						# Cerrando el archivo.


# ----------------------------------------------------------------------------------------------------------------------
# ------------- Leyendo los primeros 5 caracteres de un archivo: ---------------------------------------------

	f = open('message.txt', 'r')

	# read the first 5 characters
	content = f.read(5)
	print(content)

	f.close()

# -------------------------------------------------------------------------------------------------------------------
#------------------- try...finally in Files --------------------------

	try:
		f = open('message.txt', 'r')
		content = f.read()
		print(content)

	finally:
		# close the file
		f.close()					# Para asegurar que el archivo sea cerrado,				No importa lo que ocurra ariba.



# ----------- OUTPUT: -----------------------------


	with open('python.txt', 'w') as f:					# Creando un archivo inexistente.		Se abre en modo de escritura.
														# Si el archivo existe, éste se sobreescribe.

		f.write("I like Python.\n")				# Se pueden agregar cortes de línea.
		f.write("Files is easy.")


# --------------------- Agregando contenido SIN SOBREESCRIBIR, se conserva el contenido anterior del archivo: ----------------------

	# opening file in append mode
	with open('python.txt', 'a') as f:									# El modo append (a) evita que el contenido se sobreescriba, solo se agrega.
		f.write(' Appending data using the same write() method.')


# ----------------- Accediendo un archivo en una CARPETA DIFERENTE: -------------------------------------	

# Carpetas de ejemplo:

# main.py
# external
#   - messages.txt

	with open('external/messages.txt', 'r'):			# Ruta del archivo a abrir.
		f.read()



# ------------------------- Trabajando con directorios: -----------------------------------------------

	# Obteniendo la ruta actual:

	import os

	# print current working directory
	print(os.getcwd())

	# Output:
		# C:\Users\lenovo\Desktop\Files

# Cambiando de directorio de trabajo:

	import os

	# print current working directory
	print('Before CWD =',os.getcwd())

	# change current working directory
	os.chdir('D:/Projects')							# By the way, chdir means change directory.

	# print current working directory
	print('After CWD =', os.getcwd())

		# Before CWD = c:\Users\lenovo\Desktop\Files
		# After CWD = D:\Projects

# Listando todos los directorios y archivos dentro del directorio de trabajo:

	import os
	print(os.listdir())

# Obtener directorios y archhivos de una ruta específica:

	import os
	print(os.listdir('D:/Projects'))

# Creando un nuevo directorio:

	import os
	os.mkdir('test')

# Creando un nuevo directorio en una ruta específica:


	import os

	# change current working directory
	os.chdir('D:/Projects')

	os.mkdir('test')


# Renombrando un directorio: (El mismo que se creó anteriormente)

	import os

	# rename directory
	os.rename('test', 'new')

# Eliminando un directorio o un archivo: (2 METODOS)

	import os

	os.remove('hello.txt')

# -----

	import os

	os.rmdir('new')



# --------------	CREACION DE MODULOS ---------------:

	import math as m				# Manejando un "alias" para math
	
	# call sqrt() to get square root
	result = m.sqrt(9)
	print(f'result = {result}')

result = m.sqrt(9)


# .............................................
# .............................................




############################################################################################################################
# What is a Module?

# A module is a file containing a set of functions and statements. It's similar to other Python files that end with the .py file extension.

# Let's first create a file named **calculator.py** with these function:

	def add(a, b):
		return a + b
		
	def subtract(a, b):
		return a - b

	def multiply(a, b):
		return a * b
		
	def divide(a, b):
		return a / b 

# This **calculator.py** file itself is a module. Now, let's import this file from another file named **main.py**.

	import calculator

	result1 = calculator.add(2, 3)							#### Modulo.Función
	print(result1)   # 5

	result3 = calculator.multiply(10, 3)					#### Modulo.Función
	print(result3)   # 30

# After we use this statement import calculator, we can use all the functions and statements defined inside the calculator module.

# Then, we have used the add() function of the calculator.py file using calculator.add().

# Similarly, we have used the multiply() function of the calculator.py file using calculator.multiply()


# .............................................
# .............................................

# Generador de Código QR:

# Previamente:

# Escribir en la (((línea de comandos))):

	pip install pyqrcode


## Posterior a la instalación:


	# import the pyqrcode  module after you install it
	import pyqrcode

	# take user input
	# this is the text for which we want to generate a QR code
	text = input("Enter the text to generate QR code: ")

	# create a pyqrcode object by calling the create() method
	# we will use our text as an argument
	qr_code = pyqrcode.create(text)

	# calling the svg() method of the qr_code object 
	# creates the file named qr_code.svg in svg format
	# the scale argument sets how large to draw a single image
	qr_code.svg('qr_code.svg', scale = 8)

# Salida:

	# Enter the text to generate QR code: https://www.programiz.pro

	# After we enter the text, this code geneters a file named qr_code.svg in the current location, and the image will be a QR code.


# -------------------- Ejemplos de entrevista: ----------------------------------


# ------------ Determina que elementos se repiten más: ---------

# define a function that returns the majority element
def find_majority_element(num_list):

    # loop through each number in a list
    for num in num_list:

        # if the number of times a number appears,
        # is greater than the length of the list divided by 2,
        # return the number
        if num_list.count(num) > len(num_list) // 2:
            return num

# cal the function
numbers = [1, 7, 8, 7, 7, 7]
result = find_majority_element(numbers)
print(result)

# -----------------------------------------------
# ----- Otra manera de revisar que elemento se repite más: -----------


# Para revisar que elemento se repite más veces

from collections import Counter         # Modulo para contar cosas en colecciones de Python

a = [1, 7, 8, 7, 7, 7, 2, 2]
counter = Counter(a)            # Se crea un objeto (Se crea una instancia del método de Python)

most_counted = counter.most_common()        # Se invoca la función a travéz del objeto (instancia)

primer = most_counted[0]        # Extrayendo la tupla mas repetida
segundo = primer[0]             # Extrayendo el elemento mas repetido

print(segundo)


# -----------------------------------------------------------
# ----- Programa que calcula la suma del mínimo + máximo elemento de una lista: ---------

# define a function
def calc_sum(num_list):

    # find the smallest number
    min_num = min(num_list)				# Mínimo

    # find the largest number
    max_num = max(num_list)				# Máximo

    # find the sum
    total = min_num + max_num			# Suma total

    return total


numbers = [5, 6, 3, 8, 9]

result = calc_sum(numbers)

print(result)

# -----------------------------------------------------
# Suma de todos los elementos de una lista.

numbers = [5, 6, 7, 8, 23, 51]
sumando = 0

for i in numbers:
    sumando += i

print(sumando)

# ---------------------------------------------------

# Suma mas facil de todos los elementos de una lista

numbers = [5, 6, 7, 8, 23, 51]
print(sum(numbers))

# -------------------------------------------------

# Agregar un elemento al final de una lista:

# create a list of numbers
num_list = [5, 2, 13, 72, 4]
 
# add 5 to the list
num_list.append(5)
print(num_list)


# ----------------------------------------------
# Concatenando dos listas:

# define two separate lists
list1 = ["apple", "orange", "banana"]
list2 = [5, 8, 10]
 
# concat those lists using + operator
merged_list = list1 + list2
 
# print the merged_list
print(merged_list)

# ----------------------------------------------
# Invirtiendo el orden de una lista:

# define a list
num_list = [5, 8, 4, 7, 1, 23, 6]

# reverse the list using the slicing method
# and store it in reversed_list
reversed_list = num_list[::-1]					# Inicio:final:Step

# print the reversed_list
print(reversed_list)

# -----------------------------------------------------------------------
# Remover las vocales de una cadena

# Remove vowels from the string

string = "A quick brown fox jumps over the lazy dog"
vocales = "aeiouAEIOU"


for i in string:
    if i in vocales:
        # print("vocal:",i)
        string = string.replace(i,"")

print(string)


# --------------------------------------------------------

# Conteo de vocales y consonantes

# Remove vowels from the string

string = "A quick brown fox jumps over the lazy dog"
vocales = "aeiouAEIOU"

voc = 0
cons = 0


for i in string:
    if i in vocales:
        # print("vocal:",i)
        voc += 1
    elif i == " ":
        continue			# Los espacios no cuentan
    else:
        cons += 1

print("Vocales:",voc)
print("Consonantes:",cons)

# ------------------------------------------------

# Multiplicando enteros almacenados en cadenas:

# -----------------------------------------------

# Contando el número de letras mayusculas en una oración:

# define a function that counts the capital letters in a string
def count_capitals(string):

    # initialize a counter
    capital_counter = 0

    # loop through the string
    for char in string:

        # take the ASCII value of the character and
        # check if it is a capital letter
        if ord(char) >= 65 and ord(char) <= 90:
            capital_counter += 1

    # return the counter
    print(capital_counter)


# call the function
count_capitals("The Sum gives UV light")

# ----------------------------------------------------

# Uniendo en una sola cadena una lista de cadenas:

lista = ["Hello", "world", "from", "python"]
cadena = ""

for i in lista:
    cadena += i
    cadena += " "

print(cadena)


# ---------------------------------------------

# Lo mismo que el anterior de manera más elegante:

# define a list
words = ["Hello", "world", "from", "python"]
 
# join the list items with space in between
sentence = " ".join(words)							# Función JOIN es la clave aquí.
 
# print the sentence
print(sentence)

# -----------------------------------------------
a
