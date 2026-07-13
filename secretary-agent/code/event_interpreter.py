import os
from datetime import datetime
from typing import Literal, Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY não encontrada. "
        "Verifique se o arquivo .env existe e contém a chave."
    )

client = OpenAI(api_key=api_key)


class CalendarEvent(BaseModel):
    title: Optional[str] = Field(
        default=None,
        description=(
            "Título específico do evento informado ou claramente "
            "deduzido da mensagem. Nunca use 'CalendarEvent', "
            "'Evento' ou o nome da classe como preenchimento."
        ),
    )

    start_datetime: Optional[str] = Field(
        default=None,
        description=(
            "Data e hora de início em ISO 8601 com offset. "
            "Deixe como null caso a data ou o horário não estejam claros."
        ),
    )

    end_datetime: Optional[str] = Field(
        default=None,
        description=(
            "Data e hora de término em ISO 8601 com offset. "
            "Deixe como null caso o horário final ou a duração "
            "não tenham sido informados."
        ),
    )

    timezone: str = Field(
        default="Europe/Lisbon",
        description="Fuso horário IANA do evento.",
    )

    description: Optional[str] = None
    location: Optional[str] = None

    attendees: list[str] = Field(
        default_factory=list,
        description="E-mails de convidados explicitamente informados.",
    )

    missing_fields: list[str] = Field(
        default_factory=list,
        description=(
            "Campos obrigatórios ausentes ou ambíguos. "
            "Use apenas: title, start_datetime ou end_datetime."
        ),
    )

    clarification_questions: list[str] = Field(
        default_factory=list,
        description=(
            "Perguntas curtas que devem ser feitas ao usuário "
            "para completar os campos ausentes."
        ),
    )

    interpretation_notes: Optional[str] = Field(
        default=None,
        description=(
            "Observações sobre informações interpretadas, "
            "sem inventar dados."
        ),
    )

    status: Literal[
        "needs_clarification",
        "ready_for_confirmation",
    ] = Field(
        description=(
            "Use needs_clarification quando faltar informação obrigatória. "
            "Use ready_for_confirmation quando o evento estiver completo."
        ),
    )


def interpret_calendar_event(
    transcription: str,
    current_datetime: datetime,
) -> CalendarEvent:

    system_prompt = """
Você é o módulo de interpretação de uma secretária virtual.

Sua função é transformar uma solicitação do usuário em dados
estruturados para um evento do Google Calendar.

Campos obrigatórios:
- title
- start_datetime
- end_datetime

Regras obrigatórias:

1. Não invente informações.

2. A data e hora atuais servem somente para resolver expressões
   relativas como "hoje", "amanhã" e "sexta-feira".

3. Nunca use a hora atual como horário do evento quando o usuário
   não tiver informado um horário.

4. Nunca assuma uma duração padrão.

5. Para preencher end_datetime, o usuário precisa informar:
   - o horário final; ou
   - uma duração clara.

6. Não use "CalendarEvent", "Evento" ou o nome da classe como título.

7. Caso o título não esteja suficientemente definido, deixe title
   como null e inclua "title" em missing_fields.

8. Caso a data ou o horário inicial estejam ausentes ou ambíguos,
   deixe start_datetime como null e inclua "start_datetime"
   em missing_fields.

9. Caso o horário final ou a duração estejam ausentes,
   deixe end_datetime como null e inclua "end_datetime"
   em missing_fields.

10. Para cada campo ausente, produza uma pergunta curta e objetiva
    em clarification_questions.

11. Use status="needs_clarification" se missing_fields não estiver vazio.

12. Use status="ready_for_confirmation" somente quando title,
    start_datetime e end_datetime estiverem completos.

13. Mesmo quando estiver completo, não crie o evento.
    O usuário ainda precisará confirmar.

14. Considere Europe/Lisbon como fuso padrão.

15. Retorne datas no formato ISO 8601 com offset.
""" 

    user_prompt = f"""
Data e hora atuais:
{current_datetime.isoformat()}

Transcrição:
{transcription}
"""

    response = client.responses.parse(
        model="gpt-4o-mini",
        instructions=system_prompt,
        input=user_prompt,
        text_format=CalendarEvent,
    )

    return response.output_parsed