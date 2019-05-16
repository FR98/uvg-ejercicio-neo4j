# HT10 Estructuras de Datos
# Gian Luca Rivera 18049
# Francisco Rosal 18676
# Programa de recomendacion de medicos

from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "admin123"))

def deleteLast(tx):
    tx.run("MATCH (n) DETACH DELETE n")

def initTransaction(tx):
    tx.run("""
    CREATE
        //Patients
        (Luca: Patient {name: 'Luca', tel: 123456}),
        (Willi: Patient {name: 'Willi', tel: 456123}),
        (Andy: Patient {name: 'Andy', tel: 54678965}),
        (Juan: Patient {name: 'Juan', tel: 999978}),
        (Cristina: Patient {name: 'Cristina', tel: 43235643}),
        (MariaI: Patient {name: 'Maria Ines', tel: 34567834}),
        (Marco: Patient {name: 'Marco', tel: 59821453}),
        (Camila: Patient {name: 'Camila', tel: 56438765}),
        (Abril: Patient {name: 'Abril', tel: 54786523}),
        (Alfredo: Patient {name: 'Alfredo', tel: 47611839}),
        //Doctors
        (DrHouse: Doctor {name: 'Gregory House', especialidad: 'Pediatra', tel: 789456}),
        (Pedro: Doctor {name: 'Pedro', especialidad: 'Internista', tel: 888845}),
        (Freud: Doctor {name: 'Sigmund Freud', especialidad: 'Psicologo', tel: 45321234}),
        (Pasteur: Doctor {name: 'Louis Pasteur', especialidad: 'Dermatologo', tel: 78307654}),
        (Hipocrates: Doctor {name: 'Hipocrates', especialidad: 'Cardiologo', tel: 54321567}),
        (Metrodora: Doctor {name: 'Metrodora', especialidad: 'Ginecologa', tel: 46786323}),
        (Blackwell: Doctor {name: 'Elizabeth Blackwell', especialidad: 'Oftalmologo', tel: 75432198}),
        (Lister: Doctor {name: 'Joseph Lister', especialidad: 'Cirujano', tel: 43876542}),
        (Apgar: Doctor {name: 'Virginia Apgar', especialidad: 'Anestesista', tel: 54329087}),
        (Netter: Doctor {name: 'Frank H. Netter', especialidad: 'Dentista', tel: 888845}),
        //Drugs
        (Paracetamol: Drug {name: 'Paracetamol'}),
        (Aspirina: Drug {name: 'Aspirina'}),
        (Lansoprazol: Drug {name: 'Lansoprazol'}),
        (Amoxicilina: Drug {name: 'Amoxicilina'}),
        (Amlodipina: Drug {name: 'Amlodipina'}),
        (Omeprazol: Drug {name: 'Omeprazol'}),
        (Lexotiroxina: Drug {name: 'Lexotiroxina'}),
        (Colecalciferol: Drug {name: 'Colecalciferol'}),
        (Furosemida: Drug {name: 'Furosemida'}),
        (Warafina: Drug {name: 'Warafina'}),

        //Relations
        (Willi) -[:VISITS {date:'10012010'}]-> (DrHouse) -[:PRESCRIBES]-> (Paracetamol) <-[:TAKES]- (Willi),
        (Juan) -[:VISITS {date:'20170515'}]-> (Pedro) -[:PRESCRIBES]-> (Aspirina) <-[:TAKES]- (Juan),
        (Andy) -[:VISITS {date:'28052017'}]-> (Freud) -[:PRESCRIBES]-> (Lansoprazol) <-[:TAKES]- (Andy),
        (Cristina) -[:VISITS {date:'15112019'}]-> (Pasteur) -[:PRESCRIBES]-> (Amoxicilina) <-[:TAKES]- (Cristina),
        (MariaI) -[:VISITS {date:'11122016'}]-> (Hipocrates) -[:PRESCRIBES]-> (Amlodipina) <-[:TAKES]- (MariaI),
        (Luca) -[:VISITS {date:'11102015'}]-> (Apgar) -[:PRESCRIBES]-> (Omeprazol) <-[:TAKES]- (Luca),
        (Marco) -[:VISITS {date:'01072012'}]-> (Metrodora) -[:PRESCRIBES]-> (Lexotiroxina) <-[:TAKES]- (Marco),
        (Camila) -[:VISITS {date:'05042008'}]-> (Blackwell) -[:PRESCRIBES]-> (Colecalciferol) <-[:TAKES]- (Camila),
        (Abril) -[:VISITS {date:'05042008'}]-> (Lister) -[:PRESCRIBES]-> (Furosemida) <-[:TAKES]- (Abril),
        (Alfredo) -[:VISITS {date:'05042008'}]-> (Netter) -[:PRESCRIBES]-> (Warafina) <-[:TAKES]- (Alfredo),
        (Andy) -[:KNOWS]-> (Marco),
        (Cristina) -[:KNOWS]-> (Abril),
        (MariaI) -[:KNOWS]-> (Cristina),
        (Marco) -[:KNOWS]-> (Juan),
        (Camila) -[:KNOWS]-> (Willi),
        (Abril) -[:KNOWS]-> (Luca),
        (Alfredo) -[:KNOWS]-> (Andy),
        (Juan) -[:KNOWS]-> (Willi),
        (Luca) -[:KNOWS]-> (Alfredo),
        (Willi) -[:KNOWS]-> (Andy),
        (Abril) -[:KNOWS]-> (Camila),
        (Marco) -[:KNOWS]-> (Cristina),
        (Camila) -[:KNOWS]-> (MariaI),
        //Medicos
        (Pasteur) -[:KNOWS]-> (Freud),
        (Pedro) -[:KNOWS]-> (Hipocrates),
        (Lister) -[:KNOWS]-> (DrHouse),
        (Pedro) -[:KNOWS]-> (Apgar),
        (Netter) -[:KNOWS]-> (Blackwell),
        (Blackwell) -[:KNOWS]-> (Metrodora),
        (Hipocrates) -[:KNOWS]-> (Metrodora),
        (Metrodora) -[:KNOWS]-> (Pasteur),
        (Pedro) -[:KNOWS]-> (Metrodora),
        (Apgar) -[:KNOWS]-> (Lister),
        (Freud) -[:KNOWS]-> (Blackwell),
        (DrHouse) -[:KNOWS]-> (Hipocrates),
        (Lister) -[:KNOWS]-> (Apgar),
        (DrHouse) -[:KNOWS]-> (Freud);
    """)


def addDoctor(tx, name, especialidad, tel):
    tx.run("MERGE (d: Doctor {name: $name, especialidad: $especialidad, tel: $tel})",
            name=name, especialidad=especialidad, tel=tel)

def addPatient(tx, name, tel):
    tx.run("MERGE (p: Patient {name: $name, tel: $tel})",
            name=name, tel=tel)

def visitaMedica(tx, patient, doctor, date, drug):
    #------------------------------------------------------ FALTA DEFENSIVA
    #OPTIONAL MATCH (dc: Doctor) WHERE d.name = $doctor
    tx.run("""
    MATCH (p: Patient) WHERE p.name = $patient
    MERGE (p) -[:VISITS {date: $date}]-> (dc: Doctor {name: $doctor}) -[:PRESCRIBES]-> (d: Drug {name: $drug}) <-[:TAKES]- (p);
    """, patient=patient, doctor=doctor, drug=drug, date=date)

def showDoctors(tx, especialidad):
    print("---------------------------")
    for doctor in tx.run("""
    MATCH (d: Doctor) WHERE d.especialidad = $especialidad
    RETURN d.name
    """, especialidad=especialidad):
        print(doctor["d.name"])
    print("---------------------------")

def makeRelationship(tx, person1, person2):
    #---------------------------------------------Hay que crearlos si no existen?
    #---------------------------------------------Un nodo puede ser persona y doctor?
    #---------------------------------------------Un nodo puede ser persona y paciente?
    tx.run("""
    MATCH (p1: Patient) WHERE p1.name = $person1
    MATCH (p2: Patient) WHERE p2.name = $person2
    MERGE (p1) -[:KNOWS]-> (p2)
    """, person1=person1, person2=person2)

def recomendarDoctor(tx, paciente, especialidad):
    print("---------------------------")
    for doctor in tx.run("""
    MATCH (p: Patient) WHERE p.name = $paciente
    MATCH (p) -[:KNOWS]-> (:Patient) -[:VISITS]-> (d1:Doctor) WHERE d1.especialidad = $especialidad
    RETURN d1.name
    """, paciente=paciente, especialidad=especialidad):
        print(doctor["d1.name"])

    for doctor in tx.run("""
    MATCH (p: Patient) WHERE p.name = $paciente
    MATCH (p) -[:KNOWS]-> (:Patient) -[:KNOWS]-> (:Patient) -[:VISITS]-> (d2:Doctor) WHERE d2.especialidad = $especialidad
    RETURN d2.name
    """, paciente=paciente, especialidad=especialidad):
        print(doctor["d2.name"])

def referirDoctor(tx, doctor, especialidad):
    print("---------------------------")
    for medicoReferido in tx.run("""
    MATCH (d: Doctor) WHERE d.name = $doctor
    MATCH (d) -[:KNOWS]-> (d1:Doctor) WHERE d1.especialidad = $especialidad
    RETURN d1.name
    """, doctor=doctor, especialidad=especialidad):
        print(medicoReferido["d1.name"])

    for medicoReferido in tx.run("""
    MATCH (d: Doctor) WHERE d.name = $doctor
    MATCH (d) -[:KNOWS]-> (d1:Doctor) -[:KNOWS]-> (d2:Doctor) WHERE d2.especialidad = $especialidad
    RETURN d2.name
    """, doctor=doctor, especialidad=especialidad):
        print(medicoReferido["d2.name"])

def menu():
    return ("""
-----------------------------
    Menu:
1. Ingresar doctor nuevo
2. Ingresar paciente nuevo
3. Ingresar visita medica
4. Mostrar doctores
5. Crear relacion
6. Recomendar medico
7. Referir medico
8. Salir
-----------------------------
    """)

with driver.session() as session:
    session.write_transaction(deleteLast)
    session.write_transaction(initTransaction)
    session.write_transaction(addDoctor, "Juan Paco Pedro de la Mar", "Pediatra", 456789)
    session.write_transaction(addPatient, "Paco", 555555)
    session.write_transaction(visitaMedica, "Luca", "Pedro Infantes", "20191505", "Penicilina")
    session.write_transaction(makeRelationship, "Willi", "Luca")

continuar = True
while continuar:
    print(menu())
    opcion = input("Ingrese la opcion deseada: ")

    if (opcion == "1"):
        nombre = input("Ingrese el nombre del doctor: ")
        especialidad = input("Ingrese la especialidad: ")
        tel = int(input("Ingrese el numero telefonico: "))
        driver.session().write_transaction(addDoctor, nombre, especialidad, tel)
    elif (opcion == "2"):
        nombre = input("Ingrese el nombre del paciente: ")
        tel = int(input("Ingrese el numero telefonico: "))
        driver.session().write_transaction(addPatient, nombre, tel)
    elif (opcion == "3"):
        paciente = input("Ingrese el nombre del paciente: ")
        medico = input("Ingrese el nombre del doctor: ")
        fecha = input("Ingrese la fecha de la cita: ")
        medicamento = input("Ingrese el nombre del medicamento prescrito: ")
        driver.session().write_transaction(visitaMedica, paciente, medico, fecha, medicamento)
    elif (opcion == "4"):
        especialidad = input("Ingrese la especialidad de la que desea buscar: ")
        driver.session().read_transaction(showDoctors, especialidad)
    elif (opcion == "5"):
        persona1 = input("Ingrese el nombre de la primera persona: ")
        persona2 = input("Ingrese el nombre de la segunda persona: ")
        driver.session().write_transaction(makeRelationship, persona1, persona2)
    elif (opcion == "6"):
        # Recomendacion de doctor buscando por especialidad y doctor que atendio a conocido o conocido de conocido
        paciente = input("Ingrese el nombre del paciente: ")
        especialidad = input("Ingrese la especialidad que busca: ")
        driver.session().write_transaction(recomendarDoctor, paciente, especialidad)
    elif (opcion == "7"):
        doctor = input("Ingrese el nombre del medico: ")
        especialidad = input("Ingrese la especialidad que busca: ")
        driver.session().write_transaction(referirDoctor, doctor, especialidad)
    elif (opcion == "8"):
        print("Adios")
        continuar = False
    else:
        print("Opcion invalida")
