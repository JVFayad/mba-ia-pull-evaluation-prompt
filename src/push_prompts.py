"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_data["system_prompt"]),
            ("human", prompt_data.get("user_prompt", "{bug_report}")),
        ])

        metadata = {
            "description": prompt_data.get("description", ""),
            "version": prompt_data.get("version", ""),
            "created_at": prompt_data.get("created_at", ""),
            "tags": prompt_data.get("tags", []),
            "techniques_applied": prompt_data.get("techniques_applied", []),
        }
        prompt_template.metadata = metadata

        hub.push(
            prompt_name,
            prompt_template,
            new_repo_is_public=True,
            new_repo_description=metadata["description"],
            tags=metadata["tags"],
        )
        print(f"✓ Prompt publicado: {prompt_name}")
        return True
    except Exception as exc:
        print(f"Erro ao fazer push do prompt '{prompt_name}': {exc}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    required_fields = ["description", "system_prompt", "version"]
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {field}")

    system_prompt = prompt_data.get("system_prompt", "").strip()
    if not system_prompt:
        errors.append("system_prompt está vazio")

    user_prompt = prompt_data.get("user_prompt", "").strip()
    if not user_prompt:
        errors.append("user_prompt está vazio")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("Push de Prompts Otimizados para LangSmith")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    prompts_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "prompts",
        "bug_to_user_story_v2.yml",
    )

    all_prompts = load_yaml(prompts_path)
    if not all_prompts:
        print(f"Erro ao carregar prompts de: {prompts_path}")
        return 1

    prompt_key = "bug_to_user_story_v2"
    prompt_data = all_prompts.get(prompt_key)

    if not prompt_data:
        print(f"Erro: prompt '{prompt_key}' não encontrado no arquivo YAML.")
        return 1

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("Erro de validação do prompt:")
        for error in errors:
            print(f"- {error}")
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    prompt_name = f"{username}/{prompt_key}"

    print(f"Prompt local: {prompt_key}")
    print(f"Destino Hub: {prompt_name}")

    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
