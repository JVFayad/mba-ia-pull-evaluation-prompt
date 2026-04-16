"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """Faz pull do prompt inicial do LangSmith Prompt Hub e salva localmente."""
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    output_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v1.yml"

    print_section_header("Pull de Prompt do LangSmith")
    print(f"Prompt: {prompt_name}")

    try:
        prompt = hub.pull(prompt_name)
    except Exception as exc:
        print(f"Erro ao fazer pull do prompt '{prompt_name}': {exc}")
        return False

    system_prompt = ""
    user_prompt = "{bug_report}"

    messages = getattr(prompt, "messages", [])
    if messages:
        for message in messages:
            class_name = message.__class__.__name__.lower()
            message_template = getattr(getattr(message, "prompt", None), "template", "")

            if "system" in class_name and message_template:
                system_prompt = message_template
            elif ("human" in class_name or "user" in class_name) and message_template:
                user_prompt = message_template

    if not system_prompt:
        system_prompt = getattr(prompt, "template", "")

    if not system_prompt:
        print("Erro: não foi possível extrair o system_prompt do prompt remoto.")
        return False

    metadata = getattr(prompt, "metadata", {}) or {}
    if not isinstance(metadata, dict):
        metadata = {}

    tags = metadata.get("tags", ["bug-analysis", "user-story", "product-management"])
    if isinstance(tags, str):
        tags = [tags]

    prompt_data = {
        "bug_to_user_story_v1": {
            "description": metadata.get(
                "description",
                "Prompt para converter relatos de bugs em User Stories",
            ),
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": metadata.get("version", "v1"),
            "created_at": metadata.get("created_at", date.today().isoformat()),
            "tags": tags,
        }
    }

    if not save_yaml(prompt_data, str(output_path)):
        print(f"Erro ao salvar prompt em: {output_path}")
        return False

    print(f"Prompt salvo com sucesso em: {output_path}")
    return True


def main():
    """Função principal"""
    required_vars = ["LANGSMITH_API_KEY"]

    if not check_env_vars(required_vars):
        return 1

    success = pull_prompts_from_langsmith()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
