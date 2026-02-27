import streamlit as st
import pandas as pd

from datetime import datetime

from entre_mundos_app.common import (
    default_page_config,
    form_projeto,
    mostrar_todos_projetos,
    form_editar_projeto,
    gestao_projeto_container,
    form_add_participante,
    form_add_pacote,
    busca_tabela,
    balanco_financeiro
)

def editar_projeto_aberto():
    st.session_state["form_editar_projeto_aberto"] = True

def add_participante_aberto():
    st.session_state["form_add_participante_aberto"] = True

def add_pacote_aberto():
    st.session_state["form_add_pacote_aberto"] = True

def fechar_gestão():
    st.session_state["projeto_a_gerir"] = None

def main():
    default_page_config()

    left, center, right = st.columns([0.2, 0.6, 0.2])
    proj_container = left.container(border=True)
    with proj_container:
        st.write("**Projetos**")
        proj_col1, proj_col2 = st.columns(2, vertical_alignment="center")
        novo_projeto = proj_col1.button(
            ":material/travel_explore: Novo",
            type="primary",
            width="stretch"
        )
        proj_col2.button(
            ":material/edit_document: Editar",
            type="secondary",
            width="stretch",
            on_click=editar_projeto_aberto,
        )

        gestao_projeto_container()

    with left:
        balanco_financeiro()

    with center:
        if novo_projeto:
            form_projeto()
        if st.session_state["form_editar_projeto_aberto"]:
            form_editar_projeto()

        if st.session_state["projeto_a_gerir"] is not None:
            with st.container(border=True):
                titulo_col, fechar_col = st.columns([0.95, 0.05], gap="xxsmall")

                fechar_col.button(
                    label=":red[:material/close:]",
                    key="btn_fecha_gestao",
                    on_click=fechar_gestão,
                )

                titulo_col.subheader(st.session_state['projeto_a_gerir']['nome'])
                st.write(f"Quantidade máxima de participantes: `{st.session_state['projeto_a_gerir']['qtd_pessoas']}`")
                st.write(f"Período: `{st.session_state['projeto_a_gerir']['data_inicio'].strftime('%d/%m/%Y')}` a `{st.session_state['projeto_a_gerir']['data_fim'].strftime('%d/%m/%Y')}`")
                st.write(f"Localização: `{st.session_state['projeto_a_gerir']['local']}`")

                participante_df = busca_tabela("participante")
                pacote_df = busca_tabela("pacote")
                participantes_col, pacotes_col = st.columns(2, vertical_alignment="top")

                if not participante_df.empty:
                    df_participante_do_projeto = participante_df[participante_df["projeto_id"] == st.session_state['projeto_a_gerir']['id']].reset_index(drop=True)

                    participantes_col.write(f"Inscritos **:primary[{len(df_participante_do_projeto['nome']):.0f}]**")
                    for idx, pacote in df_participante_do_projeto.iterrows():
                        participantes_col.write(f"`{idx + 1}` **{pacote['nome']}** de {(datetime.today() - pacote['data_nascimento']).days/365.25:.0f} anos")

                if not pacote_df.empty:
                    df_pacote_do_projeto = pacote_df[pacote_df["projeto_id"] == st.session_state['projeto_a_gerir']['id']].reset_index(drop=True)
                    
                    pacotes_col.write(f"Pacotes **:primary[{len(df_pacote_do_projeto['nome']):.0f}]**")
                    for idx, pacote in df_pacote_do_projeto.iterrows():
                        pacotes_col.write(f"`{idx + 1}` **{pacote['nome']}** ({pacote['lote']:.0f}° lote) no valor de R$ {pacote['valor']:.2f}")
                    
                    st.write("")
                
                botoes_col, _ = st.columns(2)

                add_participante_col, add_pacote_col = botoes_col.columns(2)

                add_participante_col.button(
                    label=":material/person_add: Adicionar participantes",
                    key="btn_adicionar_participante",
                    on_click=add_participante_aberto,
                    width="stretch"
                )

                add_pacote_col.button(
                    label=":material/add_card: Inserir lote",
                    key="btn_adicionar_pacote",
                    on_click=add_pacote_aberto,
                    width="stretch"
                )

                if st.session_state["form_add_participante_aberto"]:
                    form_add_participante(st.session_state['projeto_a_gerir']['id'])
                if st.session_state["form_add_pacote_aberto"]:
                    form_add_pacote(st.session_state['projeto_a_gerir']['id'])

    with right:
        projetos_df = mostrar_todos_projetos()

    # center.dataframe(projetos_df)

if __name__ == '__main__':
    main()