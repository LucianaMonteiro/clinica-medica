# Criar a estrutura inicial do banco de dados em SQLite3.

import connection


print(f"Script {__name__} executado.")

def tbl_create():
    """Criar as tabelas MEDICOS e PACIENTES."""

    con, cur = connection.get()

    try:
        cur.execute("DROP TABLE medicos")
        cur.execute("DROP TABLE pacientes")
    except:
        pass

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS medicos
                (id integer PRIMARY KEY AUTOINCREMENT,
                nome text,
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
                (id integer PRIMARY KEY AUTOINCREMENT,
                nome text,
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

    con, cur = connection.get()

    medicos = [
        (
            "Kaio Oliveira",
            "123456",
            "kaio@gmail.com",
            "cardiologia",
            "noturno",
            "ativo",
        ),
        (
            "Dileyciane Monteiro",
            "234567",
            "ciane@gmail.com",
            "dermatologia",
            "diurno",
            "em análise",
        ),
        (
            "naelle monteiro",
            "345678",
            "NAELLE@gmail.com",
            "pediatria",
            "DIURNO",
            "ATIVO",
        ),
    ]

    pacientes = [
        ("izaias lima", "izaias@lima.com", "61 98181-3390", "internado"),
        ("Luciete Lima", "luciete@lima.com", "61 98136-0050", "em atendimento"),
    ]

    cur.execute("DELETE FROM medicos")
    cur.execute("DELETE FROM pacientes")

    if connection.DB_TYPE == "psql":
        cur.executemany("INSERT INTO medicos values (DEFAULT,%s,%s,%s,%s,%s,%s)", medicos)
        cur.executemany("INSERT INTO pacientes values (DEFAULT,%s,%s,%s,%s)", pacientes)
    else:
        cur.executemany("INSERT INTO medicos values (NULL,?,?,?,?,?,?)", medicos)
        cur.executemany("INSERT INTO pacientes values (NULL,?,?,?,?)", pacientes)

    con.commit()
    con.close()

    print("Dados iniciais incluídos nas tabelas.")


if __name__ == "__main__":
    tbl_create()
    tables_init()
