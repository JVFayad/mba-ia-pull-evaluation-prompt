## Técnicas Aplicadas (Fase 2)

1. Técnicas escolhidas para refatoração
- Few-shot Learning
- Role Prompting
- Explicit Output Schema (estrutura de saída explícita em Markdown)

2. Justificativa de escolha
- Few-shot Learning: requisito obrigatório do desafio e técnica útil para reduzir ambiguidade na transformação de bug report em user story. No v2, isso foi implementado com exemplos completos de entrada e saída esperada.
- Role Prompting: adiciona contexto operacional estável para a resposta. No v2, o sistema define o modelo como Product Manager sênior, orientando priorização, objetividade e foco em produto.
- Explicit Output Schema: melhora consistência de formato e facilita avaliação automática (clareza, precisão e corretude estrutural). No v2, a saída foi rigidamente definida em seções fixas.

3. Exemplos práticos de aplicação no prompt v2
- Few-shot Learning: inclusão de 3 exemplos reais no system_prompt, cobrindo cenário financeiro crítico (checkout), inconsistência de filtros/exportação e relato incompleto ("Está tudo quebrado no login.").
- Role Prompting: instrução explícita no início do system_prompt: persona de Product Manager sênior especializado em triagem de bugs e escrita de User Stories.
- Explicit Output Schema: imposição do formato de resposta com seções obrigatórias: user_story, acceptance_criteria, assumptions, missing_info_questions e observacoes; além da regra de responder somente nessa estrutura, sem texto extra.
