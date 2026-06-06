import io

import pandas as pd
import numpy as np
import streamlit as st

from datetime import datetime
from common import default_page_config

tabela_taxa = {
    "intervalo": ["1;1", "2;6", "7;13"],
    "cartao": [1.99, 2.49, 2.99],
    "adiantamento": [1.25, 1.70, 1.70],
}

def save_output(data):
    output = io.BytesIO()
    xls = pd.ExcelWriter(output, engine="xlsxwriter")
    data.to_excel(xls, index=False)
    xls.close()
    return output.getvalue()


def dynamic_input_data_editor(data, key, **_kwargs):
    changed_key = f"{key}_khkhkkhkkhkhkihsdhsaskskhhfgiolwmxkahs"
    initial_data_key = f"{key}_khkhkkhkkhkhkihsdhsaskskhhfgiolwmxkahs__initial_data"

    def on_data_editor_changed():
        if "on_change" in _kwargs:
            args = _kwargs["args"] if "args" in _kwargs else ()
            kwargs = _kwargs["kwargs"] if "kwargs" in _kwargs else {}
            _kwargs["on_change"](*args, **kwargs)
        st.session_state[changed_key] = True

    if changed_key in st.session_state and st.session_state[changed_key]:
        data = st.session_state[initial_data_key]
        st.session_state[changed_key] = False
    else:
        st.session_state[initial_data_key] = data
    __kwargs = _kwargs.copy()
    __kwargs.update({"data": data, "key": key, "on_change": on_data_editor_changed})
    return st.data_editor(**__kwargs)


def editar_taxa():
    st.session_state["alterar_taxa"] = not st.session_state["alterar_taxa"]


def card_valor(titulo, texto, width="stretch", height=120, color="#31333f"):
    if isinstance(width, int):
        height = width // 2
    with st.container(border=True, width=width, height=height):
        st.markdown(
            f"""
                <div style="text-align: center;">
                    <a style="font-size:16px;color:#6E6E6E">{titulo}</a>
                    </br>
                    <a style="font-size:24px;font-weight:bold;color:{color}">{texto}</a>
                </div>
            """,
            unsafe_allow_html=True,
        )


def card_valor_lucro(
    titulo, texto, lucro, width="stretch", height=120, color="#31333f"
):
    if isinstance(width, int):
        height = width
    with st.container(border=True, width=width, height=height):
        st.markdown(
            f"""
                <div style="text-align: center;">
                    <a style="font-size:16px;color:#6E6E6E">{titulo}</a>
                    </br>
                    <a style="font-size:24px;font-weight:bold;color:{color}">{texto}</a>
                    </br>
                    <a style="font-size:14px;font-weight:bold;color:{"#FF6E6E" if lucro < 0 else "#5BBF54"}">R${"" if lucro < 0 else "+"}{lucro:.2f}</a>
                </div>
            """,
            unsafe_allow_html=True,
        )


def card_valor_lucro_parcela(
    titulo, recebido, pago, lucro, width="stretch", height=150, color="#31333f"
):
    if isinstance(width, int):
        height = width
    with st.container(border=True, width=width, height=height):
        st.markdown(
            f"""
                <div style="text-align: center;">
                    <a style="font-size:16px;color:#6E6E6E">{titulo}</a>
                    </br>
                    <a style="font-size:18px;font-weight:bold;color:{color}">{pago}</a>
                    </br>
                    <a style="font-size:24px;font-weight:bold;color:{color}">{recebido}</a>
                    </br>
                    <a style="font-size:14px;font-weight:bold;color:{"#FF6E6E" if lucro < 0 else "#5BBF54"}">R${"" if lucro < 0 else "+"}{lucro:.2f}</a>
                </div>
            """,
            unsafe_allow_html=True,
        )


def calcular_parcelado(valor_pago, n_parcelas, taxa, taxa_adiantamento, repassar):
    taxa /= 100
    taxa_adiantamento /= 100

    dias_comercial = 30
    valor_parcela = valor_pago / n_parcelas
    valor_taxa = valor_parcela * taxa

    valor_receber = 0
    for parcela in range(1, n_parcelas + 1):
        desconto = (
            parcela
            * (
                taxa_adiantamento
                * ((dias_comercial * parcela) - 1)
                / (dias_comercial * parcela)
            )
            * (valor_parcela - valor_taxa)
        ) + valor_taxa
        if repassar:
            valor_pago += desconto
            valor_receber += valor_parcela
        else:
            valor_receber += valor_parcela - desconto

    return valor_pago, valor_receber

def taxas(qtd_parcelas): 
    for idx, intervalo in enumerate(tabela_taxa["intervalo"]):
        low, up = intervalo.split(";")
        if int(low) <= qtd_parcelas <= int(up):
            return tabela_taxa["cartao"][idx], tabela_taxa["adiantamento"][idx]

def main():
    qtd_guias = 2

    default_page_config()

    left, center, right = st.columns([0.2, 0.6, 0.2], vertical_alignment="top")

    left.write("**Configurações :material/settings:**")
    config_container = left.container(border=True)

    # config_container.toggle(
    #     label="Editar taxas",
    #     key="alterar_taxa",
    #     value=False,
    # )

    # taxa_cartao = config_container.number_input(
    #     label="Taxa do Cartão %",
    #     key="taxa_cartao",
    #     min_value=0.0,
    #     value=2.49,
    #     disabled=(not st.session_state["alterar_taxa"]),
    #     help="Verifique a tabela de taxas abaixo para ajustas as taxas conforme a forma de pagamento em estudo.",
    # )
    # taxa_adiantamento = config_container.number_input(
    #     label="Taxa de Adiantamento %",
    #     key="taxa_adiantamento",
    #     min_value=0.0,
    #     value=1.7,
    #     disabled=(not st.session_state["alterar_taxa"]),
    #     help="Verifique a tabela de taxas abaixo para ajustas as taxas conforme a forma de pagamento em estudo.",
    # )

    # tabela_taxa = config_container.expander("Tabela de Taxas", expanded=False)
    # tabela_taxa.table(
    #     data={
    #         "Condições": ["À vista", "De 2x a 6x", "De 7x a 13x"],
    #         "Cartão": ["1.99%", "2.49%", "2.99%"],
    #         "Adiant.": ["1.25%", "1.70%", "1.70%"],
    #     },
    #     border="horizontal",
    # )

    margem_lucro = config_container.number_input(
        label="Margem de Lucro %",
        key="margem_lucro",
        min_value=0,
        value=5,
    )
    desconto_10 = config_container.checkbox(
        label="Incluir o adicional de 10%",
        key="desconto_10",
        value=True,
        help="Escolha se irá incluir no valor do evento o desconto de 10% para as primeiras Entre Munders.",
    )
    lista_parcelas = [n for n in range(1, 14)]
    qtd_parcelas = config_container.selectbox(
        label="Quantidade de Parcelas",
        options=lista_parcelas,
        key="qtd_parcelas",
        index=0,
    )
    repassar_parcela = config_container.toggle(
        label="Repassar a taxa",
        value=False,
        key="repassar_parcela",
        help="O valor total das taxas será incluído no valor a ser pago pela Entre Munder.",
    )
    taxa_cartao, taxa_adiantamento = taxas(qtd_parcelas)
    config_container.badge(label=f"Taxa do Cartão: **{taxa_cartao}%** | Taxa de Adiantamento: **{taxa_adiantamento}%**", color="primary")

    left.write("**Informações do Evento**")
    evento_config_container = left.container(border=True)
    qtd_dias = evento_config_container.number_input(
        label="Quantidade de Dias",
        min_value=1,
        key="qtd_dias_evento",
        value=1,
    )
    min_pessoas = evento_config_container.number_input(
        label="Qtd. Mínima de Pessoas",
        min_value=1,
        key="qtd_minima_pessoas",
        value=4,
    )
    valor_diaria = evento_config_container.number_input(
        label="Valor da Diária **R$**",
        help="Quanto será pago para cada uma de vocês.",
        min_value=0.0,
        value=150.0,
    )
    diaria_individual = evento_config_container.checkbox(
        label="Diária para 1 guia",
        key="diaria_uma_guia",
        value=False,
        help="Se o valor da diária será para uma só (Viki ou Laura). O padrão é considerar a diária para duas.",
    )
    left.write("**Carregar Planilha de Custos**")
    st.session_state["custos_carregado"] = left.file_uploader(
        label="Insira planilha de custos que deseja",
        type=[
            "xlsx",
        ],
        key="uploader_custos",
    )

    if st.session_state["custos_carregado"] is not None:
        st.session_state["custos"] = pd.read_excel(st.session_state["custos_carregado"])

    if diaria_individual:
        qtd_guias = 1

    center_1, center_2 = center.columns(2, vertical_alignment="top")
    center_1.write("**Custos do Evento**")

    with center_1:
        custos_atualizado = dynamic_input_data_editor(
            data=st.session_state["custos"],
            key="editor_custos",
            hide_index=True,
            column_config={
                "nome": st.column_config.TextColumn(
                    label="Nome",
                    help="Adicione aqui os custos que não dependem da quantidade de pessoas envolvidas no evento. Por exemplo: ",
                ),
                "valor": st.column_config.NumberColumn(
                    label="Valor",
                    default=0.0,
                    format="R$ %.2f",
                ),
                "depende": st.column_config.CheckboxColumn(
                    label="Cobrado por pessoa?",
                    default=False,
                ),
            },
            num_rows="dynamic",
        )
        st.session_state["custos_file"] = save_output(custos_atualizado)

        st.download_button(
            label=":material/download: Planilha de Custos",
            key="baixar_custos",
            data=st.session_state["custos_file"],
            file_name=f"Custos - {datetime.today().strftime('%d-%m-%Y')}.xlsx",
            type="primary",
        )

    custo_fixo = 0
    custo_pessoa = 0
    for idx, row in custos_atualizado.iterrows():
        valor = row["valor"]
        depende = row["depende"]
        if depende:
            custo_pessoa += valor
        else:
            custo_fixo += valor

    taxa_incluir = 0
    if desconto_10:
        taxa_incluir += 10

    custo_diaria = qtd_guias * valor_diaria * qtd_dias
    custo_fixo += custo_diaria
    if custo_fixo == custo_diaria:  # Vazio
        custo_fixo = 0

    qtd_pessoas = min_pessoas + qtd_guias
    custo_variavel = custo_pessoa * qtd_pessoas
    custo_total = custo_variavel + custo_fixo
    custo_total_unit = custo_total / min_pessoas
    valor_unitario = (
        (custo_variavel * (1 + margem_lucro / 100)) + custo_fixo
    ) / min_pessoas
    valor_unitario /= (1 - taxa_incluir / 100) if desconto_10 else 1

    center_2.write("**Resumo**")
    with center_2:
        center2_col1, center2_col2 = st.columns(2, vertical_alignment="top")
        with center2_col1:
            card_valor("Custo Fixo", f"R${custo_fixo:.2f}")
            card_valor("Custo Total", f"R${custo_total:.2f}")
        with center2_col2:
            card_valor("Custo / Pessoa", f"R${custo_pessoa:.2f}")
            card_valor("Custo Total / Pessoa", f"R${custo_total_unit:.2f}")

    center.divider()
    center.write("**Parcelamento**")
    center_col1, center_col2, center_col3, center_col4 = center.columns(
        4, vertical_alignment="top"
    )
    valor_entre_munders = valor_unitario * (1 - 0.1)

    with center_col1:
        valor_pago, valor_receber = calcular_parcelado(
            valor_unitario,
            qtd_parcelas,
            taxa_cartao,
            taxa_adiantamento,
            repassar_parcela,
        )
        lucro = valor_receber - custo_total_unit
        card_valor_lucro_parcela(
            titulo=f"Parcelado {qtd_parcelas}x",
            recebido=f"R${valor_receber:.2f}",
            pago=f"R${valor_pago:.2f}",
            lucro=lucro,
        )
    with center_col2:
        valor_pago, valor_receber = calcular_parcelado(
            valor_entre_munders,
            qtd_parcelas,
            taxa_cartao,
            taxa_adiantamento,
            repassar_parcela,
        )
        lucro = valor_receber - custo_total_unit
        card_valor_lucro_parcela(
            titulo=f"EM 10% + Parcelado {qtd_parcelas}x",
            recebido=f"R${valor_receber:.2f}",
            pago=f"R${valor_pago:.2f}",
            lucro=lucro,
        )

    right.write("**Valores Calculados**")
    with right:
        lucro = valor_unitario - custo_total_unit
        card_valor_lucro(
            "Valor do Evento", f"R${valor_unitario:.2f}", lucro, color="#3892FF"
        )
        valor_pix = valor_unitario * (1 - 0.05)
        lucro = valor_pix - custo_total_unit
        card_valor_lucro("Pix 5%", f"R${valor_pix:.2f}", lucro)
        lucro = valor_entre_munders - custo_total_unit
        card_valor_lucro("EntreMunders 10%", f"R${valor_entre_munders:.2f}", lucro)
        valor_receber = valor_entre_munders * (1 - 0.05)
        lucro = valor_receber - custo_total_unit
        card_valor_lucro("EntreMunders 10% + Pix", f"R${valor_receber:.2f}", lucro)


if __name__ == "__main__":
    main()
