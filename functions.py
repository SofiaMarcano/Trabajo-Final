import mysql.connector
from pymongo import MongoClient
import datetime
db_config = {
    "host": "localhost",
    "user": "informatica1",
    "password": "info20242",
    "database": "Informatica1_PF"
}
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
    paciente_id=rev_num("Ingrese el ID del paciente: ")
    connection = con_db()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM pacientes WHERE paciente_id = %s"
        cursor.execute(query, (paciente_id,))
        re = cursor.fetchone()
        if re:
            print(f"Paciente encontrado:\nID: {re[0]}\nNombre: {re[1]}\nEdad: {re[2]}\nGénero: {re[3]}")
        else:
            print("Paciente no encontrado.")
    except Exception as e:
        print(f"Error al leer el paciente: {e}")
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
    paciente_id=rev_num("Ingrese el ID del paciente: ")
    connection = con_db()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM pacientes WHERE paciente_id = %s"
        cursor.execute(query, (paciente_id,))
        result = cursor.fetchone()
        if not result:
            print("Paciente no encontrado en MySQL.")
            return
        else:
            query = "DELETE FROM pacientes WHERE paciente_id = %s"
            cursor.execute(query, (paciente_id,))
            connection.commit()
            print("Paciente eliminado con éxito en MySQL.")
    except Exception as e:
        print(f"Error al eliminar el paciente: {e}")
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
            reporte_doc = {
                "id_reporte": reporte_id,
                "id_paciente": paciente_id,
                "id_medico": medico_id,
                "fecha_reporte": fecha_reporte,
                "diagnosticos": diagnosticos,
                "notas_adicionales": notas_adicionales,
                "conclusiones": conclusiones,
                "recomendaciones": recomendaciones
            }
            try:
                rep_colection.insert_one(reporte_doc)
                print("Reporte creado exitosamente en MongoDB.")
            except Exception as e:
                print(f"Error al crear el reporte en MongoDB: {e}")

#Esta se va a encargar de devolver el ID del paciente o un none para hacer el submenú del punto 6
def ver_pac():
    while True:
        paciente_id=rev_num("Ingrese el ID del paciente: ")
        connection = con_db()
        cursor = connection.cursor()
        try:
            query = "SELECT * FROM pacientes WHERE paciente_id = %s"
            cursor.execute(query, (paciente_id,))
            re = cursor.fetchone()
            if re:
                return paciente_id
            else:
                return None
        except Exception as e:
            print(f"Error al leer el paciente: {e}")
        finally:
            cursor.close()
            connection.close()
#Este va a ser el submenú del punto 6, aún no está terminado, porque necesito saber como está estructurada la información de la base de datos :(.
def search_pac():
    while True:
       msj=("Ingrese una opción: \n1. Ver historial de diagnósticos. \n2. Consultar imágenes asociadas. \n==============\n")
       x = rev_num(msj)
       if x==1:
           ID=ver_pac()
           if ID != None:
               

