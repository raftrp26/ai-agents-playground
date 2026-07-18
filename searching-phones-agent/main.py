from google_places_call import call_places_in_google
from text_queries_agent import generate_text_queries


def get_user_input():
    city = input("Qual cidade você quer pesquisar? ").strip()
    country = input("Qual país? ").strip()
    establishment_profile = input(
        "Qual perfil de estabelecimento você procura? "
    ).strip()

    return {
        "city": city,
        "country": country,
        "establishment_profile": establishment_profile,
    }


user_request = get_user_input()

text_queries = generate_text_queries(user_request)

first_text_query = text_queries[0]

print(f"\nTestando consulta: {first_text_query}")

places = call_places_in_google(first_text_query)

formatted_places = []

for place in places:
    formatted_places.append({
        "name": place.get("displayName", {}).get("text", ""),
        "phone": place.get("internationalPhoneNumber", "")
    })

print(formatted_places)

