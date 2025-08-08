#!/bin/bash
# Comandos de actualización para snippets de the-way
# IMPORTANTE: Revisar cada comando antes de ejecutar

# === ACTUALIZAR SNIPPET #109 ===
# Descripción actual: Snippet 1: Ejemplo de código Python de referencia
# Descripción mejorada: Interacción Básica Con Usuario (entrada: texto, salida: texto) - números, entrada-usuario, salida-datos [ejemplo integrado]
# Tags actuales: referencia:python:nivel-beginner:tema-variables:tema-strings:facil:
# Tags mejorados: python:referencia:nivel-muy-facil:tema-números:tema-entrada-usuario:tema-salida-datos:ejemplo-integrado:

# 1. Crear archivo temporal con el contenido:
cat > temp_snippet_109.py << 'EOF'
print("Ingresa tu nombre:")
numero = input()
EOF

# 2. Eliminar snippet actual:
/home/joselillo/.cargo/bin/the-way delete 109

# 3. Importar con nueva descripción:
/home/joselillo/.cargo/bin/the-way import temp_snippet_109.py --description \"Interacción Básica Con Usuario (entrada: texto, salida: texto) - números, entrada-usuario, salida-datos [ejemplo integrado]\" --tags \"python:referencia:nivel-muy-facil:tema-números:tema-entrada-usuario:tema-salida-datos:ejemplo-integrado:\"

# 4. Limpiar archivo temporal:
rm temp_snippet_109.py

# ========================================

# === ACTUALIZAR SNIPPET #110 ===
# Descripción actual: Snippet 2: Ejemplo de código Python de referencia
# Descripción mejorada: Operaciones Básicas De Python - números
# Tags actuales: referencia:python:nivel-intermediate:facil:
# Tags mejorados: python:referencia:nivel-muy-facil:tema-números:concepto-básico:

# 1. Crear archivo temporal con el contenido:
cat > temp_snippet_110.py << 'EOF'
float(numero) + 5
EOF

# 2. Eliminar snippet actual:
/home/joselillo/.cargo/bin/the-way delete 110

# 3. Importar con nueva descripción:
/home/joselillo/.cargo/bin/the-way import temp_snippet_110.py --description \"Operaciones Básicas De Python - números\" --tags \"python:referencia:nivel-muy-facil:tema-números:concepto-básico:\"

# 4. Limpiar archivo temporal:
rm temp_snippet_110.py

# ========================================

# === ACTUALIZAR SNIPPET #111 ===
# Descripción actual: Snippet 3: Ejemplo de código Python de referencia
# Descripción mejorada: Interacción Usuario Con Bucles (entrada: texto, salida: texto) - listas, números, bucles-for [ejemplo completo]
# Tags actuales: referencia:python:nivel-beginner:tema-variables:tema-loops:tema-lists:facil:
# Tags mejorados: python:referencia:nivel-facil:tema-listas:tema-números:tema-bucles-for:tema-entrada-usuario:ejemplo-completo:

# 1. Crear archivo temporal con el contenido:
cat > temp_snippet_111.py << 'EOF'
listas  = []

print("Ingresa 5 números")
for i in range(5):
	listas.append(input("Ingresa número: "))
print("Numeros ingresados:",listas)
EOF

# 2. Eliminar snippet actual:
/home/joselillo/.cargo/bin/the-way delete 111

# 3. Importar con nueva descripción:
/home/joselillo/.cargo/bin/the-way import temp_snippet_111.py --description \"Interacción Usuario Con Bucles (entrada: texto, salida: texto) - listas, números, bucles-for [ejemplo completo]\" --tags \"python:referencia:nivel-facil:tema-listas:tema-números:tema-bucles-for:tema-entrada-usuario:ejemplo-completo:\"

# 4. Limpiar archivo temporal:
rm temp_snippet_111.py

# ========================================

# === ACTUALIZAR SNIPPET #112 ===
# Descripción actual: Snippet 4: Ejemplo de código Python de referencia
# Descripción mejorada: Salida Simple De Datos (salida: texto) - números, salida-datos [ejemplo integrado]
# Tags actuales: referencia:python:nivel-intermediate:tema-strings:facil:
# Tags mejorados: python:referencia:nivel-muy-facil:tema-números:tema-salida-datos:ejemplo-integrado:

# 1. Crear archivo temporal con el contenido:
cat > temp_snippet_112.py << 'EOF'
print("Hola a todos mis amigos")
EOF

# 2. Eliminar snippet actual:
/home/joselillo/.cargo/bin/the-way delete 112

# 3. Importar con nueva descripción:
/home/joselillo/.cargo/bin/the-way import temp_snippet_112.py --description \"Salida Simple De Datos (salida: texto) - números, salida-datos [ejemplo integrado]\" --tags \"python:referencia:nivel-muy-facil:tema-números:tema-salida-datos:ejemplo-integrado:\"

# 4. Limpiar archivo temporal:
rm temp_snippet_112.py

# ========================================

# === ACTUALIZAR SNIPPET #113 ===
# Descripción actual: Snippet 5: Ejemplo de código Python de referencia
# Descripción mejorada: Formateo De Strings - diccionarios, formateo-strings [ejemplo integrado]
# Tags actuales: referencia:python:nivel-beginner:tema-variables:tema-dictionaries:tema-strings:facil:
# Tags mejorados: python:referencia:nivel-muy-facil:tema-diccionarios:tema-formateo-strings:ejemplo-integrado:

# 1. Crear archivo temporal con el contenido:
cat > temp_snippet_113.py << 'EOF'
variable = 'Joselillo Castillo'
otra = 'Genios estudiantes'

forma = "El profesor '{}' y sus '{}'".format(variable,otra)

# Retorna lo siguiente:
EOF

# 2. Eliminar snippet actual:
/home/joselillo/.cargo/bin/the-way delete 113

# 3. Importar con nueva descripción:
/home/joselillo/.cargo/bin/the-way import temp_snippet_113.py --description \"Formateo De Strings - diccionarios, formateo-strings [ejemplo integrado]\" --tags \"python:referencia:nivel-muy-facil:tema-diccionarios:tema-formateo-strings:ejemplo-integrado:\"

# 4. Limpiar archivo temporal:
rm temp_snippet_113.py

# ========================================
