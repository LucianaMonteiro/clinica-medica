# Criar a estrutura inicial do banco de dados em SQLite3.

import sqlite3


print(f"Script {__name__} executado.") 


def tbl_create():
    """Criar as tabelas MEDICOS e PACIENTES."""

    con = sqlite3.connect("clinica.db")
    cur = con.cursor()

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS medicos
                (nome text,
                crm text,
                email text,
                especialidade text,
                turno text,
                status text
            )
        """
    )

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS pacientes
                (nome text,
                email text,
                telefone text,
                status text
            )
        """
    )

    con.commit()
    con.close()

    print("Tabelas criadas.")

def tables_init():
    """Incluir dados iniciais de teste nas tabelas."""

    con = sqlite3.connect("clinica.db")
    cur = con.cursor()


    # cur.execute(
    #     """
    #         INSERT INTO medicos VALUES (
    #             "Kaio Oliveira",
    #             "123456",
    #             "kaio@gmail.com",
    #             "cardiologia",
    #             "noturno",
    #             "ativo"
    #         )
    #     """
    # )

    medicos = [
        (
            "Kaio Oliveira",
                "123456",
                "kaio@gmail.com",
                "cardiologia",
                "noturno",
                "ativo"
        ),
        (
            "Dileyciane Monteiro",
            "234567",
            "ciane@gmail.com",
            "dermatologia",
            "diurno",
            "em análise"
        ),
        (
            "Naelle Monteiro",
            "345678",
            "NAELLE@gmail.com",
            "pediatria",
            "DIURNO",
            "ATIVO"
        ),
    ]

    pacientes = [
        (
            "Izaias Lima",
            "izaias@lima.com",
            "61 98181-3390",
            "internado"
        ),
        (
            "Luciete Lima",
            "luciete@lima.com",
            "61 98136-0050",
            "em atendimento"
        ),
    ]

    cur.execute("DELETE FROM medicos")
    cur.execute("DELETE FROM pacientes")

    cur.executemany("INSERT INTO medicos values (?,?,?,?,?,?)", medicos)
    cur.executemany("INSERT INTO pacientes values (?,?,?,?)", pacientes)

    con.commit()
    con.close() 

    print("Dados iniciais incluídos nas tabelas.")


if __name__ == "__main__":
    tbl_create()
    tables_init()