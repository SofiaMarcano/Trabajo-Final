import mysql.connector
from pymongo import MongoClient
import datetime
db_config = {
    "host": "localhost",
    "user": "informatica1",
    "password": "info20242",
}
def ini_mysql():
    db_name = "Informatica1_PF"
    ex_tab= ["usuarios", "pacientes", "diagnosticos"]
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
            (1, "MRI", "Glioblastoma multiforme", "2024-05-14", "No"),
            (2, "CT", "Fractura craneal", "2024-05-13", "Si")
        ]
    }
    create_tab_ = {
        "usuarios": """
            CREATE TABLE usuarios (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('administrador', 'medico', 'tecnico') NOT NULL
            );
        """,
        "pacientes": """
            CREATE TABLE pacientes (
                paciente_id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                edad INT NOT NULL,
                genero ENUM('Masculino', 'Femenino') NOT NULL,
            );
        """,
        "diagnosticos": """
            CREATE TABLE diagnosticos (
                diagnostico_id INT AUTO_INCREMENT PRIMARY KEY,
                paciente_id INT NOT NULL,
                tipo_imagen ENUM('MRI', 'CT', 'Rayos X') NOT NULL,
                resultado_ia VARCHAR(255) NOT NULL,
                fecha_diagnostico DATE NOT NULL,
                estado ENUM('Si', 'No') NOT NULL,
            );
        """
    }
    try:
        con = mysql.connector.connect(**db_config)
        cursor = con.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = [db[0] for db in cursor.fetchall()]
        if db_name in databases:
            print(f"La base de datos '{db_name}' existe.")
        else:
            print(f"La base de datos '{db_name}' no existe. Creandola...")
            cursor.execute(f"CREATE DATABASE {db_name};")
            print(f"La Base de datos '{db_name}' ha sido creada exitosamente.")
        cursor.execute(f"USE {db_name};")
        cursor.execute("SHOW TABLES;")
        existing_tables = [table[0] for table in cursor.fetchall()]

        for t in ex_tab:
            if t in existing_tables:
                print(f"La tabla '{t}' ya existe.")
            else:
                print(f"La tabla '{t}' no existe. Creándola...")
                cursor.execute(create_tab_[t])
                print(f"Tabla '{t}' creada exitosamente.")
                for i in data_inserts[t]:
                    if t == "usuarios":
                        cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)", row)
                    elif t == "pacientes":
                        cursor.execute("INSERT INTO pacientes (nombre, edad, genero, historial_diagnosticos) VALUES (%s, %s, %s, %s)", row)
                    elif t == "diagnosticos":
                        cursor.execute("INSERT INTO diagnosticos (paciente_id, tipo_imagen, resultado_ia, fecha_diagnostico, estado) VALUES (%s, %s, %s, %s, %s)", row)

                print(f"Datos insertados en la tabla '{t}'.")
        con.commit()
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err.msg} (Código: {err.errno})")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            con.close()

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
        query = "SELECT user_id, password, role FROM usuarios WHERE username = %s"
        cursor.execute(query, (username,))
        re= cursor.fetchone()
        if re:
            user_id, s_password, role = re
            if s_password == password:
                print(f"Login exitoso. Rol: {role}")
                return user_id,role
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
        print("Paciente creado con exito")
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
    paciente_id=rev_num("Ingrese el ID del paciente:")
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
                elif opc== 2:
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
            print("Paciente actualizado con exito")
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
            if con ==2:
                print("Operación cancelada.")
                return
            elif con !=1:
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
    username = input("Ingrese el nombre de usuario: ").strip()
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
                           (username, password, rol))
            connection.commit()
            print("Usuario creado con éxito.")
        except Exception as e:
            print(f"Error al crear el usuario: {e}")
        finally:
            cursor.close()
            connection.close()
def mod_user():
    user_id = input("Ingrese el ID del usuario a modificar: ")
    connection = con_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE user_id = %s", (user_id,))
        re = cursor.fetchone()
    if not re:
        print("El usuario con el ID proporcionado no existe.")
        return
    else:
        print("1. Username\n2. Contraseña\n3. Rol")
        num = rev_num("Seleccione lo que desea modificar: ")
        if num == 1:
            new_username = input("Ingrese el nuevo nombre de usuario: ")
            query = "UPDATE usuarios SET username = %s WHERE user_id = %s"
            params = (new_username, user_id)
        elif num == 2:
            new_pass = input("Ingrese la nueva contraseña: ")
            query = "UPDATE usuarios SET password = %s WHERE user_id = %s"
            params = (new_pass, user_id)
        elif num == 3:
            while True:
                print("1. Administrador\n2. Médico\n3. Técnico")
                num_rol = rev_num("Ingrese el rol: ")
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
                    print("Opción no válida")
            query = "UPDATE usuarios SET role = %s WHERE user_id = %s"
            params = (new_rol, user_id)
        else:
            print("Opción no válida.")
            return
        if connection:
            cursor = connection.cursor()
            try:
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
    paciente_id = rev_num("Ingrese el ID del paciente: ")
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
    resultado_ia = input("Ingrese el resultado del análisis de IA (probabilidad %): ")
    fecha_diagnostico = input("Ingrese la fecha del diagnóstico (YYYY-MM-DD): ")
    fecha_diagnostico = rev_fecha(fecha_diagnostico)
    while True:
        print("1. Si\n2. No")
        num_est = input("Ingrese el estado de revisión: ")
        if num_est == 1:
            estado_revision = "Si"
            break
        elif num_est == 2:
            estado_revision = "No"
            break
        else:
            print("Ingrese una opción válida")
    connection = con_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT MAX(diagnostico_id) FROM diagnosticos")
        max_id = cursor.fetchone()[0]
        diagnostico_id = (max_id + 1) if max_id else 1 
        query = """INSERT INTO diagnosticos 
                   (diagnostico_id, paciente_id, tipo_imagen, resultado_ia, fecha_diagnostico, estado_revision) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (diagnostico_id, paciente_id, tipo_imagen, resultado_ia, fecha_diagnostico, estado_revision))
        connection.commit()
        print("Diagnóstico creado con éxito.")
        diag_doc = {
            "diagnostico_id": diagnostico_id,
            "paciente_id": paciente_id,
            "tipo_imagen": tipo_imagen,
            "resultado_ia": resultado_ia,
            "fecha_diagnostico": fecha_diagnostico,
            "estado_revision": estado_revision
        }
        db = con_mongodb()
        rep_colection=db["reportes"]
        reporte = rep_colection.find_one({"paciente_id": paciente_id})
        if reporte:
            rep_colection.insert_one({
            "paciente_id": paciente_id,
            "diagnosticos": diag_doc})
            print("Diagnóstico sincronizado con MongoDB.")
        else:
            print(f"No se encontró un reporte con el paciente_id: {paciente_id}. Se procede a crearse un nuevo reporte con el diagnóstico")
            while True:
                id_reporte = rev_num("Ingrese el ID del reporte: ")
                reporte =   rep_colection.find_one({"id_reporte": id_reporte})
                if reporte:
                    print("Este reporte ya existe")
                else:
                    break
            medico_id = rev_num("Ingrese el ID del médico que genera el reporte: ")
            fecha_reporte = rev_fecha("Ingrese la fecha del reporte (YYYY-MM-DD): ")
            print("¿Deseas ingresar una nota adicional? (1.Si 2.No): ")
            opc1=rev_num("Selecciona una opcion: ")
            notas_adicionales = []
            if opc1==1:
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
                    cont = rev_num("¿Desea añadir otra nota? (1.Si 2.No): ")
                    if cont != 1:
                        break
            conclusiones = input("Ingrese las conclusiones del médico: ")
            recomendaciones = input("Ingrese las recomendaciones del médico: ")
            reporte = {
                "reporte_id": id_reporte,
                "paciente_id":paciente_id,
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
        print(f"Error al crear el diagnóstico: {e}")
    finally:
        cursor.close()
        connection.close()
def read_diag():
    diag_id=rev_num("Ingrese el ID del diagnostico: ")
    connection = con_db()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM diagnosticos WHERE diagnostico_id = %s"
        cursor.execute(query, (diag_id,))
        result = cursor.fetchone()
        if result:
            print("Diagnóstico encontrado")
            print(f"ID: {result[0]}, Tipo de Imagen: {result[2]}, Resultado IA: {result[3]}%, Estado de Revisión: {result[6]}")
        else:
            print("Diagnóstico no encontrado ")
    except Exception as e:
        print(f"Error al leer el diagnóstico: {e}")
    finally:
        cursor.close()
        connection.close()
def act_diag():
    diagnostico_id = rev_num("Ingrese el ID del diagnóstico: ")
    connection = con_db()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM diagnosticos WHERE diagnostico_id = %s"
        cursor.execute(query, (diagnostico_id,))
        result = cursor.fetchone()
        if result:
            while True:
                print(f"Datos actuales: Tipo de Imagen: {result[2]}, Resultado IA: {result[3]}%, Estado de Revisión: {result[6]}")
                print("\n¿Qué deseas actualizar?\n1. Resultado de IA\n2. Estado de Revisión")
                opc = rev_num("Ingrese el número de la opción que desea actualizar: ")
                if opc == 1:
                    new_res_ia = input("Ingrese el nuevo resultado de IA: ")
                    query = "UPDATE diagnosticos SET resultado_ia = %s WHERE diagnostico_id = %s"
                    cursor.execute(query, (new_res_ia, diagnostico_id))
                    break
                elif opc == 2:
                    while True:
                        print("1. Si\n2. No")
                        num = input("Ingrese el nuevo estado de revisión : ")
                        if num==1:
                            new_est_rev="Si"
                            break
                        elif num==2:
                            new_est_rev="No"
                            break
                        else:
                            print("Opcion no valida")
                    query = "UPDATE diagnosticos SET estado_revision = %s WHERE diagnostico_id = %s"
                    cursor.execute(query, (new_est_rev, diagnostico_id))
                    break
                else:
                    print("Opción no válida.")
            connection.commit()
            print("Diagnóstico actualizado con éxito en MySQL.")
            db= con_mongodb()
            rep_colection=db["reportes"]
            if rep_colection:
                diag_act = rep_colection.find_one({"_id": diagnostico_id})
                if diag_act:
                    if opc == 1:
                        diag_act['analisis_IA']['resultado_preliminar'] = new_res_ia
                    elif opc == 2:
                        diag_act['estado_revision'] = new_est_rev
                    rep_colection.replace_one({"_id": diagnostico_id}, diag_act)
                    print("Diagnóstico actualizado en MongoDB.")
        else:
            print("Diagnóstico no encontrado.")
    except Exception as e:
        print(f"Error al actualizar el diagnóstico: {e}")
    finally:
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
        if rep_colection:
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
    if rep_colection:
        reporte_id = rev_num("Ingrese el ID del reporte: ")
        reporte = rep_colection.find_one({"id_reporte": reporte_id})
        if reporte:
            print("Este reporte ya existe.")
        else:
            paciente_id = rev_num("Ingrese el ID del paciente: ")
            medico_id = rev_num("Ingrese el ID del médico que genera el reporte: ")
            fecha_reporte = rev_fecha("Ingrese la fecha del reporte (YYYY-MM-DD): ")
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
                        estado_diagnostico = ["Pendiente", "Confirmado", "Descartado"][int(input("Ingrese el estado del diagnóstico: ")) - 1]
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
                "id_reporte": reporte_id,
                "id_paciente": paciente_id,
                "id_medico": medico_id,
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
def add_nota_tec(user_id):
    db = con_mongodb()
    rep_colection = db["reportes"]
    reporte_id = rev_num("Ingrese el ID del reporte al que desea añadir notas técnicas: ")
    reporte = rep_colection.find_one({"id_reporte": reporte_id})
    if not reporte:
        print("Reporte no encontrado.")
        return
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
                        prionidad="Alta"
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
                    "autor_tecnico": user_id,
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
# Función para validar fechas en formato YYYY-MM-DD
def rev_fecha(mensaje):
    while True:
        fecha = input(f"{mensaje}: ").strip()
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("Por favor, ingrese una fecha válida en formato YYYY-MM-DD.")

# Función para validar respuestas de sí o no
def opcion_si_no(mensaje):
    while True:
        opcion = input(f"{mensaje} (Sí/No): ").strip().lower()
        if opcion in ["sí", "si", "no"]:
            return opcion.capitalize()
        print("Por favor, responda con 'Sí' o 'No'.")

# Función para validar datos alfabéticos
def val_alf(mensaje):
    while True:
        entrada = input(f"{mensaje}: ").strip()
        if all(palabra.isalpha() for palabra in entrada.split()):
            return entrada
        print("Por favor, ingrese solo letras.")

# Función para validar datos numéricos dentro de un rango
def rango(min_val, max_val, mensaje, unidad):
    while True:
        try:
            valor = float(input(f"{mensaje} ({unidad}, rango {min_val}-{max_val}): "))
            if min_val <= valor <= max_val:
                return valor
            print(f"El valor debe estar entre {min_val} y {max_val}.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

# Función principal para almacenar imágenes
def alm_imagenes():
    id_paciente_imagen = rev_num("Ingrese el ID del paciente")

    # Selección del tipo de imagen
    print("1. MRI\n2. CT\n3. Rayos X")
    while True:
        num_img = rev_num("Ingresa el tipo de imagen")
        if 1 <= num_img <= 3:
            tipo_imagen = ["MRI", "CT", "Rayos X"][num_img - 1]
            break
        print("Seleccione un número válido entre 1 y 3.")

    # Fecha de la imagen
    fecha_imagen = rev_fecha("Ingresa la fecha de la imagen (YYYY-MM-DD)")

    # Resultado de IA
    resultado_IA_valor = rev_num("Ingresa el resultado preliminar del análisis por IA (en %)")
    resultado_IA = f"{resultado_IA_valor}%"

    # Selección del tipo de captura
    print("1. Digital\n2. Analógica\n3. 3D")
    while True:
        num_captura = rev_num("Ingresa el tipo de captura")
        if 1 <= num_captura <= 3:
            tipo_captura = ["Digital", "Analógica", "3D"][num_captura - 1]
            break
        print("Seleccione un número válido entre 1 y 3.")

    # Contraste
    contraste = opcion_si_no("¿En la imagen se utilizó contraste?")

    # Posicionamiento del paciente
    posicionamiento = val_alf("Describa cual fue el posicionamiento del paciente. (solo en palabras)")

    # Resolución espacial
    resolucion_espacial_valor = rango(0.01, 1.0, "Resolución espacial", "mm/píxel")
    resolucion_espacial = f"{resolucion_espacial_valor} mm/píxel"

    # Frecuencia de muestreo
    frecuencia_muestreo_valor = rango(2, 15, "Frecuencia de muestreo", "MHz")
    frecuencia_muestreo = f"{frecuencia_muestreo_valor} MHz"

    # Zona de estudio
    zona_estudio = val_alf("Ingresa la zona de estudio donde se realizo la imagen (alfabético, ej. Abdomen, Cabeza)")

    # Estructura del documento
    Alm_imagenes = {
        "ID paciente": id_paciente_imagen,
        "Tipo de imagen": tipo_imagen,
        "Fecha de imagen": fecha_imagen,
        "Resultado IA": resultado_IA,
        "Información técnica": {
            "Tipo captura": tipo_captura,
            "Contraste": contraste,
            "Posicionamiento": posicionamiento,
            "Resolución espacial": resolucion_espacial,
            "Frecuencia muestreo": frecuencia_muestreo
        },
        "Zona de estudio": zona_estudio
    }

    # Insertar en MongoDB
    imagenes_col.insert_one(Alm_imagenes)
    print("La imagen y los metadatos han sido almacenados correctamente.")

# Función para ver imágenes de un paciente
def ver_imagen():
    id_paciente_imagen = rev_num("Ingresa el ID del paciente para buscar imágenes")
    filtro = {"ID paciente": id_paciente_imagen}

    imagenes = list(imagenes_col.find(filtro))
    if not imagenes:
        print(f"No se encontraron imágenes asociadas al ID {id_paciente_imagen}.")
        return

    for idx, imagen in enumerate(imagenes, start=1):
        print(f"\n{idx}. Tipo de imagen: {imagen.get('Tipo de imagen')}, Fecha: {imagen.get('Fecha de imagen')}")
        print(f"   Resultado IA: {imagen.get('Resultado IA')}")
        print(f"   Información técnica:")
        for clave, valor in imagen.get("Información técnica", {}).items():
            print(f"      - {clave}: {valor}")
        print(f"   Zona de estudio: {imagen.get('Zona de estudio')}")

# Función para eliminar imágenes de un paciente
def eliminar_imagen():
    id_paciente_imagen = rev_num("Ingrese el ID del paciente cuyas imágenes desea eliminar")
    filtro = {"ID paciente": id_paciente_imagen}

    imagenes = list(imagenes_col.find(filtro))
    if not imagenes:
        print(f"No se encontraron imágenes asociadas al ID {id_paciente_imagen}.")
        return

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
    """Busca el historial de diagnósticos de un paciente dado su ID y consulta imágenes asociadas."""
    try:
        
        connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database="Informatica1_PF"
        )
        cursor = connection.cursor(dictionary=True)

        
        query = """
            SELECT * FROM diagnosticos WHERE patient_id = %s
        """
        cursor.execute(query, (patient_id,))
        diagnosticos = cursor.fetchall()

        if not diagnosticos:
            print(f"No se encontraron diagnósticos para el paciente con ID {patient_id}.")
            return []

        
        print(f"Historial de diagnósticos para el paciente con ID {patient_id}:")
        for diag in diagnosticos:
            print(f"  - ID: {diag['diagnosis_id']}, Fecha: {diag['diagnosis_date']}, "
                  f"Tipo: {diag['diagnosis_type']}, Probabilidad: {diag['probability']}%, "
                  f"Notas: {diag['preliminary_notes']}")

        
        imagenes_query = """
            SELECT * FROM imagenes WHERE diagnosis_id IN (%s)
        """
        diagnosis_ids = tuple(diag["diagnosis_id"] for diag in diagnosticos)
        cursor.execute(imagenes_query, (diagnosis_ids,))
        imagenes = cursor.fetchall()

        
        if imagenes:
            print("Imágenes asociadas:")
            for img in imagenes:
                print(f"  - ID: {img['image_id']}, URL: {img['image_url']}, "
                      f"Descripción: {img['description']}, Fecha: {img['date_uploaded']}")
        else:
            print("No se encontraron imágenes asociadas a los diagnósticos.")

        return diagnosticos, imagenes

    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return [], []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
