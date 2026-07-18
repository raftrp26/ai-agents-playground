import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv("../.env")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_text_queries(user_request):
    prompt = f"""
    Crie consultas objetivas para pesquisar estabelecimentos na Google Places API.

    Cidade: {user_request["city"]}
    País: {user_request["country"]}
    Perfil procurado: {user_request["establishment_profile"]}

    Expanda o perfil em diferentes tipos concretos de estabelecimentos.
    Evite consultas repetidas ou excessivamente genéricas.
    Gere entre 1 e 5 consultas. Cada consulta deve representar uma categoria diferente.
    Retorne somente a estrutura solicitada, sem explicações.
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "google_places_queries",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "text_queries": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "minItems": 1,
                            "maxItems": 5
                        }
                    },
                    "required": ["text_queries"],
                    "additionalProperties": False
                }
            }
        }
    )

    result = json.loads(response.output_text)

    return result["text_queries"]