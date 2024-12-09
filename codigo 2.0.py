import functions
db_config = {
    "host": "localhost",
    "user": "informatica1",
    "password": "info20242",
    "database":"SistemaMedico"
}
functions.iny_mysql()
functions.iny_mongo()
while True:
    print("Por favor, inicie sesión.")
    user_data = functions.login()  
    if user_data:
        username, rol = user_data
        print(f"Bienvenido, {username}. Tu rol es: {rol}.")
    else:
        print("Login fallido. Por favor, intente nuevamente.")
        continue
    while True:
        if rol == "administrador":
            msj = (
                f"Bienvenido al menú administrador, {username}.\n"
                "Seleccione una opción:\n"
                "1. Gestión de usuario.\n"
                "2. Gestión de pacientes.\n"
                "3. Gestión de diagnósticos.\n"
                "4. Gestión de imágenes.\n"
                "5. Salir.\n"
                "======================\n"
            )
            opc= functions.rev_num(msj)
            if opc== 1:
                while True:
                    msj = (
                        "Ingrese una opción:\n"
                        "1. Añadir usuario.\n"
                        "2. Modificar usuario.\n"
                        "3. Eliminar usuario.\n"
                        "4. Salir.\n"
                        "=================\n"
                    )
                    opc1 = functions.rev_num(msj)
                    if opc1 == 1:
                        functions.create_user()
                    elif opc1 == 2:
                        functions.mod_user()
                    elif opc1 == 3:
                        functions.del_user()
                    elif opc1 == 4:
                        break
                    else:
                        print("Ingrese una opción válida.")
            elif opc == 2:
                while True:
                    msj = (
                        "Ingrese una opción:\n"
                        "1. Crear paciente.\n"
                        "2. Leer paciente.\n"
                        "3. Actualizar paciente.\n"
                        "4. Eliminar paciente.\n"
                        "5. Salir.\n"
                        "=================\n"
                    )
                    opc1 = functions.rev_num(msj)
                    if opc1 == 1:
                        functions.create_pac()
                    elif opc1== 2:
                        functions.read_pac()
                    elif opc1== 3:
                        functions.act_pac()
                    elif opc1== 4:
                        functions.del_pac()
                    elif opc1== 5:
                        break
                    else:
                        print("Ingrese una opción válida.")
            elif opc== 3:
                while True:
                    msj = (
                        "Ingrese una opción:\n"
                        "1. Registrar diagnóstico.\n"
                        "2. Actualizar diagnóstico.\n"
                        "3. Ver diagnóstico.\n"
                        "4. Eliminar diagnóstico.\n"
                        "5. Salir.\n"
                        "=================\n"
                    )
                    opc1 = functions.rev_num(msj)
                    if opc1 == 1:
                        functions.create_diag()
                    elif opc1 == 2:
                        functions.act_diag()
                    elif opc1== 3:
                        functions.read_diag()
                    elif opc1== 4:
                        functions.del_diag()
                    elif opc1== 5:
                        break
                    else:
                        print("Ingrese una opción válida.")
            elif opc== 4:
                while True:
                    msj = (
                        "Ingrese una opción:\n"
                        "1. Almacenar imagen.\n"
                        "2. Ver imagen.\n"
                        "3. Eliminar imagen.\n"
                        "4. Salir.\n"
                        "=================\n"
                    )
                    opc1= functions.rev_num(msj)
                    if opc1== 1:
                        functions.alm_imagenes()
                    elif opc1== 2:
                        functions.ver_imagen()
                    elif opc1== 3:
                        functions.eliminar_imagen()
                    elif opc1== 4:
                        break
                    else:
                        print("Ingrese una opción válida.")
            elif opc== 5:
                print("Saliendo del menú administrador...")
                break
            else:
                print("Ingrese una opción válida.")
        
        elif rol == "medico":
            msj = (
                f"Bienvenido al menú médico, {username}.\n"
                "Seleccione una opción:\n"
                "1. Gestionar pacientes.\n"
                "2. Gestionar diagnósticos.\n"
                "3. Gestionar reportes médicos.\n"
                "4. Salir.\n"
                "============\n"
            )
            opc = functions.rev_num(msj)
            if opc == 1:
                while True:
                    msj = (
                        "Ingrese una opción:\n"
                        "1. Leer paciente.\n"
                        "2. Actualizar paciente.\n"
                        "3. Salir.\n"
                        "=================\n"
                    )
                    opc1 = functions.rev_num(msj)
                    if opc1 == 1:
                        functions.read_pac()
                    elif opc1 == 2:
                        functions.act_pac()
                    elif opc1 == 3:
                        break
                    else:
                        print("Ingrese una opción válida.")
            elif opc == 2:
                while True:
                    msj = (
                        "Ingrese una opción:\n"
                        "1. Actualizar diagnóstico.\n"
                        "2. Ver diagnóstico.\n"
                        "3. Salir.\n"
                        "=================\n"
                    )
                    opc1 = functions.rev_num(msj)
                    if opc1 == 1:
                        functions.act_diag()
                    elif opc1 == 2:
                        functions.read_diag()
                    elif opc1 == 3:
                        break
                    else:
                        print("Ingrese una opción válida.")
            elif opc == 3:
                while True:
                    msj = (
                        "Ingrese una opción:\n"
                        "1. Crear reporte.\n"
                        "2. Actualizar reporte.\n"
                        "3. Salir.\n"
                        "=================\n"
                    )
                    opc1 = functions.rev_num(msj)
                    if opc1 == 1:
                        functions.create_reporte()
                    elif opc1 == 2:
                        functions.act_reporte()
                    elif opc1 == 3:
                        break
                    else:
                        print("Ingrese una opción válida.")
            elif opc == 4:
                print("Saliendo del menú médico...")
                break
            else:
                print("Ingrese una opción válida.")
        
        elif rol == "tecnico":
            msj = (
                f"Bienvenido al menú técnico, {username}.\n"
                "Seleccione una opción:\n"
                "1. Añadir imágenes.\n"
                "2. Añadir notas técnicas.\n"
                "3. Salir.\n"
                "===============\n"
            )
            opc1 = functions.rev_num(msj)
            if opc1 == 1:
                functions.alm_imagenes()
            elif opc1== 2:
                functions.add_nota_tec(username)
            elif opc1 == 3:
                print("Saliendo del menú técnico...")
                break
            else:
                print("Ingrese una opción válida.")
        
        else:
            print("Rol no reconocido. Saliendo del sistema...")
            break

