import functions
while True:
    msj=("Bienvenido. \nSeleccione una opción. \n1.Ingresar al sistema. \n3.Ingresar al submenú \n3.Salir. \n===============\n")
    op=functions.rev_num(msj)
    if op==1:
        rol=functions.login
        if rol=="administrador":
            msj=("Bienvenido al menú administradir. \nSeleccione una opción: \n1.Gestión de usuario. \n2.Gestión de pacientes. \n3.Gestión de Diagnósticos. \n4.Gestión de imágenes. \n5.Salir \n======================\n")
            opcion=functions.ver_num(msj)
            while True:
                if opcion==1:
                    while True:
                        msj=("Ingrese una opción: \n1.Añadir usuario. \n2.Modificar usuario. \n3.Eliminar usuario. \n4.Salir. \n=================\n")
                        opcion=functions.ver_num(msj)
                        if opcion==1:
                            functions.create_user()
                        elif opcion==2:
                            functions.mod_user()
                        elif opcion==3:
                            functions.del_user()
                        elif opcion==4:
                            break
                        else:
                            print("Ingrese una opción válida.")
                            continue
                elif opcion==2:
                    while True:
                        msj=("Ingrese una opción: \n1.Crear paciente. \n2.Leer paciente. \n3.Actualizar paciente. \n4.Eliminar paciente. \n5.Salir. \n=================\n")
                        opcion=functions.ver_num(msj)
                        if opcion==1:
                            functions.create_pac()
                        elif opcion==2:
                            functions.read_pac()
                        elif opcion==3:
                            functions.act_pac()
                        elif opcion==4:
                            functions.del_pac()
                        elif opcion==5:
                            break
                        else:
                            print("Ingrese una opción válida.")
                            continue
                elif opcion==3:
                    while True:
                        msj=("Ingrese una opción: \n1.Registrar diagnóstico. \n2.Actualizar diagnóstico. \n3.Ver diagnóstico. \n4.Eliminar diagnóstico. \n5.Salir \n=================\n")
                        opcion=functions.ver_num(msj)
                        if opcion==1:
                            functions.create_diag()
                        elif opcion==2:
                            functions.act_diag()
                        elif opcion==3:
                            functions.read_diag()
                        elif opcion==4:
                            functions.del_diag()
                        elif opcion==5:
                            break
                        else:
                            print("Ingrese una opción válida.")
                            continue
                elif opcion==4:
                    while True:
                        msj=("Ingrese una opción: \n1.Almacenar imagen. \n2.Ver imagen. \n3.Eliminar imagen. \n4.Salir \n=================\n")
                        opcion=functions.ver_num(msj)
                        if opcion==1:
                            functions.alm_imagenes()
                        elif opcion==2:
                            functions.ver_imagen()
                        elif opcion==3:
                            functions.eliminar_imagen()
                        elif opcion==4:
                            break
                elif opcion==5:
                    break
                else:
                    print("Ingrese una opción válida.")
                    continue
        elif rol=="medico":
            msj=("Bienvenido al menú medico. \nSeleccione una opción: \n1.Gestionar pacientes \n2.Gestinar diagnósticos. \n3.Gestionar reportes médicos. \n4.Salir. \n============\n")
            opcion=functions.ver_num(msj)
            while True:
                if opcion==1:
                    while True:
                        msj=("Ingrese una opción: \n1.Leer paciente. \n2.Actualizar paciente. \n3.Salir. \n=================\n")
                        opcion=functions.ver_num(msj)
                        if opcion==1:
                            functions.read_pac()
                        elif opcion==2:
                            functions.act_pac()
                        elif opcion==3:
                            break
                        else:
                            print("Ingrese una opción válida.")
                            continue
                elif opcion==2:
                    while True:
                        msj=("Ingrese una opción: \n1.Actualizar diagnóstico. \n2.Ver diagnóstico. \n3.Salir \n=================\n")
                        opcion=functions.ver_num(msj)
                        if opcion==1:
                            functions.act_diag()
                        elif opcion==2:
                            functions.read_diag()
                        elif opcion==3:
                            break
                        else:
                            print("Ingrese una opción válida.")
                            continue
                elif opcion==3:
                    while True:
                        msj=("Ingrese una opción: \n1.Crear reporte. \n2.Actualizar reporte. \n3.Salir \n=================\n")
                        opcion=functions.ver_num(msj)
                        if opcion==1:
                            functions.create_reporte()
                        elif opcion==2:
                            functions.act_reporte()
                        elif opcion==3:
                            break
                        else:
                            print("Ingrese una opción válida.")
                            continue
                elif opcion==4:
                    break
                else:
                    print("Ingrese una opción válida.")
                    continue
        elif rol=="tecnico":
            msj=("Bienvenido al menú tecnico. \nSeleccione una opción: \n1.Añadir imágenes. \n2.Añadir notas técnicas. \n3.Salir. \n===============\n")
            opcion=functions.ver_num(msj)
            while True:
                if opcion==1:
                    functions.alm_imagenes()
                elif opcion==2:
                    functions.add_nota_tec()
                elif opcion==3:
                    break
                else:
                    print("Ingrese una opción válida.")
                    continue
    elif op==4:
        msj=("Ingrese el ID del paciente: \n")
        patient_id=functions.rev_num(msj)
        functions.search_pac(patient_id)
    elif op==3:
        break
    else:
        print("Ingrese una opción válida")
        continue