import streamlit as st
import pandas as pd

from pathlib import Path
from entre_mundos_app.common import navbar, default_page_config

def init_session():
    ## Gasto
    if "form_gasto_aberto" not in st.session_state:
        st.session_state["form_gasto_aberto"] = False
    if "form_editar_gasto" not in st.session_state:
        st.session_state["form_editar_gasto"] = False
    if "form_editar_gasto_aberto" not in st.session_state:
        st.session_state["form_editar_gasto_aberto"] = False
    if "editar_gasto_selecao" not in st.session_state:
        st.session_state["editar_gasto_selecao"] = False
    
    ## Projeto
    if "form_add_projeto" not in st.session_state:
        st.session_state["form_add_projeto"] = False
    if "form_editar_projeto_aberto" not in st.session_state:
        st.session_state["form_editar_projeto_aberto"] = False
    if "projeto_a_gerir" not in st.session_state:
        st.session_state["projeto_a_gerir"] = None
    if "btn_busca_info" not in st.session_state:
        st.session_state["btn_busca_info"] = False

    ## Participante
    if "form_editar_participante_aberto" not in st.session_state:
        st.session_state["form_editar_participante_aberto"] = False
    if "form_add_participante_aberto" not in st.session_state:
        st.session_state["form_add_participante_aberto"] = False
    if "editar_participante_id" not in st.session_state:
        st.session_state["editar_participante_id"] = None

    ## Pacote
    if "form_editar_pacote_aberto" not in st.session_state:
        st.session_state["form_editar_pacote_aberto"] = False
    if "editar_pacote_id" not in st.session_state:
        st.session_state["editar_pacote_id"] = None
    if "form_add_pacote_aberto" not in st.session_state:
        st.session_state["form_add_pacote_aberto"] = False

    ## Pagamento
    if "form_editar_pagamento" not in st.session_state:
        st.session_state["form_editar_pagamento"] = False
    if "form_editar_pagamento_aberto" not in st.session_state:
        st.session_state["form_editar_pagamento_aberto"] = False
    if "form_pagamento_aberto" not in st.session_state:
        st.session_state["form_pagamento_aberto"] = False 
    if "pagamento_participante_id" not in st.session_state:
        st.session_state["pagamento_participante_id"] = None
    if "pagamento_pacote_id" not in st.session_state:
        st.session_state["pagamento_pacote_id"] = None

    ## Calculadora
    if "alterar_taxa" not in st.session_state:
        st.session_state["alterar_taxa"] = False
    if "custos" not in st.session_state:
        st.session_state["custos"] = pd.DataFrame(
            {
                "nome": [""],
                "valor": [0.0],
                "depende": [True]
            }
        )

def main():

    init_session()

    default_page_config()
    navbar()

    assets = Path(__file__).parent / "assets"
    logo = assets / "logo.png"
    st.logo(logo, size="large")

if __name__ == '__main__':
    main()