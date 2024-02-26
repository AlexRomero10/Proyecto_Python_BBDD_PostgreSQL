import psycopg2


def Conectar_BD(host, usuario, password, database):
    try:
        db = psycopg2.connect(
            host=host,
            user=usuario,
            password=password,
            database=database
        )

        return db
    except psycopg2.Error as e:
        print("No puedo conectar a la base de datos:", e)
        return None

def MostrarMenu():
    menu = '''
    1- Muestra el nombre de cada empresa junto con su respectiva localidad.
    2- Muestra cargos que empiecen por una subcadena especificada.
    3- Pide por teclado un nombre de empleado y muestre la descripcion del area de trabajo asociada a ese empleado 
    4- Pide por teclado los datos de una nueva empresa. Luego, inserta los datos en la tabla empresa y muestra una tabla actualizada con toda la informacion de la tabla empresa.
    5- Elimina todos los cargos cuyos nombres comienzan con un prefijo especifico.
    6- Actualiza la informacion de la descripcion de la tabla area de trabajo solicitando al usuario el codigo de area de trabajo y el nombre que desea actualizar.
    7- Salir
    '''
    print(menu)
    while True:
        try:
            opcion=int(input("Selecciona una opción: "))
            while opcion<1 or opcion>7:
                print("Error, el número de la opción debe estar comprendido entre el 1 y el 7")
                opcion=int(input("\nSelecciona una opción: "))
            return opcion
        except:
            print("Error, la opción debe de ser un número.\n")

#Ejercicio1
def mostrar_empresas_por_localidad(db):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT Localidad, Nombre FROM EMPRESA ORDER BY Localidad, Nombre")
        resultados = cursor.fetchall()
        localidad_actual = None
        for localidad, nombre_empresa in resultados:
            if localidad != localidad_actual:
                print(f"Empresa: {nombre_empresa}")
                localidad_actual = localidad
            print(f"Localidad: {localidad}")
    except Exception as e:
        print("Se ha producido un error al ejecutar la consulta:", e)
    finally:
        cursor.close()

#Ejercicio2
def buscar_cargos(conexion, subcadena):
    cursor = conexion.cursor()
    consulta = ("SELECT Cargo FROM persona_de_contacto WHERE Cargo LIKE %s")
    cursor.execute(consulta, (subcadena + '%',))

    cargos_encontrados = cursor.fetchall()

    if cargos_encontrados:
        print("Cargos encontrados que comienzan con '{}':".format(subcadena))
        for cargo in cargos_encontrados:
            print(cargo[0])
    else:
        print("No se encontraron cargos que comiencen con '{}".format(subcadena))


#Ejercicio3
def mostrar_area_trabajo_empleado(db, nombre_empleado):
    try:
        cursor = db.cursor()
        sql = """SELECT Nombre, Descripcion
                 FROM areatrabajo
                 WHERE ID_AreaTrabajo = (
                     SELECT ID_AreaTrabajo
                     FROM areatrabajo
                     WHERE Nombre = %s
                 )"""
        cursor.execute(sql, (nombre_empleado,))
        resultado = cursor.fetchone()
        if resultado:
            print(f"Área de trabajo de {nombre_empleado}:")
            print(f"Nombre: {resultado[0]}\nDescripción: {resultado[1]}")
        else:
            print(f"No se encontró información del área de trabajo para {nombre_empleado}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

#Ejercicio4
def agregar_empresa(db, cif, nombre, direccion, localidad):
    cursor = db.cursor()
    sql = "INSERT INTO empresa (cif, nombre, direccion, localidad) VALUES (%s, %s, %s, %s)"  # Corregido el nombre de la tabla a 'empresa'
    val = (cif, nombre, direccion, localidad)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "empresa insertada.")

def actualizar_tabla_empresa(db):
    cursor = db.cursor()
    sql = "SELECT * FROM empresa"
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        print("TABLA ACTUALIZADA EMPRESA:")
        for result in registros:
            print("CIF:", result[0])
            print("Nombre:", result[1])
            print("Direccion:", result[2])
            print("Localidad:", result[3])
            print("----------------------")
    except:
        print("Se ha producido un error al mostrar la tabla.")

#Ejercicio5
def eliminar_personas_por_prefijo(db, prefijo):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM persona_de_contacto WHERE Cargo LIKE %s"
        cursor.execute(sql, (prefijo + '%',))
        filas_afectadas = cursor.rowcount
        print(f"Se han eliminado {filas_afectadas} registros donde el nombre comienza con '{prefijo}'.")
        db.commit()
    except:
        print("Se ha producido un error al eliminar los clientes.")
        db.rollback()
def actualizar_tabla_persona_contacto(db):
    cursor = db.cursor()
    sql = "SELECT * FROM persona_de_contacto"
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        print("TABLA ACTUALIZADA PERSONA DE CONTACTO:")
        for result in registros:
            print("Codigo_ContactoEmpresa:", result[0])
            print("Cargo:", result[1])
            print("Nombre:", result[2])
            print("Correo_electronico:", result[3])
            print("CIF:", result[4])
            print("----------------------")
    except:
        print("Se ha producido un error al mostrar la tabla.")

#Ejercicio6
def actualizar_area_trabajo(db, ID_AreaTrabajo, campo, nuevo_valor):
    sql = "UPDATE areatrabajo SET Nombre = %s WHERE ID_AreaTrabajo = %s"
    try:
        cursor = db.cursor()
        cursor.execute(sql, (nuevo_valor, ID_AreaTrabajo))
        db.commit()
        print("La información ha sido actualizada correctamente.")
    except Exception as e:
        db.rollback()
        print("No se ha podido actualizar la información:", e)

def actualizar_tabla_area_trabajo(db):
    cursor = db.cursor()
    sql = "SELECT * FROM areatrabajo"
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        print("TABLA ACTUALIZADA PERSONA DE CONTACTO:")
        for result in registros:
            print("ID_AreaTrabajo:", result[0])
            print("Nombre:", result[1])
            print("Descripcion:", result[2])
            print("----------------------")
    except:
        print("Se ha producido un error al mostrar la tabla.")