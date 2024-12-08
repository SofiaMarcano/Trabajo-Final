
import mysql.connector
from pymongo import MongoClient
import datetime

# Configuración de la base de datos
db_config = {
    "host": "localhost",
    "user": "informatica1",
    "password": "info20242",
    "database": "Informatica1_PF"  # Agregado para evitar errores
}

def ini_mysql():
    db_name = db_config["database"]
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
            (1, "MRI", "Glioblastoma multiforme", "2024-05-14", "No"),
            (2, "CT", "Fractura craneal", "2024-05-13", "Si")
        ]
    }
    create_tab_ = {
        "usuarios": """
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
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
        "diagnosticos": """
            CREATE TABLE IF NOT EXISTS diagnosticos (
                diagnostico_id INT AUTO_INCREMENT PRIMARY KEY,
                paciente_id INT NOT NULL,
                tipo_imagen ENUM('MRI', 'CT', 'Rayos X') NOT NULL,
                resultado_ia VARCHAR(255) NOT NULL,
                fecha_diagnostico DATE NOT NULL,
                estado ENUM('Si', 'No') NOT NULL,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(paciente_id)
            );
        """
    }
    try:
        con = mysql.connector.connect(**db_config)
        cursor = con.cursor()
        
        # Crear la base de datos si no existe
        cursor.execute("SHOW DATABASES;")
        databases = [db[0] for db in cursor.fetchall()]
        if db_name not in databases:
            cursor.execute(f"CREATE DATABASE {db_name};")
            print(f"Base de datos '{db_name}' creada exitosamente.")
        
        cursor.execute(f"USE {db_name};")
        
        # Crear tablas si no existen
        cursor.execute("SHOW TABLES;")
        existing_tables = [table[0] for table in cursor.fetchall()]
        for table in ex_tab:
            if table not in existing_tables:
                cursor.execute(create_tab_[table])
                print(f"Tabla '{table}' creada exitosamente.")
        
        # Insertar datos iniciales
        for table, rows in data_inserts.items():
            for row in rows:
                if table == "usuarios":
                    cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)", row)
                elif table == "pacientes":
                    cursor.execute("INSERT INTO pacientes (nombre, edad, genero) VALUES (%s, %s, %s)", row)
                elif table == "diagnosticos":
                    cursor.execute(
                        "INSERT INTO diagnosticos (paciente_id, tipo_imagen, resultado_ia, fecha_diagnostico, estado) VALUES (%s, %s, %s, %s, %s)",
                        row
                    )
        con.commit()
        print("Datos iniciales insertados exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()

def con_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    return client["sistema_medico"]

def con_db():
    return mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"]
    )

def rev_num(msj):
    while True:
        try:
            x = int(input(msj))
            return x
        except ValueError:
            print("Ingrese un número válido.")

def rev_fecha(date):
    while True:
        try:
            fecha = datetime.datetime.strptime(date, "%Y-%m-%d")
            return fecha.strftime("%Y-%m-%d")
        except ValueError:
            print("Formato incorrecto, ingrese la fecha nuevamente (YYYY-MM-DD):")
            date = input()
