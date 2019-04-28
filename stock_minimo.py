import xlrd
loc = ("Datos.xlsx")
wb = xlrd.open_workbook(loc)
sheet_productos = wb.sheet_by_index(0)
sheet_ingredientes = wb.sheet_by_index(1)
sheet_recetas = wb.sheet_by_index(2)
sheet_asignacion = wb.sheet_by_index(3)
sheet_stock = wb.sheet_by_index(4)



stock_minimo = {}