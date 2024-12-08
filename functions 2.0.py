import mysql.connector
from pymongo import MongoClient
import datetime
db_config = {
    "host": "localhost",
    "user": "informatica1",
    "password": "info20242",
    "database":"SistemaMedico"
}
def rango(min_val, max_val, msj, u):
    while True:
        try:
            valor = float(input(f"{msj} ({u}, rango {min_val}-{max_val}): "))
            if min_val <= valor <= max_val:
                return valor
            print(f"El valor debe estar entre {min_val} y {max_val}.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
def iny_mysql():
    db_name = "SistemaMedico"
    ex_tab = ["usuarios", "pacientes", "diagnosticos"]
    data_inserts = {
        "usuarios": [
            ("Miguel_Iglesia", "KarateKid", "tecnico"),
            ("Franchesca_01", "12_Reinaldo", "medico"),
            ("Apolit0", "Bell000", "administrador")
        ],
        "pacientes": [
            ("Juan Perez", 35, "Masculino"),
            ("Maria Lopez", 28, "Femenino")
        ],
        "diagnosticos": [
            (1, 'MRI', 'Cabeza', 'Tumor cerebral', 85, 'Se observa una masa irregular en la región frontal, que podría sugerir un tumor.', 'Se recomienda realizar una biopsia para confirmar diagnóstico.', '2024-12-01', 'Confirmado'),
            (2, 'Rayos X', 'Pulmones', 'Neumonía', 70, 'Hay signos de consolidación en los pulmones, compatible con neumonía bacteriana.', 'Se ha iniciado tratamiento con antibióticos y se monitoriza al paciente.', '2024-12-05', 'Pendiente')
        ]
    }
    create_tab = {
        "usuarios": """
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role ENUM('administrador', 'medico', 'tecnico') NOT NULL
            );
        """,
        "pacientes": """
            CREATE TABLE IF NOT EXISTS pacientes (
                paciente_id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                edad INT NOT NULL,
                genero ENUM('Masculino', 'Femenino') NOT NULL
            );
        """,
        "diagnosticos":"""
        CREATE TABLE IF NOT EXISTS diagnosticos (
            diagnostico_id INT AUTO_INCREMENT PRIMARY KEY,
            paciente_id INT NOT NULL,
            tipo_imagen ENUM('MRI', 'CT', 'Rayos X') NOT NULL,
            parte_cuerpo VARCHAR(255) NOT NULL,
            condicion_sugerida VARCHAR(255) NOT NULL,
            probabilidad INT NOT NULL,
            notas_ia TEXT NOT NULL,
            comentarios_medico TEXT NOT NULL,
            fecha_diagnostico DATE NOT NULL,
            estado ENUM('Pendiente', 'Confirmado', 'Descartado') NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(paciente_id)
        );
        """
    }

    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"]
        )
        cursor = conexion.cursor()

        # Verificar si la base de datos existe
        cursor.execute("SHOW DATABASES;")
        databases = [db[0] for db in cursor.fetchall()]
        if db_name not in databases:
            print(f"La base de datos '{db_name}' no existe. Creándola...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            print(f"Base de datos '{db_name}' creada exitosamente.")
        else:
            print(f"La base de datos '{db_name}' ya existe.")
        
        # Usar la base de datos
        cursor.execute(f"USE {db_name};")
        
        # Crear tablas si no existen
        cursor.execute("SHOW TABLES;")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        for table_name in ex_tab:
            if table_name in existing_tables:
                print(f"La tabla '{table_name}' ya existe.")
            else:
                print(f"La tabla '{table_name}' no existe. Creándola...")
                cursor.execute(create_tab[table_name])
                print(f"Tabla '{table_name}' creada exitosamente.")
        
        # Insertar los usuarios
        for record in data_inserts["usuarios"]:
            query = "INSERT IGNORE INTO usuarios (username, password, role) VALUES (%s, %s, %s);"
            cursor.execute(query, record)
        
        # Insertar pacientes y obtener sus IDs
        paciente_ids = {}
        for record in data_inserts["pacientes"]:
            query = "INSERT INTO pacientes (nombre, edad, genero) VALUES (%s, %s, %s);"
            cursor.execute(query, record)
            paciente_id = cursor.lastrowid  # Obtener el paciente_id generado
            paciente_ids[record[0]] = paciente_id  # Guardar el id del paciente
            print(f"Paciente insertado: {record[0]} con paciente_id {paciente_id}")
        
        # Verificar que los pacientes se insertaron correctamente
        print(f"paciente_ids: {paciente_ids}")

        # Insertar los diagnósticos con los paciente_ids correctos
        for record in data_inserts["diagnosticos"]:
            paciente_id = paciente_ids.get(f"Juan Perez" if record[0] == 1 else "Maria Lopez")  # Recuperar el paciente_id correcto
            print(f"Insertando diagnóstico para paciente_id: {paciente_id}")
            
            query = """
                INSERT INTO diagnosticos 
                (paciente_id, tipo_imagen, parte_cuerpo, condicion_sugerida, 
                probabilidad, notas_ia, comentarios_medico, fecha_diagnostico, estado) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (paciente_id, *record[1:]))
        
        # Confirmar los cambios
        conexion.commit()
        print("Datos iniciales insertados exitosamente.")
    
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err.msg} (Código: {err.errno})")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()
def con_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    return client["sistema_medico"]
def con_db():
    return mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
def rev_num(msj):
    while True:
        try:
            x=int(input(msj))
            return x
        except:
            print("Ingrese un numero valido")
def rev_fecha(date):
    while True:
        try:
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            return fecha.strftime("%Y-%m-%d")
        except ValueError:
            print("Formato incorrecto, ingrese la fecha nuevamente (YYYY-MM-DD):")
            date = input()
def login():
    username = input("Ingrese su nombre de usuario: ").strip()
    password = input("Ingrese su contraseña: ").strip()
    connection = con_db()
    cursor = connection.cursor()
    try:
        query = "SELECT password, role FROM usuarios WHERE username = %s"
        cursor.execute(query, (username,))
        re= cursor.fetchone()
        if re:
            s_password, role = re
            if s_password == password:
                print(f"Login exitoso. Rol: {role}")
                return username,role
            else:
                print("Contraseña incorrecta.")
        else:
            print("Usuario no encontrado.")
        return None
    except Exception as e:
        print(f"Error al autenticar al usuario: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
def create_pac():
    nombre = input("Ingrese el nombre del paciente: ").strip()
    edad = rev_num("Ingrese la edad del paciente: ")
    
    while True:
        print("1. Femenino\n2. Masculino")
        num_gen = rev_num("Ingrese el género del paciente: ")
        if num_gen == 1:
            genero = "Femenino"
            break
        elif num_gen == 2:
            genero = "Masculino"
            break
        else:
            print("Opción no válida. Intente de nuevo.")
    
    connection = con_db()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO pacientes (nombre, edad, genero) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, edad, genero))
        connection.commit()
        print(f"Paciente {nombre} creado con éxito.")
    except Exception as e:
        print(f"Error al crear el paciente: {e}")
    finally:
        cursor.close()
        connection.close()
def read_pac():
    paciente_id = rev_num("Ingrese el ID del paciente: ")
    connection = con_db()
    cursor = connection.cursor()
    try:
        query_paciente = "SELECT * FROM pacientes WHERE paciente_id = %s"
        cursor.execute(query_paciente, (paciente_id,))
        paciente = cursor.fetchone()
        if paciente:
            print(f"Paciente encontrado:\nID: {paciente[0]}\nNombre: {paciente[1]}\nEdad: {paciente[2]}\nGénero: {paciente[3]}")
            query_diagnosticos = "SELECT * FROM diagnosticos WHERE paciente_id = %s"
            cursor.execute(query_diagnosticos, (paciente_id,))
            diagnosticos = cursor.fetchall()

            if diagnosticos:
                print("\nHistorial de Diagnósticos:")
                for diag in diagnosticos:
                    print(f"ID Diagnóstico: {diag[0]}\nTipo de Imagen: {diag[2]}\nResultado IA: {diag[3]}\nFecha: {diag[4]}\nEstado: {diag[5]}\n")
            else:
                print("No se encontraron diagnósticos para este paciente.")
        else:
            print("Paciente no encontrado.")
    except Exception as e:
        print(f"Error al leer el paciente o el historial de diagnósticos: {e}")
    finally:
        cursor.close()
        connection.close()
def act_pac():
    paciente_id = rev_num("Ingrese el ID del paciente: ")
    connection = con_db()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM pacientes WHERE paciente_id = %s"
        cursor.execute(query, (paciente_id,))
        result = cursor.fetchone()
        if not result:
            print("Paciente no encontrado.")
        else:
            while True:
                print(f"Datos actuales:\nNombre: {result[1]}\nEdad: {result[2]}\nGénero: {result[3]}")
                print("\n¿Qué deseas actualizar?\n1. Nombre\n2. Edad\n3. Género")
                opc = rev_num("Ingrese el número de la opción que desea actualizar: ")
                upd_f = {}
                if opc == 1:
                    new_name = input("Ingrese el nuevo nombre: ").strip()
                    upd_f["nombre"] = new_name
                    break
                elif opc == 2:
                    new_edad = rev_num("Ingrese la nueva edad: ")
                    upd_f["edad"] = new_edad
                    break
                elif opc == 3:
                    new_genero = input("Ingrese el nuevo género (Femenino/Masculino): ").strip()
                    upd_f["genero"] = new_genero
                    break
                else:
                    print("Opción no válida.")
            
            for field, value in upd_f.items():
                query = f"UPDATE pacientes SET {field} = %s WHERE paciente_id = %s"
                cursor.execute(query, (value, paciente_id))
            connection.commit()
            print("Paciente actualizado con éxito.")
    except Exception as e:
        print(f"Error al actualizar el paciente: {e}")
    finally:
        cursor.close()
        connection.close()
def del_pac():
    paciente_id = rev_num("Ingrese el ID del paciente: ")
    connection = con_db()
    cursor = connection.cursor()
    db = con_mongodb()
    rep_colection = db["reportes"]
    try:
        query = "SELECT * FROM pacientes WHERE paciente_id = %s"
        cursor.execute(query, (paciente_id,))
        result = cursor.fetchone()
        if not result:
            print("Paciente no encontrado en MySQL.")
            return
        else:
            con = rev_num(f"¿Está seguro de eliminar al paciente {result[1]} y sus diagnósticos? (1. Si 2. No): ").strip().lower()
            if con == 2:
                print("Operación cancelada.")
                return
            elif con != 1:
                print("Ingrese una opción válida.")
                return
            else:
                query_diag = "DELETE FROM diagnosticos WHERE paciente_id = %s"
                cursor.execute(query_diag, (paciente_id,))
                print("Diagnósticos eliminados con éxito.")
                query_pac = "DELETE FROM pacientes WHERE paciente_id = %s"
                cursor.execute(query_pac, (paciente_id,))
                connection.commit()
                print("Paciente eliminado con éxito en MySQL, junto con sus diagnósticos.")
                rep_colection.delete_one({"id_paciente": paciente_id})
                print("Reporte asociado al paciente eliminado con éxito en MongoDB.")
        
    except Exception as e:
        print(f"Error al eliminar el paciente, sus diagnósticos o el reporte en MongoDB: {e}")
    finally:
        cursor.close()
        connection.close()
def create_user():
    usern = input("Ingrese el nombre de usuario: ").strip()
    password = input("Ingrese la contraseña: ").strip()
    while True:
        print("1.Admninistrador\n2.Medico\n3.Tecnico")
        num = rev_num("Ingrese el rol : ")
        if num==1:
            rol="administrador"
            break
        elif num==2:
            rol="medico"
            break
        elif num==3:
            rol="tecnico"
            break
        else:
            print("Opcion no valida")
    connection = con_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)", 
                           (usern, password, rol))
            connection.commit()
            user_id = cursor.lastrowid
            print("Usuario creado con éxito.")
            print(f"ID: {user_id}, Username: {usern}, Rol: {rol}")
        except Exception as e:
            print(f"Error al crear el usuario: {e}")
        finally:
            cursor.close()
            connection.close()
def mod_user():
    user_id = rev_num("Ingrese el ID del usuario a modificar: ")
    connection = con_db()

    if not connection:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = connection.cursor()
        # Verifica si el usuario existe
        cursor.execute("SELECT user_id, username, role FROM usuarios WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()

        if not user_data:
            print("El usuario con el ID proporcionado no existe.")
            return

        user_id, current_username, current_role = user_data
        print(f"Usuario encontrado: ID = {user_id}, Nombre = {current_username}, Rol = {current_role}")

        # Opciones de modificación
        print("1. Modificar nombre de usuario\n2. Modificar contraseña\n3. Modificar rol")
        num = rev_num("Seleccione lo que desea modificar: ")

        if num == 1:
            new_username = input("Ingrese el nuevo nombre de usuario: ").strip()
            query = "UPDATE usuarios SET username = %s WHERE user_id = %s"
            params = (new_username, user_id)
        elif num == 2:
            new_pass = input("Ingrese la nueva contraseña: ").strip()
            query = "UPDATE usuarios SET password = %s WHERE user_id = %s"
            params = (new_pass, user_id)
        elif num == 3:
            while True:
                print("1. Administrador\n2. Médico\n3. Técnico")
                num_rol = rev_num("Ingrese el nuevo rol: ")
                if num_rol == 1:
                    new_rol = "administrador"
                    break
                elif num_rol == 2:
                    new_rol = "medico"
                    break
                elif num_rol == 3:
                    new_rol = "tecnico"
                    break
                else:
                    print("Opción no válida. Intente de nuevo.")
            query = "UPDATE usuarios SET role = %s WHERE user_id = %s"
            params = (new_rol, user_id)
        else:
            print("Opción no válida.")
            return

        # Ejecuta la actualización
        cursor.execute(query, params)
        connection.commit()
        print("Usuario modificado con éxito.")

    except Exception as e:
        print(f"Error al modificar el usuario: {e}")
    finally:
        cursor.close()
        connection.close()
def del_user():
    user_id = input("Ingrese el ID del usuario a eliminar: ")
    connection = con_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE user_id = %s", (user_id,))
        re = cursor.fetchone()
    if not re:
        print("El usuario con el ID proporcionado no existe.")
        return
    else:
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE user_id = %s", (user_id,))
            connection.commit()
            print("Usuario eliminado con éxito.")
        except Exception as e:
            print(f"Error al eliminar el usuario: {e}")
        finally:
            cursor.close()
            connection.close()
def create_diag():
    try:
        paciente_id = rev_num("Ingrese el ID del paciente: ")
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute("SELECT paciente_id FROM pacientes WHERE paciente_id = %s", (paciente_id,))
        paciente_exists = cursor.fetchone()
        if not paciente_exists:
            print(f"Error: El paciente con ID {paciente_id} no existe en la base de datos.")
            cursor.close()
            connection.close()
            return
        else:
            while True:
                print("1.MRI\n2.CT\n3.Rayos X")
                num_tip = rev_num("Ingrese el tipo de imagen:")
                if num_tip == 1:
                    tipo_imagen = "MRI"
                    break
                elif num_tip == 2:
                    tipo_imagen = "CT"
                    break
                elif num_tip == 3:
                    tipo_imagen = "Rayos X"
                    break
                else:
                    print("Ingrese una opción válida")
        parte_cuerpo = input("Ingrese la parte del cuerpo (por ejemplo, Cabeza, Pulmones): ")
        condicion_sugerida = input("Ingrese la condición sugerida: ")
        probabilidad = rev_num("Ingrese la probabilidad del diagnóstico (%): ")
        notas_ia = input("Ingrese las notas de la IA sobre el diagnóstico: ")
        comentarios_medico = input("Ingrese los comentarios del médico: ")
        date=input("Ingrese la fecha del diagnóstico (YYYY-MM-DD): ")
        fecha_diagnostico = input(date)
        
        while True:
            est = rev_num("Ingrese el estado del diagnóstico ( 1. Pendiente, 2. Confirmado, 3. Descartado): ")
            if est == 1:
                estado = "Pendiente"
                break
            elif est == 2:
                estado = "Confirmado"
                break
            elif est == 3:
                estado = "Descartado"
                break
            else:
                print("Ingrese una opción válida")

        try:
            cursor.execute("SELECT MAX(diagnostico_id) FROM diagnosticos")
            max_id = cursor.fetchone()[0]
            diagnostico_id = (max_id + 1) if max_id else 1

            sql_insert_query = """
                INSERT INTO diagnosticos 
                (paciente_id, tipo_imagen, parte_cuerpo, condicion_sugerida, 
                probabilidad, notas_ia, comentarios_medico, fecha_diagnostico, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            diagnostico = (paciente_id,tipo_imagen, parte_cuerpo, condicion_sugerida, 
                            probabilidad, notas_ia, comentarios_medico, fecha_diagnostico, estado)
            cursor.execute(sql_insert_query, diagnostico)
            connection.commit()  
            print("Diagnóstico insertado correctamente")

            diag_doc = {
                "diagnostico_id": diagnostico_id,
                "tipo_imagen": tipo_imagen,
                "parte_cuerpo": parte_cuerpo,
                "analisis_IA": {
                    "condicion_sugerida": condicion_sugerida,
                    "probabilidad_%": probabilidad,
                    "notas_ia": notas_ia
                },
                "comentarios_medico": comentarios_medico,
                "fecha_diagnostico": fecha_diagnostico,
                "estado": estado
            }

            db = con_mongodb()
            rep_colection = db["reportes"]
            reporte = rep_colection.find_one({"paciente_id": paciente_id})
            if reporte:
                rep_colection.insert_one({
                    "paciente_id": paciente_id,
                    "diagnosticos": diag_doc
                })
                print("Diagnóstico sincronizado con MongoDB.")
            else:
                print(f"No se encontró un reporte con el paciente_id: {paciente_id}. Se procede a crearse un nuevo reporte con el diagnóstico")
                try:
                    last_reporte = rep_colection.find_one(sort=[("id_reporte", -1)])  # Buscar el último ID
                    id_reporte = (last_reporte["id_reporte"] + 1) if last_reporte else 1
                    print(f"Creando un nuevo reporte con ID: {id_reporte}")
                    medico_id = rev_num("Ingrese el ID del médico que genera el reporte: ")
                    date = input("Ingrese la fecha del reporte (YYYY-MM-DD): ")
                    fecha_reporte = rev_fecha(date)
                    print("¿Deseas ingresar una nota adicional? (1.Si 2.No): ")
                    opc1 = rev_num("Selecciona una opción: ")
                    notas_adicionales = []
                    if opc1 == 1:
                        while True:
                            print("\n=== Añadir Nota Adicional ===")
                            id_nota = rev_num("Ingrese el ID de la nota: ")
                            date_n = input("Ingrese la fecha de la nota (YYYY-MM-DD): ")
                            fecha_nota = rev_fecha(date_n)
                            texto = input("Ingrese el texto de la nota: ")
                            notas_adicionales.append({
                                "id_nota": id_nota,
                                "fecha_nota": fecha_nota,
                                "texto": texto
                            })
                            cont = rev_num("¿Desea añadir otra nota? (1.Si 2.No): ")
                            if cont != 1:
                                break
                    conclusiones = input("Ingrese las conclusiones del médico: ")
                    recomendaciones = input("Ingrese las recomendaciones del médico: ")
                    reporte = {
                        "reporte_id": id_reporte,
                        "paciente_id": paciente_id,
                        "medico_id": medico_id,
                        "fecha_reporte": fecha_reporte,
                        "diagnosticos": diag_doc,
                        "notas_adicionales": notas_adicionales,
                        "conclusiones": conclusiones,
                        "recomendaciones": recomendaciones
                    }
                    rep_colection.insert_one(reporte)
                    print("Reporte creado con éxito.")
                except Exception as e:
                    print(f"Error al crear el reporte: {e}")
        except Exception as e:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error al crear el diagnóstico: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def read_diag():
    try:
        diagnostico_id = rev_num("Ingrese el ID del diagnóstico a consultar: ")
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT tipo_imagen, parte_cuerpo, condicion_sugerida, probabilidad, 
                   notas_ia, comentarios_medico, fecha_diagnostico, estado
            FROM diagnosticos
            WHERE diagnostico_id = %s
        """, (diagnostico_id,))
        diagnostico = cursor.fetchone()
        if diagnostico:
            tipo_imagen, parte_cuerpo, condicion_sugerida, probabilidad, \
            notas_ia, comentarios_medico, fecha_diagnostico, estado = diagnostico
            print(f"Diagnóstico ID: {diagnostico_id}")
            print(f"Tipo de Imagen: {tipo_imagen}")
            print(f"Parte del Cuerpo: {parte_cuerpo}")
            print(f"Condición Sugerida: {condicion_sugerida}")
            print(f"Probabilidad: {probabilidad}%")
            print(f"Notas de la IA: {notas_ia}")
            print(f"Comentarios del Médico: {comentarios_medico}")
            print(f"Fecha del Diagnóstico: {fecha_diagnostico}")
            print(f"Estado: {estado}")
        else:
            print(f"No se encontró un diagnóstico con ID {diagnostico_id}.")
    
    except Exception as e:
        print(f"Error al leer el diagnóstico: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def act_diag():
    try:
        diagnostico_id = rev_num("Ingrese el ID del diagnóstico a actualizar: ")
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM diagnosticos WHERE diagnostico_id = %s", (diagnostico_id,))
        diagnostico = cursor.fetchone()
        if diagnostico:
            print(f"Diagnóstico encontrado: ID {diagnostico_id}")
            while True:
                print("1. Tipo de Imagen\n 2. Condición Sugerida\n3. Probabilidad\n5. Estado\n6. Salir")
                opcion = rev_num("Ingrese una opción : ")
                if opcion == 1:
                    while True:
                        print("1.MRI\n2.CT\n3.Rayos X")
                        num_tip = rev_num("Ingrese el tipo de imagen:")
                        if num_tip == 1:
                            tipo_imagen = "MRI"
                            break
                        elif num_tip == 2:
                            tipo_imagen = "CT"
                            break
                        elif num_tip == 3:
                            tipo_imagen = "Rayos X"
                            break
                        else:
                            print("Ingrese una opción válida")
                    cursor.execute("""
                        UPDATE diagnosticos
                        SET tipo_imagen = %s
                        WHERE diagnostico_id = %s
                    """, (tipo_imagen, diagnostico_id))
                    connection.commit()
                    print(f"Tipo de imagen actualizado a: {tipo_imagen}")
                elif opcion == 2:
                    condicion_sugerida = input(f"Nueva condición sugerida (actual: {diagnostico[3]}): ") or diagnostico[3]
                    cursor.execute("""
                        UPDATE diagnosticos
                        SET condicion_sugerida = %s
                        WHERE diagnostico_id = %s
                    """, (condicion_sugerida, diagnostico_id))
                    connection.commit()
                    print(f"Condición sugerida actualizada a: {condicion_sugerida}")

                elif opcion == 3:
                    probabilidad = rev_num(f"Nueva probabilidad del diagnóstico (actual: {diagnostico[4]}%): ") or diagnostico[4]
                    cursor.execute("""
                        UPDATE diagnosticos
                        SET probabilidad = %s
                        WHERE diagnostico_id = %s
                    """, (probabilidad, diagnostico_id))
                    connection.commit()
                    print(f"Probabilidad actualizada a: {probabilidad}%")

                elif opcion == 4:
                    notas_ia = input(f"Nuevas notas de la IA (actual: {diagnostico[5]}): ") or diagnostico[5]
                    cursor.execute("""
                        UPDATE diagnosticos
                        SET notas_ia = %s
                        WHERE diagnostico_id = %s
                    """, (notas_ia, diagnostico_id))
                    connection.commit()
                    print(f"Notas de la IA actualizadas a: {notas_ia}")

                elif opcion == 5:
                    print("1. Pendiente\n2. Confirmado\n3. Descartado")
                    estado = ["Pendiente", "Confirmado", "Descartado"][rev_num("Ingrese el estado del diagnóstico: ") - 1]
                    cursor.execute("""
                        UPDATE diagnosticos
                        SET estado = %s
                        WHERE diagnostico_id = %s
                    """, (estado, diagnostico_id))
                    connection.commit()
                    print(f"Estado actualizado a: {estado}")

                elif opcion == 6:
                    print("Saliendo de la actualización de diagnóstico.")
                    break

                else:
                    print("Opción no válida. Por favor, seleccione una opción entre 1 y 6.")

        else:
            print(f"No se encontró un diagnóstico con ID {diagnostico_id}.")
    
    except Exception as e:
        print(f"Error al actualizar el diagnóstico: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def del_diag():
    diagnostico_id = rev_num("Ingrese el ID del diagnóstico a eliminar: ")
    connection = con_db()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM diagnosticos WHERE diagnostico_id = %s"
        cursor.execute(query, (diagnostico_id,))
        connection.commit()
        print("Diagnóstico eliminado con éxito en MySQL.")
        db= con_mongodb()
        rep_colection=db["reportes"]
        if rep_colection is not None:
            resultado = rep_colection.delete_one({"_id": diagnostico_id})
            if resultado.deleted_count > 0:
                print("Diagnóstico eliminado con éxito en MongoDB.")
            else:
                print("No se encontró el diagnóstico en MongoDB.")
    except Exception as e:
        print(f"Error al eliminar el diagnóstico: {e}")
    finally:
        cursor.close()
        connection.close()
def create_reporte():
    db = con_mongodb()
    rep_colection = db["reportes"]
    if rep_colection is not None:
        last_reporte = rep_colection.find_one(sort=[("reporte_id", -1)])
        reporte_id = (last_reporte["reporte_id"] + 1) if last_reporte else 1
        print(f"Creando reporte con ID: {reporte_id}")
        paciente_id = rev_num("Ingrese el ID del paciente: ")
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute("SELECT paciente_id FROM pacientes WHERE paciente_id = %s", (paciente_id,))
        if not cursor.fetchone():
            raise ValueError(f"El paciente con ID {paciente_id} no existe.")
        else:
            print(f"Paciente con ID {paciente_id} validado correctamente.")
            medico_id = rev_num("Ingrese el ID del médico que genera el reporte: ")
            date=input("Ingrese la fecha del reporte (YYYY-MM-DD): ")
            fecha_reporte = rev_fecha(date)
            diagnosticos = []
            notas_adicionales = []
            print("¿Deseas ingresar un diagnóstico? (1. Sí / 2. No)")
            opc = rev_num("Selecciona una opción: ")
            if opc == 1:
                connection = con_db()
                cursor = connection.cursor()
                try:
                    while True:
                        print("\n=== Añadir Diagnóstico ===")
                        id_diagnostico = rev_num("Ingrese el ID del diagnóstico: ")
                        cursor.execute("SELECT 1 FROM diagnosticos WHERE diagnostico_id = %s", (id_diagnostico,))
                        if cursor.fetchone():
                            print(f"El diagnóstico con ID {id_diagnostico} ya existe. Use otro ID.")
                            continue
                        print("1. MRI\n2. CT\n3. Rayos X")
                        num_img = rev_num("Ingrese el tipo de imagen: ")
                        tipo_imagen = ["MRI", "CT", "Rayos X"][num_img - 1] if 1 <= num_img <= 3 else None
                        parte_cuerpo = input("Ingrese la parte del cuerpo: ")
                        condicion_sugerida = input("Ingrese la condición sugerida por IA: ")
                        probabilidad = rev_num("Ingrese la probabilidad del análisis IA (%): ")
                        notas_ia = input("Ingrese las notas del análisis de IA: ")
                        comentarios_medico = input("Ingrese comentarios del médico sobre el diagnóstico: ")
                        print("1. Pendiente\n2. Confirmado\n3. Descartado")
                        estado_diagnostico = ["Pendiente", "Confirmado", "Descartado"][rev_num("Ingrese el estado del diagnóstico: ") - 1]
                        diag_doc = {
                            "id_diagnostico": id_diagnostico,
                            "tipo_imagen": tipo_imagen,
                            "parte_cuerpo": parte_cuerpo,
                            "analisis_IA": {
                                "condicion_sugerida": condicion_sugerida,
                                "probabilidad_%": probabilidad,
                                "notas": notas_ia
                            },
                            "comentarios_medico": comentarios_medico,
                            "estado_diagnostico": estado_diagnostico
                        }
                        diagnosticos.append(diag_doc)
                        query = """INSERT INTO diagnosticos 
                                    (diagnostico_id, paciente_id, tipo_imagen, parte_cuerpo, condicion_sugerida, 
                                    probabilidad, notas_ia, comentarios_medico, estado_diagnostico) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                        cursor.execute(query, (id_diagnostico, paciente_id, tipo_imagen, parte_cuerpo, condicion_sugerida,
                                                probabilidad, notas_ia, comentarios_medico, estado_diagnostico))
                        connection.commit()
                        print(f"Diagnóstico {id_diagnostico} creado exitosamente en MySQL y preparado para MongoDB.")
                        cont = rev_num("¿Desea añadir otro diagnóstico? (1. Sí / 2. No): ")
                        if cont != 1:
                            break
                except Exception as e:
                    print(f"Error al insertar diagnóstico: {e}")
                finally:
                    cursor.close()
                    connection.close()
            print("¿Deseas ingresar una nota adicional? (1. Sí / 2. No): ")
            opc1 = rev_num("Selecciona una opción: ")
            if opc1 == 1:
                while True:
                    print("\n=== Añadir Nota Adicional ===")
                    id_nota = rev_num("Ingrese el ID de la nota: ")
                    fecha_nota = rev_fecha("Ingrese la fecha de la nota (YYYY-MM-DD): ")
                    texto = input("Ingrese el texto de la nota: ")
                    notas_adicionales.append({
                        "id_nota": id_nota,
                        "fecha_nota": fecha_nota,
                        "texto": texto
                    })
                    cont = rev_num("¿Desea añadir otra nota? (1. Sí / 2. No): ")
                    if cont != 1:
                        break
            conclusiones = input("Ingrese las conclusiones del médico: ")
            recomendaciones = input("Ingrese las recomendaciones del médico: ")
            notas_tec={}
            reporte_doc = {
                "eporte_id": reporte_id,
                "paciente_id": paciente_id,
                "medico_id": medico_id,
                "fecha_reporte": fecha_reporte,
                "diagnosticos": diagnosticos,
                "notas_adicionales": notas_adicionales,
                "conclusiones": conclusiones,
                "recomendaciones": recomendaciones,
                "notas _tecnicas": notas_tec
            }
            try:
                rep_colection.insert_one(reporte_doc)
                print("Reporte creado exitosamente en MongoDB.")
            except Exception as e:
                print(f"Error al crear el reporte en MongoDB: {e}")
def act_reporte():
    db = con_mongodb()
    rep_colection = db["reportes"]
    reporte_id = rev_num("Ingrese el ID del reporte a actualizar: ")
    reporte = rep_colection.find_one({"id_reporte": reporte_id})
    if not reporte:
        print("Reporte no encontrado.")
        return
    else:
        print("Reporte encontrado. Información actual del reporte:")
        print(f"ID del reporte: {reporte['id_reporte']}")
        print(f"Paciente ID: {reporte['id_paciente']}")
        print(f"Médico ID: {reporte['id_medico']}")
        print(f"Fecha del reporte: {reporte['fecha_reporte']}")
        print("Diagnósticos actuales:")
        for diag in reporte["diagnosticos"]:
            print(f"\n=== Diagnóstico ID: {diag['id_diagnostico']} ===")
            print(f"Comentarios médicos: {diag['comentarios_medico']}")
            print(f"Estado del diagnóstico: {diag['estado_diagnostico']}")
            print("===")
        print("1. Comentarios y estado de diagnostico.\n2.Notas adicionales\n3.Conclusiones y recomendaciones")
        opc = rev_num("Seleccione la opción de actualización : ")
        if opc == 1:
            diagnostico_id = rev_num("Ingrese el ID del diagnóstico a actualizar: ")
            diagnostico = next((d for d in reporte["diagnosticos"] if d["id_diagnostico"] == diagnostico_id), None)
            if not diagnostico:
                print(f"No se encontró el diagnóstico con ID {diagnostico_id}.")
                return
            else:
                print(f"Detalles actuales del diagnóstico {diagnostico_id}:")
                print(f"Tipo de imagen: {diag['tipo_imagen']}")
                print(f"Parte del cuerpo: {diag['parte_cuerpo']}")
                print(f"Condición sugerida por IA: {diag['analisis_IA']['condicion_sugerida']}")
                print(f"Probabilidad del análisis IA: {diag['analisis_IA']['probabilidad_%']}%")
                print(f"Notas del análisis IA: {diag['analisis_IA']['notas']}")
                print(f"Comentarios médicos: {diagnostico['comentarios_medico']}")
                print(f"Estado del diagnóstico: {diagnostico['estado_diagnostico']}")
                new_come = input("Ingrese el nuevo comentario del médico (deje en blanco para no modificar): ")
                new_est = input("Ingrese el nuevo estado del diagnóstico (deje en blanco para no modificar): ")
                if new_come:
                    diagnostico['comentarios_medico'] = new_come
                if new_est:
                    diagnostico['estado_diagnostico'] = new_est
                rep_colection.update_one(
                    {"id_reporte": reporte_id, "diagnosticos.id_diagnostico": diagnostico_id},
                    {"$set": {
                        "diagnosticos.$.comentarios_medico": diagnostico['comentarios_medico'],
                        "diagnosticos.$.estado_diagnostico": diagnostico['estado_diagnostico']
                    }}
                )
                print(f"Diagnóstico {diagnostico_id} actualizado con exito.")
        elif opc == 2:
            new_nota_id = rev_num("Ingrese el ID de la nueva nota: ")
            fecha_nota = rev_fecha("Ingrese la fecha de la nota (YYYY-MM-DD): ")
            text_nota = input("Ingrese el texto de la nota: ")
            rep_colection.update_one(
                {"id_reporte": reporte_id},
                {"$push": {
                    "notas_adicionales": {
                        "id_nota": new_nota_id,
                        "fecha_nota": fecha_nota,
                        "texto": text_nota
                    }
                }}
            )
            print("Nota adicional agregada con éxito.")
        elif opc == 3:
            new_conc = input("Ingrese las nuevas conclusiones del médico: ")
            new_reco = input("Ingrese las nuevas recomendaciones del médico: ")
            rep_colection.update_one(
                {"id_reporte": reporte_id},
                {"$set": {
                    "conclusiones": new_conc,
                    "recomendaciones": new_reco
                }}
            )
            print("Conclusiones y recomendaciones actualizadas con éxito.")
        else:
            print("Opción no válida.")
def add_nota_tec(username):
    db = con_mongodb()
    rep_colection = db["reportes"]
    reporte_id = rev_num("Ingrese el ID del reporte al que desea añadir notas técnicas: ")
    reporte = rep_colection.find_one({"id_reporte": reporte_id})
    if not reporte:
        print("Reporte no encontrado.")
    else:
        print(f"Reporte encontrado. ID: {reporte['id_reporte']}")
        notas_tecnicas = reporte.get("notas_tecnicas", [])
        while True:
            print("\n=== Añadir Nota Técnica ===")
            id_nota_tecnica = rev_num("Ingrese el ID de la nueva nota técnica: ")
            if any(i["id_nota_tecnica"] == id_nota_tecnica for i in notas_tecnicas):
                print("Ya existe una nota técnica con este ID. Intente con otro.")
                continue
            else:
                fecha_nota_tec = rev_fecha("Ingrese la fecha de la nota técnica (YYYY-MM-DD): ")
                text= input("Ingrese el texto de la nota técnica: ")
                tipo_pro = input("Ingrese el tipo de procedimiento relacionado: ")
                while True:
                    print("1.Alta\n2.Media\n3.Baja")
                    pri= input("Ingrese la prioridad de la nota : ")
                    if pri==1:
                        prioridad="Alta"
                        break
                    elif pri==2:
                        prioridad="Media"
                        break
                    elif pri==3:
                        prioridad="Baja"
                        break
                    else:
                        print("Ingrese una opcion valida")
                new_nota = {
                    "id_nota_tecnica": id_nota_tecnica,
                    "fecha_nota_tecnica": fecha_nota_tec,
                    "texto": text,
                    "autor_tecnico": username,
                    "tipo_procedimiento": tipo_pro,
                    "prioridad": prioridad
                }
                notas_tecnicas.append(new_nota)
                print(f"La nota técnica con ID {id_nota_tecnica} fue añadida exitosamente.")
                continuar = rev_num("¿Desea añadir otra nota técnica? (1. Sí 2. No): ")
                if continuar != 1:
                    break
            try:
                rep_colection.update_one(
                    {"id_reporte": reporte_id},
                    {"$set": {"notas_tecnicas": notas_tecnicas}}
                )
                print("Notas técnicas añadidas exitosamente al reporte.")
            except Exception as e:
                print(f"Error al actualizar las notas técnicas en el reporte: {e}")
def alm_imagenes():
    id_paciente_imagen = rev_num("Ingrese el ID del paciente: ")
    while True:
        print("1. MRI\n2. CT\n3. Rayos X")
        num_img = rev_num("Ingresa el tipo de imagen: ")
        if 1 <= num_img <= 3:
            tipo_imagen = ["MRI", "CT", "Rayos X"][num_img - 1]
            break
        else:
            print("Seleccione un número válido entre 1 y 3.")
    date=input("Ingresa la fecha de la imagen (YYYY-MM-DD): ")
    fecha_imagen = rev_fecha(date)
    resultado_IA_valor = rev_num("Ingresa el resultado preliminar del análisis por IA (en %): ")
    resultado_IA = f"{resultado_IA_valor}%"
    while True:
        print("1. Digital\n2. Analógica\n3. 3D")
        num_captura = rev_num("Ingresa el tipo de captura: ")
        if 1 <= num_captura <= 3:
            tipo_captura = ["Digital", "Analógica", "3D"][num_captura - 1]
            break
        else:
            print("Seleccione un número válido entre 1 y 3.")
    while True:
        cont= rev_num("¿En la imagen se utilizó contraste?(1. Si 2. No): ")
        if cont==1:
            contraste="Si"
            break
        elif cont==2:
            contraste="No"
            break
        else:
            print("Ingrese una opcion valida")
    posi = input("Describa cual fue el posicionamiento del paciente: ")
    res_esp_valor = rango(0.01, 1.0, "Resolución espacial", "mm/píxel")
    res_espa = f"{res_esp_valor} mm/píxel"
    fre_muestreo_valor = rango(2, 15, "Frecuencia de muestreo", "MHz")
    fre_muestreo = f"{fre_muestreo_valor} MHz"
    zona_estudio = input("Ingresa la zona de estudio donde se realizo la imagen (alfabético, ej. Abdomen, Cabeza): ")
    Alm_imagenes = {
        "ID paciente": id_paciente_imagen,
        "Tipo de imagen": tipo_imagen,
        "Fecha de imagen": fecha_imagen,
        "Resultado IA": resultado_IA,
        "Información técnica": {
            "Tipo captura": tipo_captura,
            "Contraste": contraste,
            "Posicionamiento": posi,
            "Resolución espacial": res_espa,
            "Frecuencia muestreo": fre_muestreo
        },
        "Zona de estudio": zona_estudio
    }
    db=con_mongodb()
    imagenes_col=db["Imagenes"]
    imagenes_col.insert_one(Alm_imagenes)
    print("La imagen y los metadatos han sido almacenados correctamente.")
def ver_imagen():
    id_paciente_imagen = rev_num("Ingresa el ID del paciente para buscar imágenes: ")
    filtro = {"ID paciente": id_paciente_imagen}
    db=con_mongodb()
    imagenes_col=db["Imagenes"]
    imagenes = list(imagenes_col.find(filtro))
    if not imagenes:
        print(f"No se encontraron imágenes asociadas al ID {id_paciente_imagen}.")
        return
    else:
        for idx, imagen in enumerate(imagenes, start=1):
            print(f"\n{idx}. Tipo de imagen: {imagen.get('Tipo de imagen')}, Fecha: {imagen.get('Fecha de imagen')}")
            print(f"   Resultado IA: {imagen.get('Resultado IA')}")
            print(f"   Información técnica:")
            for clave, valor in imagen.get("Información técnica", {}).items():
                print(f"      - {clave}: {valor}")
            print(f"   Zona de estudio: {imagen.get('Zona de estudio')}")
def eliminar_imagen():
    id_paciente_imagen = rev_num("Ingrese el ID del paciente cuyas imágenes desea eliminar: ")
    filtro = {"ID paciente": id_paciente_imagen}
    db=con_mongodb()
    imagenes_col=db["Imagenes"]
    imagenes = list(imagenes_col.find(filtro))
    if not imagenes:
        print(f"No se encontraron imágenes asociadas al ID {id_paciente_imagen}.")
        return
    else:
        print("\nImágenes encontradas:")
        for idx, imagen in enumerate(imagenes, start=1):
            print(f"{idx}. Tipo: {imagen.get('Tipo de imagen')}, Fecha: {imagen.get('Fecha de imagen')}")
        confirmacion = input("¿Desea eliminar todas las imágenes asociadas a este ID? (Sí/No): ").strip().lower()
        if confirmacion in ["sí", "si"]:
            resultado = imagenes_col.delete_many(filtro)
            print(f"Se eliminaron {resultado.deleted_count} imagen(es).")
        else:
            print("Operación cancelada.")
def search_pac(patient_id):
