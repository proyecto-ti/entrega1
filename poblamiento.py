import xlrd

class Producto:
	def __init__(self,sku,nombre,precio,duracion,equivalencia,unidad,lote,tiempo):
		self.sku = sku
		self.nombre = nombre
		self.precio = precio
		self.duracion = duracion
		self.equivalencia = equivalencia
		self.unidad = unidad 
		self.lote = lote
		self.tiempo = tiempo
		self.productores = []
		self.stock_minimo = None
		self.propio = False # si nuestro grupo lo produce
		self.receta = {}


loc = ("Productos.xlsx")
wb = xlrd.open_workbook(loc)
sheet_productos = wb.sheet_by_index(0)
sheet_ingredientes = wb.sheet_by_index(1)
sheet_recetas = wb.sheet_by_index(2)
sheet_asignacion = wb.sheet_by_index(3)
sheet_stock = wb.sheet_by_index(4)

lista_productos = []

for fila in range(1,79):
	sku = int(sheet_productos.cell_value(fila, 0))
	nombre = str(sheet_productos.cell_value(fila, 1))
	precio = (sheet_productos.cell_value(fila, 3))
	duracion = int(sheet_productos.cell_value(fila, 6))
	equivalencia = float(sheet_productos.cell_value(fila, 7))
	unidad = str(sheet_productos.cell_value(fila, 8))
	lote = int(sheet_productos.cell_value(fila, 9))
	tiempo = int(sheet_productos.cell_value(fila, 10))
	productores = str((sheet_productos.cell_value(fila, 11))).split(",")
	productores2 = []
	for element in productores:
		productores2.append((int(element)))
	a = Producto(sku,nombre,precio,duracion,equivalencia,unidad,lote,tiempo)
	a.productores.extend(productores2)
	if 2 in a.productores:
		a.propio = True
	lista_productos.append(a)


for fila in range(1,24):
	sku = int(sheet_stock.cell_value(fila, 0))
	for element in lista_productos:
		if element.sku == sku :
			element.stock_minimo = int(sheet_stock.cell_value(fila, 3))

lista_ingredientes = []
for fila in range(1,192):
	sku1 = int(sheet_ingredientes.cell_value(fila, 0))
	sku2 = int(sheet_ingredientes.cell_value(fila, 2))
	valor = int(sheet_ingredientes.cell_value(fila, 9))
	lista =[sku1,sku2,valor]
	lista_ingredientes.append(lista)

for element in lista_ingredientes:
	for elemento in lista_productos:
		if elemento.sku == element[0]:
			elemento.receta[element[1]] = element[2]

for element in lista_productos:	
	print(element.receta)

















