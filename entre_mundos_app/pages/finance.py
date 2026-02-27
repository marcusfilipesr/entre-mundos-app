import sys
import streamlit as st
from pathlib import Path

# sys.path.append(Path(__file__).parent.parent)

from entre_mundos_app.common import form_gasto, default_page_config, form_pagamento, balanco_financeiro

def gasto_aberto():
    st.session_state["form_gasto_aberto"] = True

def pagamento_aberto():
    st.session_state["form_pagamento_aberto"] = True

def main():
    default_page_config()
    # navbar()

    left, center = st.columns([.2, .8])

    controle_container = left.container(border=True)
    controle_container.write("**Controle**")
    cntrl_col1, cntrl_col2 = controle_container.columns(2, vertical_alignment="center")
    add_pagamento = cntrl_col1.button(
        label=":material/attach_money: Adicionar pagamento",
        key="btn_adicionar_pagamento",
        on_click=pagamento_aberto,
        type="primary",
    )
    add_gasto = cntrl_col2.button(
        label=":material/payment_arrow_down: Adicionar gasto",
        key="btn_adicionar_gasto",
        on_click=gasto_aberto,
        type="secondary",
    )

    with left:
        balanco_financeiro()

    with center:
        if st.session_state["form_gasto_aberto"]:
            form_gasto()

        if st.session_state["form_pagamento_aberto"]:
            form_pagamento()



if __name__ == "__main__":
    main()