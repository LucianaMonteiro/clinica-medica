# Criar a estrutura inicial do banco de dados em SQLite3.

import connection


print(f"Script {__name__} executado.")


def drop_tables():
    """Excluir tabelas."""

    con, cur = connection.get()

    try:
        cur.execute("DROP TABLE medicos")
        cur.execute("DROP TABLE pacientes")
    except:
        pass

    con.commit()
    con.close()


def tbl_create():
    """Criar as tabelas MEDICOS e PACIENTES."""

    con, cur = connection.get()

    PRIMARY_KEY = (
        "id SERIAL NOT NULL PRIMARY KEY"
        if connection.DB_TYPE == connection.TYPE_PSQL
        else "id integer PRIMARY KEY AUTOINCREMENT"
    )

    cur.execute(
        f"""
            CREATE TABLE IF NOT EXISTS medicos
            (   {PRIMARY_KEY},
                nome varchar(150),
                rg varchar(15),
                cpf varchar(14),
                dt_nasc date,
                sexo varchar(15),
                uf varchar(2),
                cidade varchar(50),
                cep varchar(9),
                logradouro varchar(150),
                crm varchar(9),
                email varchar(100),
                telefone varchar(15),
                especialidade varchar(50),
                turno varchar(30),
                status varchar(30)
            )
        """
    )

    cur.execute(
        f"""
            CREATE TABLE IF NOT EXISTS pacientes
            (   {PRIMARY_KEY},
                nome varchar(150),
                rg varchar(15),
                cpf varchar(14),
                dt_nasc date,
                sexo varchar(15),
                peso integer,
                altura integer,
                tp_sanguineo varchar(3),
                uf varchar(2),
                cidade varchar(50),
                cep varchar(9),
                logradouro varchar(150),
                email varchar(100),
                telefone varchar(15),
                status varchar(30)
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
            "2797247",
            "123.456.789-00",
            "1994-09-18",
            "Masculino",
            "DF",
            "Brasília",
            "12345-000",
            "Rua 15 sul, lote 02, apto 504",
            "123",
            "kaio@gmail.com",
            "(61) 98226-1871",
            "Cardiologia",
            "Diurno",
            "Ativo",
        ),
    ]

    pacientes = [
        (
            "Luciana lima",
            "2779274",
            "056.252.401-08",
            "1997-04-03",
            "Feminino",
            49,
            163,
            "O+",
            "DF",
            "Brasília",
            "71909-540",
            "Rua 12 norte, lote 06, apto 904",
            "lucianalima@gmail.com",
            "(61) 98313-4289",
            "Agendada",
        ),
    ]

    cur.execute("DELETE FROM medicos")
    cur.execute("DELETE FROM pacientes")


    if connection.DB_TYPE == connection.TYPE_PSQL:
        cur.executemany(
            "INSERT INTO medicos values (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            medicos,
        )
        cur.executemany(
            "INSERT INTO pacientes values (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            pacientes,
        )
    else:
        cur.executemany(
            "INSERT INTO medicos values (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", medicos
        )
        cur.executemany(
            "INSERT INTO pacientes values (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            pacientes,
        )

    con.commit()
    con.close()

    print("Dados iniciais incluídos nas tabelas.")


if __name__ == "__main__":
    drop_tables()
    tbl_create()
    tables_init()

    # OPERADOR TERNARIO
    # var = "algo" if True Else "outro" (python)
    # var = True ? "algo" : "outro" (Java e JavaScript)