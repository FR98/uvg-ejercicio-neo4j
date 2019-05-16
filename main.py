# HT10 Estructuras de Datos
# Gian Luca Rivera 18049
# Francisco Rosal 18676
# Programa de recomendacion de medicos
# -[:]->

from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "admin123"))

def deleteLast(tx):
    tx.run("MATCH (n) DETACH DELETE n")

def initTransaction(tx):
    tx.run("""
    CREATE
    //Patients
        (Luca: Patient {name: 'Luca RB', tel: 123456}),
        (Willi: Patient {name: 'Willi', tel: 456123}),
        (Juan: Patient {name: 'Juan', tel: 999978}),
    //Doctors
        (DocAmigo: Doctor {name: 'Doctor Amigo', especialidad: 'Pediatra', tel: 789456}),
        (Pedro: Doctor {name: 'Pedro', especialidad: 'Internista', tel: 888845}),
    //Drugs
        (Paracetamol: Drug {name: 'Paracetamol'}),
        (Aspirina: Drug {name: 'Aspirina'}),

    //Relations
        (Willi) -[:VISITS {date:'20001230'}]-> (DocAmigo) -[:PRESCRIBES]-> (Paracetamol) <-[:TAKES]- (Willi),
        (Juan) -[:VISITS {date:'20170515'}]-> (Pedro) -[:PRESCRIBES]-> (Aspirina) <-[:TAKES]- (Juan),
        (Willi) -[:KNOWS]-> (Luca);
    """)


def addDoctor(tx, name, especialidad, tel):
    tx.run("MERGE (d: Doctor {name: $name, especialidad: $especialidad, tel: $tel})",
            name=name, especialidad=especialidad, tel=tel)

def addPatient(tx, name, tel):
    tx.run("MERGE (p: Patient {name: $name, tel: $tel})",
            name=name, tel=tel)

def visitaMedica(tx, patient, doctor, date, drug):
    tx.run("""
    MATCH (p: Patient) WHERE p.name = $patient
    MERGE (p) -[:VISITS {date: $date}]-> (dc: Doctor {name: $doctor}) -[:PRESCRIBES]-> (d: Drug {name: $drug}) <-[:TAKES]- (p);
    """, patient=patient, doctor=doctor, drug=drug, date=date)

def findDoctor(tx, especialidad):
    tx.run("""
    MATCH (d: Doctor {especialidad: $especialidad})
    """, especialidad=especialidad)

# def add_friend(tx, name, friend_name):
#     tx.run("MERGE (a:Person {name: $name}) "
#            "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
#            name=name, friend_name=friend_name)
#
# def print_friends(tx, name):
#     for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
#                          "RETURN friend.name ORDER BY friend.name", name=name):
#         print(record["friend.name"])

with driver.session() as session:
    session.write_transaction(deleteLast)
    session.write_transaction(initTransaction)
    session.write_transaction(visitaMedica, "Luca RB", "Pedro Infantes", "20191505", "Penicilina")
    # session.write_transaction(add_friend, "Arthur", "Guinevere")
    # session.write_transaction(add_friend, "Arthur", "Lancelot")
    # session.write_transaction(add_friend, "Arthur", "Merlin")
    # session.read_transaction(print_friends, "Arthur")
