def paciente_html():
    html = f"""
        <table class ="form">
            <tr trigger="cancel" class="editing">
                <td><input placeholder="Nome do paciente" name="nome" value=""></td>
                <td><input placeholder="E-mail do paciente" name="email" value=""></td>
                <td><input placeholder="Telefone do paciente" name="telefone" value=""></td>
                <td>
                    <select name="status">
                        <option value="" selected disabled hidden>Selecione</option>
                        <option value="aguardando">Aguardando</option>
                        <option value="em atendimento">Em atendimento</option>
                        <option value="atendido">Atendido</option>
                        <option value="internado">Internado</option>
                        <option value="liberado">Liberado</option>
                    </select>
                </td>
                <td class="button">
                    <div>
                        <a class="button secondary" hx-get="/api/pacientes"
                            title="Cancelar a alteração"
                            hx-swap="outerHTML" 
                            hx-target="closest table">
                            Cancelar
                        </a>
                    
                        <a class="button" hx-trigger="click" 
                            hx-include="closest tr"
                            hx-post="/api/pacientes" 
                            title="Salvar"
                            hx-swap="outerHTML" 
                            hx-target="closest table">
                            Salvar
                        </a>
                    </div>
                </td>
            </tr>
        </table>
        """
    return html

def medico_html():
    html = f"""
        <table class ="form">
            <tr trigger="cancel" class="editing">
                <td><input placeholder="Nome do médico" name="nome" value=""></td>
                <td><input placeholder="CRM" name="crm" value=""></td>
                <td><input placeholder="E-mail" name="email" value=""></td>
                <td><input placeholder="Especialidade" name="especialidade" value=""></td>
                <td>
                    <select name="turno">
                        <option value="" selected disabled hidden>Selecione</option>
                        <option value="diurno">Diurno</option>
                        <option value="vespertino">Vespertino</option>
                        <option value="noturno">Noturno</option>
                    </select>
                </td>
                
                <td>
                    <select name="status">
                        <option value="" selected disabled hidden>Selecione</option>
                        <option value="em atendimento">Em atendimento</option>
                        <option value="de plantão">De plantão</option>
                        <option value="indisponível">Indisponível</option>
                    </select>
                </td>
                <td class="button">
                    <div>
                        <a class="button secondary" hx-get="/api/medicos"
                            title="Cancelar a alteração"
                            hx-swap="outerHTML" 
                            hx-target="closest table">
                            Cancelar
                        </a>
                    
                        <a class="button" hx-trigger="click" 
                            hx-include="closest tr"
                            hx-post="/api/medicos" 
                            title="Salvar"
                            hx-swap="outerHTML" 
                            hx-target="closest table">
                            Salvar
                        </a>
                    </div>
                </td>
            </tr>
        </table>
        """
    return html