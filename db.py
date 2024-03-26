import connection

con, cur = connection.get()


# PACIENTES:
def get_pacientes():
    return get_dados("pacientes")


def get_paciente(id):
    return get_dados("pacientes", id)


def add_paciente(new_paciente: dict):
    fields = {
        "logradouro": "Rua 12 Norte, lote 6",
        "cep": "71909-540",
        "cidade": "Brasília",
        "uf": "DF",
    }
    new_paciente.update(fields)

    add("pacientes", new_paciente)


def update_paciente(id, updated: dict):
    paciente = get_paciente(id)
    update(id, "pacientes", paciente, updated)


def del_paciente(id):
    delete("pacientes", id)


# MÉDICOS:
def get_medicos():
    return get_dados("medicos")


def get_medico(id):
    return get_dados("medicos", id)


def add_medico(new_medico: dict):
    add("medicos", new_medico)


def update_medico(id, updated: dict):
    medico = get_medico(id)
    update(id, "medicos", medico, updated)


def del_medico(id):
    delete("medicos", id)


##########


def get_dados(tbl, id=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE id={id}" if id else ""
    sql += " ORDER BY 2"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


def search_medicos(param):
    return search("medicos", param)


def search_pacientes(param):
    return search("pacientes", param)


def search(tbl, param):

    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE UPPER(nome) LIKE '%{param.upper()}%'"
    sql += f" OR cpf LIKE '{param}%'"
    sql += " ORDER BY 2"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


def add(table, dados: dict):
    if dados:
        values = [f"'{v}'" for _, v in dados.items()]
        all_values = ",".join(values)

        fields = [f"{k}" for k, _ in dados.items()]
        all_fields = ",".join(fields)

        if connection.DB_TYPE == connection.TYPE_PSQL:
            sql = (
                f"INSERT INTO {table} (id, {all_fields}) values (DEFAULT, {all_values})"
            )
        else:
            sql = f"INSERT INTO {table} (id, {all_fields}) values (NULL, {all_values})"

        cur.execute(sql)
        con.commit()


def update(id, table, outdated: dict, updated: dict):

    if outdated:
        dados = outdated[0]
        dados.update(updated)

        fields = [f"{k}='{v}'" for k, v in dados.items()]
        all_fields = ",".join(fields)

        sql = f"UPDATE {table} SET {all_fields} WHERE id={id}"
        cur.execute(sql)
        con.commit()
    return


def delete(tbl, id):
    sql = f"DELETE FROM {tbl} WHERE id={id}"
    cur.execute(sql)
    con.commit()
    return
