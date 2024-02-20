def paciente_html(dados):
    html = f"""
        <tr trigger="cancel" class="editing">
            <td><input name="nome" value="{dados['nome']}"></td>
            <td><input name="email" value="{dados['email']}"></td>
            <td><input name="telefone" value="{dados['telefone']}"></td>
            <td><input name="status" value="{dados['status']}"></td>
            <td>
                <a hx-get="/api/pacientes"
                    title="Cancelar a alteração"
                    hx-swap="outerHTML" 
                    hx-target="closest table">
                    <i class="fa fa-undo"></i>
                    <!--i class="material-symbols-outlined x2">undo</i-->
                </a>
            </td>
            <td>
                <a hx-trigger="click" 
                    hx-include="closest tr"
                    hx-put="/api/pacientes/{dados['id']}" 
                    title="Salvar"
                    hx-swap="outerHTML" 
                    hx-target="closest table">
                    <i class="fa fa-floppy-o"></i>
                    <!--i class="material-symbols-outlined x2">save</i-->
                </a>
            </td>
        </tr>
        """
    return html
