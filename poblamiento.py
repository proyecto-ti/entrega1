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


loc = ("Productos.xlsx")
wb = xlrd.open_workbook(loc)
sheet_productos = wb.sheet_by_index(0)
sheet_ingredientes = wb.sheet_by_index(1)
sheet_recetas = wb.sheet_by_index(2)
sheet_asignacion = wb.sheet_by_index(3)
sheet_stock = wb.sheet_by_index(4)

lista_productos = []

for fila in range(1,78):
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


for fila in range(1,23):
	sku = int(sheet_stock.cell_value(fila, 0))
	for element in lista_productos:
		if element.sku == sku :
			element.stock_minimo = int(sheet_stock.cell_value(fila, 3))

for element in lista_productos:
	print(element.stock_minimo)









