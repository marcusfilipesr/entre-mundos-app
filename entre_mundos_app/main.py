import streamlit as st
import pandas as pd

from entre_mundos_app.common import navbar, default_page_config

def init_session():
    if "form_gasto_aberto" not in st.session_state:
        st.session_state["form_gasto_aberto"] = False
    if "form_editar_projeto_aberto" not in st.session_state:
        st.session_state["form_editar_projeto_aberto"] = False
    if "btn_busca_info" not in st.session_state:
        st.session_state["btn_busca_info"] = False
    if "form_add_participante_aberto" not in st.session_state:
        st.session_state["form_add_participante_aberto"] = False
    if "form_add_pacote_aberto" not in st.session_state:
        st.session_state["form_add_pacote_aberto"] = False
    if "form_pagamento_aberto" not in st.session_state:
        st.session_state["form_pagamento_aberto"] = False
    if "projeto_a_gerir" not in st.session_state:
        st.session_state["projeto_a_gerir"] = None
    if "pagamento_participante_id" not in st.session_state:
        st.session_state["pagamento_participante_id"] = None
    if "pagamento_pacote_id" not in st.session_state:
        st.session_state["pagamento_pacote_id"] = None


def main():

    init_session()

    default_page_config()
    navbar()


if __name__ == '__main__':
    main()