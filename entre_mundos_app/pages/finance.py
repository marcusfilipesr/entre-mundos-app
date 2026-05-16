import sys
import streamlit as st
from pathlib import Path

# sys.path.append(Path(__file__).parent.parent)

from entre_mundos_app.common import (
    form_gasto,
    default_page_config,
    form_pagamento,
    balanco_financeiro,
    busca_tabela,
    form_editar_pagamento,
    form_editar_gasto,
)


def gasto_aberto():
    st.session_state["form_gasto_aberto"] = True


def pagamento_aberto():
    st.session_state["form_pagamento_aberto"] = True


def editar_pagamento_aberto():
    st.session_state["form_editar_pagamento"] = True


def editar_gasto_aberto():
    st.session_state["form_editar_gasto"] = True


def main():
    default_page_config()
    # navbar()

    left, center = st.columns([0.2, 0.8])

    left.write("**Controle**")

    controle_container = left.container(border=True)
    controle_container.write("**Pagamentos**")
    pagamento_col1, pagamento_col2 = controle_container.columns(
        2, vertical_alignment="center"
    )
    # controle_container.divider()
    add_pagamento = pagamento_col1.button(
        label=":material/attach_money: Adicionar",
        key="btn_adicionar_pagamento",
        on_click=pagamento_aberto,
        type="primary",
        width="stretch",
    )
    editar_pagamento = pagamento_col2.button(
        label=":material/edit: Editar",
        key="btn_editar_pagamento",
        on_click=editar_pagamento_aberto,
        type="secondary",
        width="stretch",
    )
    controle_container.write("**Gastos**")
    gasto_col1, gasto_col2 = controle_container.columns(2, vertical_alignment="center")
    add_gasto = gasto_col1.button(
        label=":material/payment_arrow_down: Adicionar",
        key="btn_adicionar_gasto",
        on_click=gasto_aberto,
        type="primary",
        width="stretch",
    )
    editar_gasto = gasto_col2.button(
        label=":material/edit: Editar",
        key="btn_editar_gasto",
        on_click=editar_gasto_aberto,
        type="secondary",
        width="stretch",
    )

    with left:
        balanco_financeiro()

    with center:
        if st.session_state["form_gasto_aberto"]:
            form_gasto()

        if st.session_state["form_pagamento_aberto"]:
            form_pagamento()

        if st.session_state["form_editar_pagamento"]:
            form_editar_pagamento()

        if st.session_state["form_editar_gasto"]:
            form_editar_gasto()

        pagamento_df = busca_tabela("pagamento")
        st.write("Pagamentos")
        st.write(pagamento_df)
        gasto_df = busca_tabela("gasto")
        st.write("Gastos")
        st.write(gasto_df)


if __name__ == "__main__":
    main()
