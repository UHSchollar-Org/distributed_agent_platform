import requests

operand1 = 2
operand2 = 3
operator = "+"

# Hacer una solicitud GET a la ruta "/mi_api" en el servidor local en el puerto 5000
response = requests.get(f'http://localhost:5000/calculator?num1={operand1}&num2={operand2}&operator=%2B')

# Obtener el contenido de la respuesta
content = response.content

# Imprimir el contenido de la respuesta
print(content)