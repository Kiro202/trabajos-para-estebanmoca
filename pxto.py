import os
import win32com.client
import pyodbc


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ruta_excel = os.path.join(BASE_DIR, "FacturaDetalles.xlsx")
ruta_db = os.path.join(BASE_DIR, "Factura.accdb")

#creamos labase de datos
ruta = ruta_db

if not os.path.exists(ruta):
    access = win32com.client.Dispatch("Access.Application")
    access.NewCurrentDatabase(ruta)
    access.Quit()

print("Base de datos creada")
#nos conectamos


conn = pyodbc.connect(
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Desktop\apocalipsis\tatan\tarea_comandos\Factura.accdb;'
)
cursor = conn.cursor()


def tabla_existe(cursor, nombre_tabla):
    tablas = [row.table_name for row in cursor.tables(tableType='TABLE')]
    return nombre_tabla in tablas
tablas = {

    "Personas": """
    CREATE TABLE Personas (
        persona_id AUTOINCREMENT PRIMARY KEY,
        nombre TEXT,
        apellido TEXT,
        correo TEXT,
        telefono TEXT
    )
    """,

    "Productos": """
    CREATE TABLE Productos (
        producto_id AUTOINCREMENT PRIMARY KEY,
        nombre TEXT,
        precio DOUBLE,
        stock INTEGER
    )
    """,

    "Vendedor": """
    CREATE TABLE Vendedor (
        vendedor_id AUTOINCREMENT PRIMARY KEY,
        persona_id INTEGER,
        sueldo DOUBLE,
        fechaIngreso DATETIME
    )
    """,

    "Clientes": """
    CREATE TABLE Clientes (
        cliente_id AUTOINCREMENT PRIMARY KEY,
        persona_id INTEGER,
        fechaRegistro DATETIME
    )
    """,

    "Factura_Encabezado": """
    CREATE TABLE Factura_Encabezado (
        factura_id AUTOINCREMENT PRIMARY KEY,
        cliente_id INTEGER,
        vendedor_id INTEGER,
        fecha DATETIME
    )
    """,

    "Factura_Detalles": """
    CREATE TABLE Factura_Detalles (
        detalle_id AUTOINCREMENT PRIMARY KEY,
        factura_id INTEGER,
        producto_id INTEGER,
        cantidad INTEGER,
        valor_unitario DOUBLE,
        valor_total_sin_iva DOUBLE,
        valor_total_con_iva DOUBLE
    )
    """
}
for nombre, query in tablas.items():
    if not tabla_existe(cursor, nombre):
        cursor.execute(query)
        print(f"✅ Tabla '{nombre}' creada")
    else:
        print(f"⚠️ Tabla '{nombre}' ya existe")
conn.commit()
def crear_relaciones(cursor):
    relaciones = [

        # Vendedor → Personas
        """
        ALTER TABLE Vendedor
        ADD CONSTRAINT fk_vendedor_persona
        FOREIGN KEY (persona_id) REFERENCES Personas(persona_id)
        """,

        # Clientes → Personas
        """
        ALTER TABLE Clientes
        ADD CONSTRAINT fk_cliente_persona
        FOREIGN KEY (persona_id) REFERENCES Personas(persona_id)
        """,

        # Factura_Encabezado → Clientes
        """
        ALTER TABLE Factura_Encabezado
        ADD CONSTRAINT fk_factura_cliente
        FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id)
        """,

        # Factura_Encabezado → Vendedor
        """
        ALTER TABLE Factura_Encabezado
        ADD CONSTRAINT fk_factura_vendedor
        FOREIGN KEY (vendedor_id) REFERENCES Vendedor(vendedor_id)
        """,

        # Factura_Detalles → Factura
        """
        ALTER TABLE Factura_Detalles
        ADD CONSTRAINT fk_detalle_factura
        FOREIGN KEY (factura_id) REFERENCES Factura_Encabezado(factura_id)
        """,

        # Factura_Detalles → Productos
        """
        ALTER TABLE Factura_Detalles
        ADD CONSTRAINT fk_detalle_producto
        FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
        """
    ]

    for r in relaciones:
        try:
            cursor.execute(r)
            print("✅ Relación creada")
        except Exception:
            print("⚠️ Relación ya existe o error ignorado")
crear_relaciones(cursor)
conn.commit()
def insertar_excel(cursor, conn, ruta_excel):
    import openpyxl

    wb = openpyxl.load_workbook(ruta_excel)
    ws = wb.active

    vendedores = {}
    clientes = {}
    productos = {}
    facturas = {}

    for row in ws.iter_rows(min_row=2, values_only=True):

        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        factura_cod  = row[0]
        fecha        = row[1]
        vendedor_cod = row[2]
        cliente_cod  = str(row[3])
        prod_codigo  = str(row[4])
        prod_nombre  = row[5]
        cantidad     = row[6]
        precio_unit  = row[7]
        valor        = row[8]
        neta_pagar   = row[10]

        # VENDEDOR
        if vendedor_cod not in vendedores:
            cursor.execute("INSERT INTO Personas (nombre, apellido, correo, telefono) VALUES (?, ?, ?, ?)",
                           (vendedor_cod, "Pendiente", "correo", "000"))
            cursor.execute("SELECT @@IDENTITY")
            persona_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO Vendedor (persona_id, sueldo, fechaIngreso) VALUES (?, ?, ?)",
                           (persona_id, 0, fecha))
            cursor.execute("SELECT @@IDENTITY")
            vendedores[vendedor_cod] = cursor.fetchone()[0]

        # CLIENTE
        if cliente_cod not in clientes:
            cursor.execute("INSERT INTO Personas (nombre, apellido, correo, telefono) VALUES (?, ?, ?, ?)",
                           (cliente_cod, "Pendiente", "correo", "000"))
            cursor.execute("SELECT @@IDENTITY")
            persona_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO Clientes (persona_id, fechaRegistro) VALUES (?, ?)",
                           (persona_id, fecha))
            cursor.execute("SELECT @@IDENTITY")
            clientes[cliente_cod] = cursor.fetchone()[0]

        # PRODUCTO
        if prod_codigo not in productos:
            cursor.execute("INSERT INTO Productos (nombre, precio, stock) VALUES (?, ?, ?)",
                           (prod_nombre, precio_unit, 0))
            cursor.execute("SELECT @@IDENTITY")
            productos[prod_codigo] = cursor.fetchone()[0]

        # FACTURA
        if factura_cod not in facturas:
            cursor.execute("INSERT INTO Factura_Encabezado (cliente_id, vendedor_id, fecha) VALUES (?, ?, ?)",
                           (clientes[cliente_cod], vendedores[vendedor_cod], fecha))
            cursor.execute("SELECT @@IDENTITY")
            facturas[factura_cod] = cursor.fetchone()[0]

        # DETALLE
        cursor.execute("""
            INSERT INTO Factura_Detalles 
            (factura_id, producto_id, cantidad, valor_unitario, valor_total_sin_iva, valor_total_con_iva)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            facturas[factura_cod],
            productos[prod_codigo],
            cantidad,
            precio_unit,
            valor,
            neta_pagar
        ))

    conn.commit()
    print("🔥 Datos insertados correctamente")
insertar_excel(cursor, conn, ruta_excel)
#ruta_excel