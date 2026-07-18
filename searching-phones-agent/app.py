from io import BytesIO

import pandas as pd
import streamlit as st

from google_places_call import call_places_in_google
from text_queries_agent import generate_text_queries

st.set_page_config(
    page_title="Searching Phones Agent",
    page_icon="📞",
)

st.title("Searching Phones Agent")
st.write("Encontre estabelecimentos e exporte os contactos para Excel.")

with st.form("search_form"):
    city = st.text_input("Cidade")
    country = st.text_input("País")
    establishment_profile = st.text_input(
        "Perfil dos estabelecimentos",
        placeholder="Ex.: restaurantes relacionados com o Brasil",
    )

    submitted = st.form_submit_button("Pesquisar")

if submitted:
    if not city or not country or not establishment_profile:
        st.warning("Preencha todos os campos.")
    else:
        user_request = {
            "city": city,
            "country": country,
            "establishment_profile": establishment_profile,
        }

        with st.spinner("Pesquisando estabelecimentos..."):
            text_queries = generate_text_queries(user_request)

            formatted_places = []
            place_ids = set()

            for text_query in text_queries:
                places = call_places_in_google(text_query)

                for place in places:
                    place_id = place.get("id", "")
                    phone = place.get("internationalPhoneNumber", "")

                    if not phone:
                        continue

                    if place_id and place_id in place_ids:
                        continue

                    if place_id:
                        place_ids.add(place_id)

                    formatted_places.append({
                        "Nome": place.get("displayName", {}).get("text", ""),
                        "Telefone": phone,
                        "Endereço": place.get("formattedAddress", ""),
                        "Consulta utilizada": text_query,
                    })

        if not formatted_places:
            st.warning("Nenhum estabelecimento com telefone foi encontrado.")
        else:
            dataframe = pd.DataFrame(formatted_places)

            st.success(
                f"{len(dataframe)} estabelecimentos com telefone encontrados."
            )

            st.dataframe(
                dataframe,
                use_container_width=True,
                hide_index=True,
            )

            excel_file = BytesIO()

            with pd.ExcelWriter(
                excel_file,
                engine="openpyxl",
            ) as writer:
                dataframe.to_excel(
                    writer,
                    index=False,
                    sheet_name="Estabelecimentos",
                )

            excel_file.seek(0)

            st.download_button(
                label="Baixar Excel",
                data=excel_file,
                file_name="estabelecimentos_com_telefone.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
            )