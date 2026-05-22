import streamlit as st
import pandas as pd
import numpy as np
import time

import plotly.express as px
from pathlib import Path
from datetime import datetime


cwd_path = Path(__file__)

data_path = cwd_path / "data"

colunas_padrao_gasto = [
    "id",
    "fonte",
    "nome",
    "categoria",
    "projeto_id",
    "data",
    "valor",
]

colunas_padrao_pagamento = [
    "id",
    "participante_id",
    "projeto_id",
    "pacote_id",
    "data",
    "valor_pago",
    "valor_restante",
    "obs",
]

colunas_padrao_participante = [
    "id",
    "nome",
    "cpf",
    "data_nascimento",
    "email",
    "telefone",
    "endereco",
    "telefone_emergencia",
    "nome_emergencia",
    "projeto_id",
]

colunas_padrao_projeto = [
    "id",
    "nome",
    "tipo",
    "qtd_pessoas",
    "data_inicio",
    "data_fim",
    "local",
]

colunas_padrao_pacote = [
    "id",
    "nome",
    "lote",
    "valor",
    "projeto_id"
]

tabelas_padrao = ["gasto", "projeto", "pacote", "pagamento", "participante"]

fonte_padrao_gasto = {
    "projeto": "Projeto",
    "empresa": "Entre Mundos",
}

categoria_padrao_gasto = {
    "projeto": {
        "transporte": "Transporte",
        "alimentacao": "Alimentação",
        "hospedagem": "Hospedagem",
        "servico": "Serviços",
        "brinde": "Kit",
        "outros": "Extras",
        "diaria": "Diária",
    },
    "empresa": {
        "anuncio": "Anúncio",
        "pro-labore": "Pro-labore"
    },
}

decoradores_gasto = {
    "transporte": ":taxi: Transporte",
    "alimentacao": ":hamburger: Alimentação",
    "hospedagem": ":hotel: Hospedagem",
    "servico": ":wrench: Serviços",
    "brinde": ":gift: Kit",
    "outros": ":heavy_plus_sign: Extras",
    "diaria": ":dollar: Diária",
}

tipo_padrao_projeto = {
    "expedicao": "Expedição",
    "evento": "Evento",
}

def projeto_info(projeto, status):
    with st.container(border=True):
        st.write(f"""
            **:primary[{projeto['nome']}]**
            
            Período: **{datetime.strftime(projeto['data_inicio'], '%d/%m/%Y')}** a **{datetime.strftime(projeto['data_fim'], '%d/%m/%Y')}**
            
            Cidade: **{projeto['local']}**

            Status: {status}
        """)

def fecha_forms():
    st.session_state["form_add_projeto"] = False
    st.session_state["form_gasto_aberto"] = False
    st.session_state["form_editar_projeto_aberto"] = False
    st.session_state["form_editar_participante_aberto"] = False
    st.session_state["form_editar_pacote_aberto"] = False
    st.session_state["form_editar_pagamento_aberto"] = False
    st.session_state["form_add_participante_aberto"] = False
    st.session_state["form_add_pacote_aberto"] = False
    st.session_state["form_pagamento_aberto"] = False
    st.session_state["form_editar_pagamento"] = False
    st.session_state["form_editar_gasto"] = False
    st.session_state["form_editar_gasto_aberto"] = False
    st.session_state["editar_gasto_selecao"] = False

    st.session_state["btn_busca_info"] = False
    st.session_state["editar_participante_id"] = None
    st.session_state["editar_pacote_id"] = None


def salva_tabela(nome_tabela, tabela:pd.DataFrame, fechar_forms=False, acao="inserir"):
    try:
        caminho_tabela = Path(__file__).parent / "data"
        tabela.to_excel(caminho_tabela / f"{nome_tabela}.xlsx")
        if fechar_forms:
            fecha_forms()
        if acao == "inserir":
            st.toast(f":material/check: {nome_tabela.capitalize()} adicionado com sucesso!")
        elif acao == "editar":
            st.toast(f":material/check: {nome_tabela.capitalize()} alterado com sucesso!")
        elif acao == "remover":
            st.toast(f":material/check: {nome_tabela.capitalize()} removido com sucesso!")
    except:
        st.toast(":material/x: Algo deu errado. Verifique os dados e tente novamente!")

def busca_tabela(nome_tabela):
    caminho_tabela = Path(__file__).parent / "data"
    vars = globals()
    try:
        tabela_df = pd.read_excel(caminho_tabela / f"{nome_tabela}.xlsx", index_col=0)
    except (FileNotFoundError):
        estrutura_tabela = {}
        for col in vars[f"colunas_padrao_{nome_tabela}"]:
            estrutura_tabela[col] = []
        tabela_df = pd.DataFrame(estrutura_tabela)
    return tabela_df
    
def inserir_linha(tabela, linha):
    if tabela.empty:
        if "id" not in linha.keys():
            linha["id"] = 0
        novo_df = pd.DataFrame().from_dict(linha)
        return novo_df
    else:
        if "id" not in linha.keys():
            ultimo_id = max(tabela["id"])
            linha["id"] = ultimo_id + 1
        novo_df = pd.DataFrame(linha)
        df_atualizado = pd.concat([tabela, novo_df], ignore_index=True)
        return df_atualizado
    
def editar_linha(tabela: pd.DataFrame, linha, id):
    df = tabela.copy(deep=True)
    for k, v in linha.items():
        df.loc[df["id"] == id, k] = v[0]
    return df

def remover_linha(tabela, id):
    df = tabela.copy(deep=True)
    return df[df["id"] != id].reset_index(drop=True)

def get_key(dict, value):
    try:
        return list(dict.keys())[list(dict.values()).index(value)]
    except (KeyError):
        return None

def acao_salvar(nome_tabela, filtro=None, fechar_forms=False, acao="inserir", **kwargs):
    linha = {}
    tabela_df = busca_tabela(nome_tabela)
    vars = globals()
    for col in vars[f"colunas_padrao_{nome_tabela}"]:
        if col == "id":
            continue
        else:
            try:
                try:
                    linha[col] = [get_key(vars[f"{col}_padrao_{nome_tabela}"][filtro], st.session_state[f"{nome_tabela}_{col}"])]
                except (AttributeError, KeyError):
                    linha[col] = [get_key(vars[f"{col}_padrao_{nome_tabela}"], st.session_state[f"{nome_tabela}_{col}"])]
            except (KeyError):
                linha[col] = [st.session_state[f"{nome_tabela}_{col}"]]
    if acao == "inserir":
        tabela_atualizada = inserir_linha(tabela_df, linha)
    elif acao == "editar":
        try:
            id = kwargs.get("id")
        except KeyError:
            st.toast(":material/x: Algo deu errado. Verifique os dados e tente novamente!")
            return None
        tabela_atualizada = editar_linha(tabela_df, linha, id)
    elif acao == "remover":
        try:
            id = kwargs.get("id")
        except KeyError:
            st.toast(":material/x: Algo deu errado. Verifique os dados e tente novamente!")
            return None
        tabela_atualizada = remover_linha(tabela_df, id)
    salva_tabela(nome_tabela, tabela_atualizada, fechar_forms, acao)

def filtrar_projeto(filtro, valor, col=None):
    projeto_df = busca_tabela("projeto")
    if col is None:
        return projeto_df[(projeto_df[filtro] == valor)]
    else:
        return projeto_df[(projeto_df[filtro] == valor)][col].values[0]
    
def busca_nomes(nome_tabela, projeto_id=None):
    if projeto_id is None:
        tabela_df = busca_tabela(nome_tabela)
        return tabela_df[["nome", "id"]].set_index("id").to_dict()["nome"]
    else:
        tabela_df = busca_tabela(nome_tabela)
        tabela_df_filtrada = tabela_df[tabela_df["projeto_id"] == projeto_id].reset_index(drop=True)
        return tabela_df_filtrada[["nome", "id"]].set_index("id").to_dict()["nome"]

def form_projeto():
    st.write("**Formulário novo projeto**")
    with st.container(border=True):
        proj_col1, proj_col2, proj_col3 = st.columns(3)
        proj_col1.selectbox(
            label="Tipo",
            key="projeto_tipo",
            options=[v for k, v in tipo_padrao_projeto.items()]
        )
        proj_col2.text_input(
            label="Nome do Projeto",
            key="projeto_nome",
        )
        proj_col3.number_input(
            label="Quantidade Máxima de Pessoas",
            key="projeto_qtd_pessoas",
            min_value=0
        )
        proj_col1.date_input(
            label="Data de Início",
            key="projeto_data_inicio",
            format="DD/MM/YYYY",
        )
        proj_col2.date_input(
            label="Data de Término",
            key="projeto_data_fim",
            format="DD/MM/YYYY",
        )
        proj_col3.text_input(
            label="Localização",
            key="projeto_local"
        )

        save_btn_col, cancel_btn_col = proj_col1.columns(2)
        
        save_btn_col.button(
            label="Salvar projeto",
            key="salvar_novo_projeto",
            type="primary",
            on_click=acao_salvar,
            args=("projeto",),
            width="stretch"
        )

        with cancel_btn_col:
            botao_cancelar("cancelar_novo_projeto")

def set_buscar_info(bool):
    st.session_state["btn_busca_info"] = bool

@st.dialog("Segunda chance...")
def deletar_objeto(nome_tabela, id, filtro=None):
    st.write("Tem certeza que deseja deletar?")
    del_btn = st.button(
        label=f":red[:material/delete: Excluir {nome_tabela}]",
        type="secondary",
    )
    if del_btn:
        acao_salvar(nome_tabela, filtro=filtro, acao="remover", id=id, fechar_forms=True)
        st.rerun() 

def botao_cancelar(key):
    st.button(
        label=":red[:material/cancel: Cancelar]",
        key=key,
        on_click=fecha_forms,
        width="stretch",
    )

def editar_participante_aberto(id):
    st.session_state["form_editar_participante_aberto"] = True
    st.session_state["editar_participante_id"] = id

def form_editar_participante(id):
    if id is not None:
        with st.container(border=True):
            participante_df = busca_tabela("participante")
            # Dados na base
            nome_selecionado = participante_df[participante_df["id"] == id]["nome"].values[0]
            cpf_selecionado = participante_df[participante_df["id"] == id]["cpf"].values[0]
            data_nascimento_selecionado = pd.to_datetime(participante_df[participante_df["id"] == id]["data_nascimento"].values[0])
            email_selecionado = participante_df[participante_df["id"] == id]["email"].values[0]
            telefone_selecionado = participante_df[participante_df["id"] == id]["telefone"].values[0]
            endereco_selecionado = participante_df[participante_df["id"] == id]["endereco"].values[0]
            nome_emergencia_selecionado = participante_df[participante_df["id"] == id]["nome_emergencia"].values[0]
            telefone_emergencia_selecionado = participante_df[participante_df["id"] == id]["telefone_emergencia"].values[0]
            projeto_id = participante_df[participante_df["id"] == id]["projeto_id"].values[0]

            st.write("**Formulário do Participante**")
            col1, col2, col3 = st.columns(3)
            col1.text_input(
                label="Nome",
                key="participante_nome",
                value=nome_selecionado,
            )
            cpf = col2.text_input(
                label="CPF",
                key="participante_cpf",
                help="Somente os números",
                value=cpf_selecionado
            )
            if cpf:
                if len(cpf) != 11:
                    st.error("Por favor verifique o cpf inserido!")

            col3.date_input(
                label="Data de Nascimento",
                key="participante_data_nascimento",
                format="DD/MM/YYYY",
                min_value=datetime(1900,1,1),
                value=data_nascimento_selecionado,
            )
            col1.text_input(
                label="E-mail",
                placeholder="exemplo@email.com",
                key="participante_email",
                value=email_selecionado,
            )
            col2.text_input(
                label="Número de telefone",
                key="participante_telefone",
                help="Somente os números",
                value=telefone_selecionado,
            )
            st.text_input(
                label="Endereço",
                key="participante_endereco",
                help="Separe o endereço por virgulas. Exemplo: rua, número, complemento, bairro, cidade, estado, CEP.",
                value=endereco_selecionado,
            )
            st.write("**Contato de Emergência**")
            emerg_col1, emerg_col2, emerg_col3 = st.columns(3)
            emerg_col1.text_input(
                label="Nome",
                key="participante_nome_emergencia",
                value=nome_emergencia_selecionado,
            )
            emerg_col2.text_input(
                label="Número de telefone",
                key="participante_telefone_emergencia",
                help="Somente os números",
                value=telefone_emergencia_selecionado,
            )
            st.session_state["participante_projeto_id"] = projeto_id

            add_col, cancela_col = emerg_col1.columns(2)

            add_col.button(
                label=":material/save: Salvar",
                key="btn_salvar_participante",
                on_click=acao_salvar,
                args=("participante", None, True, "editar"),
                kwargs=dict(id=id),
                width="stretch",
            )

            with cancela_col:
                botao_cancelar("cancela_editar_participante")

        deletar_col, _ = emerg_col2.columns(2)

        btn_deletar = deletar_col.button(
            label=":red[:material/delete: Excluir]",
            type="tertiary",
            width="stretch"
        )

        if btn_deletar:
            deletar_objeto("participante", id)
            

def editar_pacote_aberto(id):
    st.session_state["form_editar_pacote_aberto"] = True
    st.session_state["editar_pacote_id"] = id

def form_editar_pacote(id):
    if id is not None:
        with st.container(border=True):
            pacote_df = busca_tabela("pacote")
            # Dados na base
            nome_selecionado = pacote_df[pacote_df["id"] == id]["nome"].values[0]
            lote_selecionado = pacote_df[pacote_df["id"] == id]["lote"].values[0]
            valor_selecionado = pacote_df[pacote_df["id"] == id]["valor"].values[0]
            projeto_id = pacote_df[pacote_df["id"] == id]["projeto_id"].values[0]

            st.write("**Formulário do Lote**")
            col1, col2, col3 = st.columns(3)
            col1.text_input(
                label="Nome",
                key="pacote_nome",
                value=nome_selecionado,
            )
            col2.number_input(
                label="Lote",
                key="pacote_lote",
                min_value=1,
                max_value=5,
                value=lote_selecionado,
            )
            col3.number_input(
                label="Valor (R$)",
                key="pacote_valor",
                min_value=0.0,
                value=valor_selecionado,
            )
            st.session_state["pacote_projeto_id"] = projeto_id

            add_col, cancela_col = col1.columns(2)

            add_col.button(
                label=":material/save: Salvar",
                key="btn_salvar_pacote",
                on_click=acao_salvar,
                args=("pacote", None, True, "editar"),
                kwargs=dict(id=id),
                width="stretch",
            )

            with cancela_col:
                botao_cancelar("cancela_editar_pacote")

            deletar_col, _ = col2.columns(2)

            btn_deletar = deletar_col.button(
                label=":red[:material/delete: Excluir]",
                type="tertiary",
                width="stretch"
            )

            if btn_deletar:
                deletar_objeto("pacote", id)

def container_com_edicao(num, tabela, tipo):
    with st.container(border=False):
        texto_col, botao_col = st.columns([.85,.15], vertical_alignment="center")
        id = tabela['id']
        if tipo == "participante":
            texto_col.write(f"`{num + 1}` **{tabela['nome']}** de {(datetime.today() - tabela['data_nascimento']).days/365.25:.0f} anos")
            func = editar_participante_aberto
        elif tipo == "pacote":
            texto_col.write(f"`{num + 1}` **{tabela['nome']}** ({tabela['lote']:.0f}° lote) no valor de R$ {tabela['valor']:.2f}")
            func = editar_pacote_aberto
        
        botao_col.button(
            label=":material/edit:",
            key=f"editar_{tipo}_{id}",
            on_click=func,
            args=(id,)
        )

def gestao_financeira_container():
    st.write("**Resumo**")
    with st.container(border=True):
        dict_projetos = busca_nomes("projeto")
        lista_projetos = [v for k, v in dict_projetos.items()]
        st.write("**Escolha um projeto**")
        col_esquerda, col_centro, col_direita = st.columns(3)
        projeto = col_esquerda.selectbox(
            label="Selecione o projeto",
            options=lista_projetos,
            key="gerir_projeto",
            label_visibility="collapsed"
        )
        st.divider()
        projeto_id = get_key(dict_projetos, projeto)
        pagamento_df = busca_tabela("pagamento")
        gasto_df = busca_tabela("gasto")
        participante_df = busca_tabela("participante")
        pacote_df = busca_tabela("pacote")

        if projeto is not None:
         
            pagamento_filtrado = pagamento_df[pagamento_df['projeto_id'] == projeto_id]
            gasto_filtrado = gasto_df[gasto_df['projeto_id'] == projeto_id]
            total_pagamentos = pagamento_filtrado['valor_pago'].sum()
            total_gasto = gasto_filtrado['valor'].sum()

            balanco = total_pagamentos - total_gasto

            st.write(f"O total recebido neste projeto foi de **R${total_pagamentos}**.")
            st.write(f"Foi necessário gastar o montante de **R${total_gasto}** com os fornecedores.")
            st.write(f"O balanço foi **{'positivo' if balanco > 0 else 'negativo'}** e gerou um saldo de :{'red' if total_pagamentos <= 0 else 'green'}[**R${balanco:.2f}**].")

            pagamento_resumo = {
                ":sparkles: Entre Munders :sparkles:": [],
                ":moneybag: Adquiriram o pacote": [],
                ":dollar: No valor de": [],
                ":calendar: No dia": [],
                ":black_nib: Obs.": [],
            }
            for row in pagamento_filtrado.loc[:, "participante_id"]:
                pagamento_resumo[":sparkles: Entre Munders :sparkles:"].append(participante_df[participante_df["id"] == row]['nome'].values[0].title())

            for row in pagamento_filtrado.loc[:, "pacote_id"]:
                pagamento_resumo[":moneybag: Adquiriram o pacote"].append(pacote_df[pacote_df["id"] == row]['nome'].values[0].title())

            for data in pagamento_filtrado.loc[:, "data"]:
                pagamento_resumo[":calendar: No dia"].append(
                    data.to_pydatetime().strftime("%d/%m/%Y")
                )
            for valor in pagamento_filtrado.loc[:, "valor_pago"]:
                pagamento_resumo[":dollar: No valor de"].append(
                    f"**R${valor:.2f}**"
                )
            for obs in pagamento_filtrado.loc[:, "obs"]:
                pagamento_resumo[":black_nib: Obs."].append(
                    "" if np.isnan(obs) else obs
                )

            st.write("")
            st.write("Veja abaixo uma tabela resumo dos pagamentos e gastos")
            st.write("**Pagamentos**")
            st.table(
                data=pagamento_resumo,
                border="horizontal"
            )

            gastos_resumo = {
                ":two_women_holding_hands: Parceiros": [],
                ":hammer: Forneceram": [],
                ":money_with_wings: Cobraram": [],
                ":calendar: No dia": [],
            }

            for nome in gasto_filtrado.loc[:, "nome"]:
                gastos_resumo[":two_women_holding_hands: Parceiros"].append(nome)
            for categoria in gasto_filtrado.loc[:, "categoria"]:
                gastos_resumo[":hammer: Forneceram"].append(decoradores_gasto[categoria])
            for valor in gasto_filtrado.loc[:, "valor"]:
                gastos_resumo[":money_with_wings: Cobraram"].append(
                    f"**R${valor:.2f}**"
                )
            for data in gasto_filtrado.loc[:, "data"]:
                gastos_resumo[":calendar: No dia"].append(
                    data.to_pydatetime().strftime("%d/%m/%Y")
                )

            st.write("**Gastos**")
            st.table(
                data=gastos_resumo,
                border="horizontal"
            )
                # gerir_projeto_id = get_key(dict_projetos, projeto)
                # projeto_df = busca_tabela("projeto")

                # lista_tipos = [k for k, v in tipo_padrao_projeto.items()]
                # tipo_selecionado = projeto_df[projeto_df["id"] == gerir_projeto_id]["tipo"].values[0]
                # nome_selecionado = projeto_df[projeto_df["id"] == gerir_projeto_id]["nome"].values[0]
                # qtd_pessoas_selecionado = projeto_df[projeto_df["id"] == gerir_projeto_id]["qtd_pessoas"].values[0]
                # data_inicio_selecionado = pd.to_datetime(projeto_df[projeto_df["id"] == gerir_projeto_id]["data_inicio"].values[0])
                # data_fim_selecionado = pd.to_datetime(projeto_df[projeto_df["id"] == gerir_projeto_id]["data_fim"].values[0])
                # local_selecionado = projeto_df[projeto_df["id"] == gerir_projeto_id]["local"].values[0]

                # if st.button(
                #     label=":material/settings: Gerir",
                #     width="stretch",
                #     type="primary"
                # ):
                #     st.session_state["projeto_a_gerir"] = {
                #         "tipo":tipo_selecionado,
                #         "nome": nome_selecionado,
                #         "qtd_pessoas": qtd_pessoas_selecionado,
                #         "data_inicio": data_inicio_selecionado,
                #         "data_fim": data_fim_selecionado,
                #         "local": local_selecionado,
                #         "id": gerir_projeto_id,
                #     }

def gestao_projeto_container():
    dict_projetos = busca_nomes("projeto")
    
    projeto = st.selectbox(
        label="Selecione o projeto",
        options=[v for k, v in dict_projetos.items()],
        key="gerir_projeto",
        # label_visibility="collapsed"
    )
    if projeto is not None:
        gerir_projeto_id = get_key(dict_projetos, projeto)
        projeto_df = busca_tabela("projeto")

        lista_tipos = [k for k, v in tipo_padrao_projeto.items()]
        tipo_selecionado = projeto_df[projeto_df["id"] == gerir_projeto_id]["tipo"].values[0]
        nome_selecionado = projeto_df[projeto_df["id"] == gerir_projeto_id]["nome"].values[0]
        qtd_pessoas_selecionado = projeto_df[projeto_df["id"] == gerir_projeto_id]["qtd_pessoas"].values[0]
        data_inicio_selecionado = pd.to_datetime(projeto_df[projeto_df["id"] == gerir_projeto_id]["data_inicio"].values[0])
        data_fim_selecionado = pd.to_datetime(projeto_df[projeto_df["id"] == gerir_projeto_id]["data_fim"].values[0])
        local_selecionado = projeto_df[projeto_df["id"] == gerir_projeto_id]["local"].values[0]

        if st.button(
            label=":material/settings: Gerir",
            width="stretch",
            type="primary"
        ):
            st.session_state["projeto_a_gerir"] = {
                "tipo":tipo_selecionado,
                "nome": nome_selecionado,
                "qtd_pessoas": qtd_pessoas_selecionado,
                "data_inicio": data_inicio_selecionado,
                "data_fim": data_fim_selecionado,
                "local": local_selecionado,
                "id": gerir_projeto_id,
            }

def form_editar_projeto():
    st.write("**Edição de Projeto**")
    with st.container(border=True):
        selec_col, busca_col, _ = st.columns(3, vertical_alignment="bottom")
        
        dict_projetos = busca_nomes("projeto")
        projeto = selec_col.selectbox(
            label="Escolha o projeto para alterar",
            options=[v for k, v in dict_projetos.items()],
            key="editar_projeto"
        )
        editar_projeto_id = get_key(dict_projetos, projeto)
        projeto_df = busca_tabela("projeto")

        busca_col1, busca_col2 = busca_col.columns(2, vertical_alignment="center")
        
        busca_col1.button(
            ":material/search: Buscar",
            key="executa_buscar_info",
            on_click=set_buscar_info,
            args=(True,),
            width="stretch",
        )

        with busca_col2:
            botao_cancelar("cancela_edicao_projeto")

        proj_col1, proj_col2, proj_col3 = st.columns(3)

        # Dados na base
        lista_tipos = [k for k, v in tipo_padrao_projeto.items()]
        tipo_selecionado = projeto_df[projeto_df["id"] == editar_projeto_id]["tipo"].values[0]
        nome_selecionado = projeto_df[projeto_df["id"] == editar_projeto_id]["nome"].values[0]
        qtd_pessoas_selecionado = projeto_df[projeto_df["id"] == editar_projeto_id]["qtd_pessoas"].values[0]
        data_inicio_selecionado = pd.to_datetime(projeto_df[projeto_df["id"] == editar_projeto_id]["data_inicio"].values[0])
        data_fim_selecionado = pd.to_datetime(projeto_df[projeto_df["id"] == editar_projeto_id]["data_fim"].values[0])
        local_selecionado = projeto_df[projeto_df["id"] == editar_projeto_id]["local"].values[0]

        if st.session_state["btn_busca_info"]:
            proj_col1.selectbox(
                label="Tipo",
                key="projeto_tipo",
                options=[v for k, v in tipo_padrao_projeto.items()],
                index=lista_tipos.index(tipo_selecionado),
            )
            proj_col2.text_input(
                label="Nome do Projeto",
                key="projeto_nome",
                value=nome_selecionado,
            )
            proj_col3.number_input(
                label="Quantidade Máxima de Pessoas",
                key="projeto_qtd_pessoas",
                min_value=0,
                value=qtd_pessoas_selecionado,
            )
            proj_col1.date_input(
                label="Data de Início",
                key="projeto_data_inicio",
                format="DD/MM/YYYY",
                value=data_inicio_selecionado
            )
            proj_col2.date_input(
                label="Data de Término",
                key="projeto_data_fim",
                format="DD/MM/YYYY",
                value=data_fim_selecionado
            )
            proj_col3.text_input(
                label="Localização",
                key="projeto_local",
                value=local_selecionado
            )
        
            proj_col1.button(
                label=":material/save: Salvar edição",
                key="salvar_edicao_projeto",
                type="primary",
                on_click=acao_salvar,
                args=("projeto", None, True, "editar",),
                kwargs=dict(id=editar_projeto_id),
                width="content",
            )

            _, deletar_col = proj_col3.columns(2)

            btn_deletar = deletar_col.button(
                label=":red[:material/delete: Excluir projeto]",
                type="tertiary",
            )

            if btn_deletar:
                deletar_objeto("projeto", editar_projeto_id)

def form_add_participante(projeto_id):
    with st.container(border=True):
        st.write("**Formulário do Participante**")
        col1, col2, col3 = st.columns(3)
        col1.text_input(
            label="Nome",
            key="participante_nome",
        )
        cpf = col2.text_input(
            label="CPF",
            key="participante_cpf",
            help="Somente os números"
        )
        if cpf:
            if len(cpf) != 11:
                st.error("Por favor verifique o cpf inserido!")
        col3.date_input(
            label="Data de Nascimento",
            key="participante_data_nascimento",
            format="DD/MM/YYYY",
            min_value=datetime(1900,1,1),
        )
        col1.text_input(
            label="E-mail",
            placeholder="exemplo@email.com",
            key="participante_email",
        )
        col2.text_input(
            label="Número de telefone",
            key="participante_telefone",
            help="Somente os números"
        )
        st.text_input(
            label="Endereço",
            key="participante_endereco",
            help="Separe o endereço por virgulas. Exemplo: rua, número, complemento, bairro, cidade, estado, CEP."
        )
        st.write("**Contato de Emergência**")
        emerg_col1, emerg_col2, _ = st.columns(3)
        emerg_col1.text_input(
            label="Nome",
            key="participante_nome_emergencia",
        )
        emerg_col2.text_input(
            label="Número de telefone",
            key="participante_telefone_emergencia",
            help="Somente os números"
        )
        st.session_state["participante_projeto_id"] = projeto_id

        add_col, cancela_col = emerg_col1.columns(2)

        add_col.button(
            label=":material/add_circle: Adicionar",
            key="btn_salvar_participante",
            on_click=acao_salvar,
            args=("participante", None, True, "inserir"),
            width="stretch"
        )

        with cancela_col:
            botao_cancelar("cancela_add_participante")

def form_add_pacote(projeto_id):
    with st.container(border=True):
        # "nome",
        # "lote",
        # "valor",
        # "projeto_id"

        st.write("**Formulário do Lote**")
        col1, col2, col3 = st.columns(3)
        col1.text_input(
            label="Nome",
            key="pacote_nome",
        )
        col2.number_input(
            label="Lote",
            key="pacote_lote",
            min_value=1,
            max_value=5
        )
        col3.number_input(
            label="Valor (R$)",
            key="pacote_valor",
            min_value=0.0,
        )
        st.session_state["pacote_projeto_id"] = projeto_id

        add_col, cancela_col = col1.columns(2)

        add_col.button(
            label=":material/add_circle: Adicionar",
            key="btn_salvar_pacote",
            on_click=acao_salvar,
            args=("pacote", None, True, "inserir"),
            width="stretch",
        )

        with cancela_col:
            botao_cancelar("cancela_add_pacote")

def form_editar_pagamento_aberto():
    st.session_state["form_editar_pagamento_aberto"] = True

def form_editar_pagamento_fechado():
    st.session_state["form_editar_pagamento_aberto"] = False

def form_editar_pagamento():
    st.write("**Edição de Pagamento**")
    with st.container(border=True):
        pagamento_df = busca_tabela("pagamento")
        projeto_df = busca_tabela("projeto")
        projeto_ids = list(set(pagamento_df["projeto_id"].to_list()))
        projeto_com_pagamento = {}
        for id in projeto_ids:
            projeto_com_pagamento[int(id)] = projeto_df[projeto_df["id"] == id]["nome"].values[0]

        # "participante_id",
        # "projeto_id",
        # "pacote_id",
        # "data",
        # "valor_pago",
        # "valor_restante",
        # "obs",
        selec_col, busca_col, btn_3_col = st.columns(3, vertical_alignment="bottom")

        dict_projetos = busca_nomes("projeto")
        projeto = selec_col.selectbox(
            label="Escolha o projeto",
            options=projeto_com_pagamento.values(),
            key="escolher_projeto_pagamento",
        )
        projeto_id = get_key(dict_projetos, projeto)
        pagamento_df_filtrado = pagamento_df[pagamento_df["projeto_id"] == projeto_id]
        pacote_df = busca_tabela("pacote")
        df_pacote_do_projeto = pacote_df[pacote_df["projeto_id"] == projeto_id]
        dict_participante = busca_nomes("participante", projeto_id)
        dict_pacote = busca_nomes("pacote", projeto_id)

        dict_pagamento = {}
        for idx, linha in pagamento_df_filtrado.iterrows():
            # info_col, btn_col = st.columns([.8,.2], vertical_alignment="center")
            # linha_container = info_col.container(border=True)
            dict_pagamento[int(linha['id'])] = f"{dict_participante[linha['participante_id']].split(' ')[0]} pagou de R${linha['valor_pago']} no dia {linha['data'].strftime('%d/%m/%Y')}"

        linha_pagamento = busca_col.selectbox(
            label="Escolha o pagamento",
            options=dict_pagamento.values(),
            key="escolher_linha_pagamento"
        )
        pagamento_id = get_key(dict_pagamento, linha_pagamento)

        select_btn_col, cancela_btn_col, _ = btn_3_col.columns(3)

        select_btn_col.button(
            label="Select",
            key="pagamento_select_btn",
            on_click=form_editar_pagamento_aberto,
            width="stretch"
        )

        with cancela_btn_col:
            botao_cancelar("cancela_edicao_pagamento")

        if st.session_state["form_editar_pagamento_aberto"]:
            lista_participante = [v for k, v in dict_participante.items()]
            lista_pacotes = [v for k, v in dict_pacote.items()]
            participante_selecionado = dict_participante[pagamento_df_filtrado[pagamento_df_filtrado["id"] == pagamento_id]["participante_id"].values[0]]
            pacote_selecionado = dict_pacote[pagamento_df_filtrado[pagamento_df_filtrado["id"] == pagamento_id]["pacote_id"].values[0]]
            valor_selecionado = pagamento_df_filtrado[pagamento_df_filtrado["id"] == pagamento_id]["valor_pago"].values[0]
            data_selecionado = pagamento_df_filtrado[pagamento_df_filtrado["id"] == pagamento_id]["data"].values[0]
            obs_selecionado = pagamento_df_filtrado[pagamento_df_filtrado["id"] == pagamento_id]["obs"].values[0]

            if np.isnan(obs_selecionado):
                obs_selecionado = ""

            col1, col2, col3 = st.columns(3)
            participante = col1.selectbox(
                label="Pagante",
                options=lista_participante,
                key="pagamento_participante",
                placeholder="Escolha um participante",
                index=lista_participante.index(participante_selecionado)
            )
            pacote = col2.selectbox(
                label="Pacote a pagar",
                options=lista_pacotes,
                key="pagamento_pacote",
                placeholder="Escolha um pacote",
                index=lista_pacotes.index(pacote_selecionado)
            )
            valor_pago = col3.number_input(
                label="Valor pago (R$)",
                key="pagamento_valor_pago",
                min_value=0.0,
                value=valor_selecionado
            )
            col1.date_input(
                label="Data",
                key="pagamento_data",
                format="DD/MM/YYYY",
                value=pd.to_datetime(data_selecionado).to_pydatetime(),
            )
            if participante is not None and pacote is not None:
                participante_id = get_key(dict_participante, participante)
                pacote_id = get_key(dict_pacote, pacote)

                valor_total = df_pacote_do_projeto[df_pacote_do_projeto['id'] == pacote_id]['valor'].values[0]
                valor_restante = valor_total - valor_pago
                # col1.write(f"Valor restante do pacote: :primary[**R${valor_restante:.2f}**]")

                st.session_state["pagamento_particiante_id"] = participante_id
                st.session_state["pagamento_pacote_id"] = pacote_id
                st.session_state["pagamento_projeto_id"] = projeto_id
                st.session_state["pagamento_valor_restante"] = valor_restante

            col2.text_area(
                label="Observações",
                key="pagamento_obs",
                value=obs_selecionado,
            )
            
            salvar_pagamento_col, cancela_editar_col, delete_col = col1.columns(3)

            salvar_pagamento_col.button(
                label=":material/save: Salvar",
                key="botao_salvar_pagamento",
                type="primary",
                on_click=acao_salvar,
                args=("pagamento", None, True, "editar"),
                kwargs=dict(id=pagamento_id),
                width="stretch"
            )

            cancela_editar_col.button(
                label=":red[:material/cancel: Cancelar]",
                key="cancela_editar_pagamento",
                on_click=form_editar_pagamento_fechado,
                width="stretch",
            )

            btn_deletar = delete_col.button(
                label=":red[:material/delete: Excluir]",
                type="tertiary",
                width="stretch"
            )

            if btn_deletar:
                deletar_objeto("pagamento", pagamento_id)

def form_editar_gasto_aberto():
    st.session_state["form_editar_gasto_aberto"] = True

def form_editar_gasto_fechado():
    st.session_state["form_editar_gasto_aberto"] = False
    st.session_state["editar_gasto_selecao"] = False

def editar_gasto_selecao():
    st.session_state["editar_gasto_selecao"] = True

def form_editar_gasto():
    st.write("**Edição de Gasto**")
    with st.container(border=True):
        gasto_df = busca_tabela("gasto")
        projeto_df = busca_tabela("projeto")

        # "participante_id",
        # "projeto_id",
        # "pacote_id",
        # "data",
        # "valor_pago",
        # "valor_restante",
        # "obs",
        fonte_col, botoes_col, _ = st.columns(3, vertical_alignment="bottom")
        selec_col, busca_col, btn_3_col = st.columns(3, vertical_alignment="bottom")
        lista_fonte = [v for k, v in fonte_padrao_gasto.items()]
        fonte = fonte_col.selectbox(
            label="Fonte",
            options=lista_fonte,
            key="gasto_fonte_editar",
        )
        fonte_key = get_key(fonte_padrao_gasto, fonte)
        btn_ir, btn_x, _= botoes_col.columns(3, vertical_alignment="center")
        btn_go = btn_ir.button(
            label="Prosseguir",
            key="selecionar_fonte_gasto",
            on_click=editar_gasto_selecao,
            width="stretch"
        )
        btn_x.button(
            label=":red[:material/cancel: Cancelar]",
            key="fecha_editar_gasto",
            on_click=fecha_forms,
            width="stretch"
        )

        if st.session_state["editar_gasto_selecao"]:
            if fonte_key != "empresa":
                projeto_ids = list(set(gasto_df["projeto_id"].to_list()))
                projeto_ids.pop(0)
                projeto_com_gasto = {}
                for id in projeto_ids:
                    projeto_com_gasto[int(id)] = projeto_df[projeto_df["id"] == id]["nome"].values[0]
            else:
                projeto_com_gasto = {}

            dict_projetos = busca_nomes("projeto")
            projeto = selec_col.selectbox(
                label="Escolha o projeto",
                options=projeto_com_gasto.values(),
                disabled=(fonte_key != "projeto"),
                key="escolher_projeto_gasto",
                index=0,
            )

            if fonte_key == "empresa":
                projeto_id = 0
            else:
                projeto_id = get_key(dict_projetos, projeto)
            gasto_df_filtrado = gasto_df[gasto_df["projeto_id"] == projeto_id]

            dict_gasto = {}
            for idx, linha in gasto_df_filtrado.iterrows():
                # info_col, btn_col = st.columns([.8,.2], vertical_alignment="center")
                # linha_container = info_col.container(border=True)
                dict_gasto[int(linha['id'])] = f"O valor de R${linha['valor']} foi pago para {linha['nome']} no dia {linha['data'].strftime('%d/%m/%Y')}"

            linha_gasto = busca_col.selectbox(
                label="Escolha o gasto",
                options=dict_gasto.values(),
                key="escolher_linha_gasto"
            )
            gasto_id = get_key(dict_gasto, linha_gasto)

            select_btn_col, cancela_btn_col, _ = btn_3_col.columns(3)

            select_btn_col.button(
                label="Select",
                key="gasto_select_btn",
                on_click=form_editar_gasto_aberto,
                width="stretch"
            )

            cancela_btn_col.button(
                    label=":red[:material/cancel: Cancelar]",
                    key="cancela_editar_gasto_form",
                    on_click=form_editar_gasto_fechado,
                    width="stretch",
                )

            if st.session_state["form_editar_gasto_aberto"]:
                lista_projetos = [v for k, v in dict_projetos.items()]
                lista_categoria = [v for k, v in categoria_padrao_gasto[fonte_key].items()]
                fonte_selecionado = fonte_padrao_gasto[gasto_df_filtrado[gasto_df_filtrado["id"] == gasto_id]["fonte"].values[0]]
                fonte_key_selecionado = get_key(fonte_padrao_gasto, fonte_selecionado)
                nome_selecionado = gasto_df_filtrado[gasto_df_filtrado["id"] == gasto_id]["nome"].values[0]
                categoria_selecionado = categoria_padrao_gasto[fonte_key_selecionado][gasto_df_filtrado[gasto_df_filtrado["id"] == gasto_id]["categoria"].values[0]]
                valor_selecionado = gasto_df_filtrado[gasto_df_filtrado["id"] == gasto_id]["valor"].values[0]
                data_selecionado = gasto_df_filtrado[gasto_df_filtrado["id"] == gasto_id]["data"].values[0]
                st.write("**Formulário de gasto**")
                col1, col2, col3 = st.columns(3)
                fonte = col1.selectbox(
                    label="Fonte",
                    options=[v for k, v in fonte_padrao_gasto.items()],
                    key="gasto_fonte",
                    index=lista_fonte.index(fonte_selecionado),
                    disabled=True
                )
                fonte_key = get_key(fonte_padrao_gasto, fonte)
                col2.selectbox(
                    label="Categoria",
                    options=lista_categoria,
                    key="gasto_categoria",
                    index=lista_categoria.index(categoria_selecionado)
                )
                col3.text_input(
                    label="Nome",
                    key="gasto_nome",
                    value=nome_selecionado,
                )
                projeto = col1.selectbox(
                    label="Nome do Projeto",
                    options=lista_projetos,
                    disabled=True,
                    key="gasto_projeto",
                    index=lista_projetos.index(projeto) if projeto is not None else 0,
                )
                st.session_state["gasto_projeto_id"] = projeto_id

                col2.number_input(
                    label="Valor (R$)",
                    min_value=0.0,
                    key="gasto_valor",
                    value=valor_selecionado,
                )
                col3.date_input(
                    label="Data",
                    key="gasto_data",
                    format="DD/MM/YYYY",
                    value=pd.to_datetime(data_selecionado).to_pydatetime(),
                )
                
                salvar_gasto_col, cancela_editar_col, delete_col = col1.columns(3)

                salvar_gasto_col.button(
                    label=":material/save: Salvar",
                    key="botao_salvar_gasto",
                    type="primary",
                    on_click=acao_salvar,
                    args=("gasto", fonte_key, True, "editar"),
                    kwargs=dict(id=gasto_id),
                    width="stretch"
                )

                cancela_editar_col.button(
                    label=":red[:material/cancel: Cancelar]",
                    key="cancela_editar_gasto",
                    on_click=form_editar_gasto_fechado,
                    width="stretch",
                )

                btn_deletar = delete_col.button(
                    label=":red[:material/delete: Excluir]",
                    type="tertiary",
                    width="stretch"
                )

                if btn_deletar:
                    deletar_objeto("gasto", gasto_id, filtro=fonte_key)

def form_pagamento():
    st.write("**Formulário de Pagamento**")
    with st.container(border=True):
        # "participante_id",
        # "projeto_id",
        # "pacote_id",
        # "data",
        # "valor_pago",
        # "valor_restante",
        # "obs",
        selec_col, busca_col, _ = st.columns(3, vertical_alignment="bottom")

        dict_projetos = busca_nomes("projeto")
        projeto = selec_col.selectbox(
            label="Escolha o projeto",
            options=[v for k, v in dict_projetos.items()],
            key="escolher_projeto_pagamento",
        )
        projeto_id = get_key(dict_projetos, projeto)
        
        pacote_df = busca_tabela("pacote")
        df_pacote_do_projeto = pacote_df[pacote_df["projeto_id"] == projeto_id]

        dict_participante = busca_nomes("participante", projeto_id)
        dict_pacote = busca_nomes("pacote", projeto_id)

        col1, col2, col3 = st.columns(3)
        participante = col1.selectbox(
            label="Pagante",
            options=[v for k, v in dict_participante.items()],
            key="pagamento_participante",
            placeholder="Escolha um participante",
        )
        pacote = col2.selectbox(
            label="Pacote a pagar",
            options=[v for k, v in dict_pacote.items()],
            key="pagamento_pacote",
            placeholder="Escolha um pacote",
        )
        valor_pago = col3.number_input(
            label="Valor pago (R$)",
            key="pagamento_valor_pago",
            min_value=0.0
        )
        col1.date_input(
            label="Data",
            key="pagamento_data",
            format="DD/MM/YYYY"
        )
        if participante is not None and pacote is not None:
            participante_id = get_key(dict_participante, participante)
            pacote_id = get_key(dict_pacote, pacote)

            valor_total = df_pacote_do_projeto[df_pacote_do_projeto['id'] == pacote_id]['valor'].values[0]
            valor_restante = valor_total - valor_pago
            col1.write(f"Valor restante do pacote: :primary[**R${valor_restante:.2f}**]")

            st.session_state["pagamento_participante_id"] = participante_id
            st.session_state["pagamento_pacote_id"] = pacote_id
            st.session_state["pagamento_projeto_id"] = projeto_id
            st.session_state["pagamento_valor_restante"] = valor_restante

        col2.text_area(
            label="Observações",
            key="pagamento_obs"
        )
        
        add_gasto_col, cancela_gasto_col = col1.columns(2)

        add_gasto_col.button(
            label=":material/add_circle: Adicionar",
            key="bota_adicionar_pagamento",
            type="primary",
            on_click=acao_salvar,
            args=("pagamento", None, True),
            width="stretch"
        )

        with cancela_gasto_col:
            botao_cancelar("cancela_pagamento")

        
def balanco_financeiro():
    st.write("**Fluxo de Caixa**")
    with st.container(border=True, horizontal_alignment="center"):
        pagamento_df = busca_tabela("pagamento")
        gasto_df = busca_tabela("gasto")

        if not pagamento_df.empty and not gasto_df.empty:
            total_recebido = pagamento_df["valor_pago"].sum()
            total_gasto = gasto_df["valor"].sum()

            balanco = total_recebido - total_gasto

            recebido_linha = st.container()
            header1_col, recebido_col = recebido_linha.columns([.3, .7], vertical_alignment="bottom")
            header1_col.write("Recebido")
            recebido_col.subheader(f":blue[R$ {total_recebido:.2f}]", anchor=False)
            
            gasto_linha = st.container()
            header2_col, gasto_col = gasto_linha.columns([.3, .7], vertical_alignment="bottom")
            header2_col.write("Gasto")
            gasto_col.subheader(f":red[R$ {total_gasto:.2f}]", anchor=False)
            
            balanco_linha = st.container()
            header3_col, balanco_col = balanco_linha.columns([.3, .7], vertical_alignment="bottom")
            header3_col.write("Balanço")
            balanco_col.subheader(f":{'red' if balanco <= 0 else 'green'}[R$ {balanco:.2f}]", anchor=False)
        else:
            st.write("Sem dados...")


def form_gasto():
    st.write("**Formulário de Gastos**")
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        fonte = col1.selectbox(
            label="Fonte",
            options=[v for k, v in fonte_padrao_gasto.items()],
            key="gasto_fonte",
        )
        fonte_key = get_key(fonte_padrao_gasto, fonte)

        col2.selectbox(
            label="Categoria",
            options=[v for k, v in categoria_padrao_gasto[fonte_key].items()],
            key="gasto_categoria"
        )
        col3.text_input(
            label="Nome",
            key="gasto_nome"
        )
        dict_projetos = busca_nomes("projeto")
        projeto = col1.selectbox(
            label="Nome do Projeto",
            options=[v for k, v in dict_projetos.items()],
            disabled=(fonte_key != "projeto"),
            key="gasto_projeto"
        )
        if fonte_key == "empresa":
            st.session_state["gasto_projeto_id"] = 0
        else:
            st.session_state["gasto_projeto_id"] = get_key(dict_projetos, projeto)

        col2.number_input(
            label="Valor (R$)",
            min_value=0.0,
            key="gasto_valor"
        )
        col3.date_input(
            label="Data",
            key="gasto_data",
            format="DD/MM/YYYY"
        )

        add_gasto_col, cancela_gasto_col = col1.columns(2)

        add_gasto_col.button(
            label=":material/add_circle: Adicionar",
            key="bota_adicionar_gasto",
            type="primary",
            on_click=acao_salvar,
            args=("gasto", fonte_key, True),
            width="stretch"
        )

        with cancela_gasto_col:
            botao_cancelar("cancela_gasto")

def create_dataframe():
    vars = globals()
    for table_name in tabelas_padrao:
        for k, v in vars.items():
            if table_name in k:
                print(f"{k}: {v}")

def default_page_config():

    assets = Path(__file__).parent / "assets"
    logo = assets / "logo.png"

    st.set_page_config(
        page_title="Entre Mundos",
        layout="wide",
        page_icon=str(logo),
    )

def navbar():
    
    home = st.Page("pages/home.py", title="Home", icon=":material/home:", default=True)
    finance = st.Page("pages/finance.py", title="Financeiro", icon=":material/account_balance:")
    calculate = st.Page("pages/calculator.py", title="Calculadora", icon=":material/calculate:")

    pg = st.navigation(pages=[home, finance, calculate], position="top")
    pg.run()

def mostrar_todos_projetos():
    projetos_df = busca_tabela("projeto")    
    data_hoje = datetime.today()
    st.write("**Histórico**")
    with st.container(border=True, height=454):
        for _, linha in projetos_df.iterrows():
            if data_hoje > linha["data_fim"]:
                projeto_info(linha, ":tada: **:primary[Finalizado!]** :tada:")
            elif data_hoje <= linha["data_fim"] and data_hoje >= linha["data_inicio"]:
                projeto_info(linha, "**:primary[Em andamento!]**")
            else:
                projeto_info(linha, "**:primary[Por vir!]**")

    return projetos_df

# if __name__ == '__main__':
#     create_dataframe()