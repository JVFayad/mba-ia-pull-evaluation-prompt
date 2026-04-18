## Técnicas Aplicadas (Fase 2)

1. Few-shot Learning
- Técnica escolhida: few-shot learning com 2 exemplos calibrados (médio + complexo).
- Justificativa: reduzir ambiguidade sem aumentar verbosidade, cobrindo padrões recorrentes de relato (crítico financeiro, inconsistência funcional, relato incompleto).
- Exemplo prático aplicado: exemplos completos de entrada e saída no system_prompt para cenário médio (webhook de pagamento) e cenário complexo (checkout com múltiplas falhas críticas).

2. Role Prompting
- Técnica escolhida: role prompting (Product Manager sênior).
- Justificativa: estabilizar tom, priorização e foco em impacto de negócio/usuário.
- Exemplo prático aplicado: abertura do system_prompt define explicitamente a persona e o objetivo de triagem + escrita de user story acionável.

3. Explicit Output Schema
- Técnica escolhida: estrutura de saída explícita em Markdown.
- Justificativa: melhorar consistência estrutural e auditabilidade automática de campos esperados.
- Exemplo prático aplicado: seções fixas obrigatórias (user_story, acceptance_criteria, assumptions, missing_info_questions, observacoes), com regra de não emitir texto fora do formato.

4. Structured Internal CoT
- Técnica escolhida: CoT estruturado interno (não exibido).
- Justificativa: aumentar cobertura semântica em casos médios/complexos sem sacrificar clareza da saída final.
- Exemplo prático aplicado: instrução interna sequencial: extrair fatos -> agrupar problemas -> mapear impactos -> gerar saída final.

5. Adaptive Constraints by Complexity
- Técnica escolhida: restrição adaptativa de critérios por complexidade.
- Justificativa: recuperar Correctness/F1 em casos médios e complexos por maior cobertura objetiva.
- Exemplo prático aplicado: simples >=3 critérios; médio 4-6; complexo 6-10, com orientação de classificação por fluxos afetados, impacto e ambiguidades.

## Rastreio por Iteração

1. Rodada 1 (Iteração 1 -> Iteração 2)
- Técnica(s) aplicada(s): role prompting, explicit output schema, few-shot.
- Justificativa: aumentar consistência de formato e reduzir ambiguidade na transformação de bug report em user story.
- Exemplo prático: inclusão da persona de Product Manager sênior, seções fixas em Markdown e 3 exemplos few-shot completos.
- Resultado da rodada: melhoria de padronização da saída, com base para iterações posteriores.

2. Rodada 2 (Iteração 2 -> Iteração 3)
- Técnica(s) aplicada(s): CoT estruturado interno, adaptive constraints by complexity, ajuste de estratégia para bugs múltiplos.
- Justificativa: ampliar cobertura semântica e recuperar aderência em casos médios/complexos.
- Exemplo prático: regra de user story principal com cobertura objetiva dos demais críticos, critérios por complexidade e checklist final de cobertura.
- Resultado da rodada: prompt mais robusto para cenários com múltiplos problemas e maior controle de completude.

3. Rodada 3 (hipótese única focada em coverage factual/correctness)
- Técnica(s) aplicada(s): hipótese única de cobertura factual explícita por problema crítico em casos médio/complexo, sem mudança estrutural adicional.
- Justificativa: testar se maior completude factual, sem inferência de solução técnica, elevaria coverage e Correctness sem introduzir novas variáveis.
- Exemplo prático: reforço da regra de cobrir cada problema crítico explícito em acceptance_criteria e/ou observacoes, mantendo schema e fluxo anteriores.
- Resultado da rodada: sem ganho de métricas; hipótese isolada não melhorou os indicadores de avaliação.

4. Rodada 4 (few-shot calibrado)
- Técnica(s) aplicada(s): few-shot calibrado com 2 exemplos (médio + complexo).
- Justificativa: melhorar generalização em casos de maior ambiguidade com exemplos mais representativos e objetivos.
- Exemplo prático: substituição/ajuste dos exemplos no system_prompt para cenário médio de webhook de pagamento e cenário complexo de checkout com múltiplas falhas críticas, com saída alinhada ao schema.
- Resultado da rodada: ganho de métricas em relação à rodada anterior, com recuperação de desempenho em critérios de qualidade.

5. Rodada 5 (hipótese única: deduplicação semântica em acceptance_criteria)
- Técnica(s) aplicada(s): hipótese única de deduplicação semântica dos acceptance_criteria com regra de fato distinto por critério.
- Justificativa: melhorar Clarity reduzindo redundância semântica entre critérios e preservando cobertura factual objetiva.
- Exemplo prático: adicionado requisito de fato distinto por item em acceptance_criteria; removido nenhum elemento; ajustada a regra de linguagem direta para incluir anti-redundância semântica entre critérios.
- Resultado da rodada: H 0.82, C 0.74, F1 0.68, Cl 0.84, P 0.80, média 0.7761; status reprovado; comparação vs Rodada 4: H -0.02, C -0.02, F1 -0.01, Cl -0.01, P -0.02, média -0.0145.

6. Rodada 6 (rollback controlado da hipótese da Rodada 5)
- Técnica(s) aplicada(s): rollback pontual da deduplicação semântica em acceptance_criteria na regra 13, preservando o restante do prompt v2.
- Justificativa: isolar a variável da Rodada 5 e verificar recuperação de desempenho sem introduzir novas mudanças de estrutura, few-shot, persona ou schema.
- Exemplo prático: remoção apenas do trecho "cada critério deve cobrir um fato distinto do relato e não repetir o mesmo problema com redações diferentes" na regra de linguagem direta.
- Resultado da rodada: H 0.84, C 0.76, F1 0.69, Cl 0.85, P 0.82, média 0.7906; status reprovado; comparação vs Rodada 4: H +0.00, C +0.00, F1 +0.00, Cl +0.00, P +0.00, média +0.0000.

## Jornada de Otimização (Iterações)

1. Baseline e resultados comparativos
- Iteração 1 (baseline): Helpfulness 0.83, Correctness 0.76, F1 0.71, Clarity 0.85, Precision 0.81, média 0.7911.
- Iteração 2: Helpfulness 0.83, Correctness 0.74, F1 0.67, Clarity 0.85, Precision 0.81, média 0.7793.
- Leitura objetiva: houve regressão em Correctness, F1 e média, com estabilidade em Helpfulness, Clarity e Precision.

2. Análise de causa raiz (prática)
- Hipótese principal: a maior rigidez de formatação no v2 pode ter aumentado consistência estrutural, mas reduziu aderência semântica em casos ambíguos, impactando Correctness e F1.
- Hipótese complementar: exemplos few-shot existentes podem não cobrir variações suficientes de bugs complexos, gerando perda de generalização.

3. Decisão de processo adotada
- Antes de nova edição de prompt, executar diagnóstico profundo por exemplo (erro por erro), mapeando onde a saída falha em conteúdo, cobertura e interpretação do bug.

4. Próximos ajustes planejados
- Executar push do prompt atualizado (v2) para o hub.
- Rodar avaliação com dataset completo para medir impacto em Correctness e F1.
- Aplicar gate humano: só avançar para nova iteração após aprovação explícita.

5. Gate humano entre iterações
- Após cada rodada de ajuste e avaliação, nova iteração só avança com aprovação explícita do usuário.
