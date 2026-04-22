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

7. Rodada 7 (hipótese única C: calibrar 1 exemplo few-shot médio)
- Técnica(s) aplicada(s): ajuste pontual do exemplo few-shot médio (entrada e saída esperada), mantendo inalterados exemplo complexo, persona, regras, schema e metadata.
- Justificativa: calibrar representatividade do caso médio com padrão mais frequente no dataset para tentar elevar Correctness/F1 sem introduzir variáveis extras.
- Exemplo prático: substituição do caso médio de webhook por cenário de estoque no checkout com concorrência entre clientes, alinhado ao padrão de referência do dataset e ao formato de saída vigente.
- Adicionado na rodada: novo exemplo médio de bug de estoque no checkout (entrada + saída esperada completas).
- Removido na rodada: exemplo médio anterior de webhook de pagamento (entrada + saída esperada).
- Ajustado na rodada: apenas o conteúdo do Exemplo 1 (few-shot médio), sem alterações estruturais no prompt.
- Resultado da rodada: H 0.84, C 0.76, F1 0.69, Cl 0.84, P 0.83, média 0.7920; status reprovado; comparação vs Rodada 6: H +0.00, C +0.00, F1 +0.00, Cl -0.01, P +0.01, média +0.0014.

8. Rodada 8 (hipótese única A: missing_info_questions apenas com lacuna explícita)
- Técnica(s) aplicada(s): ajuste pontual de regra de geração condicional de `missing_info_questions`, mantendo inalterados few-shot, persona, schema, demais regras e metadata.
- Justificativa: reduzir perguntas desnecessárias quando o relato já contém informação suficiente, preservando precisão factual e objetividade da saída.
- Exemplo prático: regra 5 alterada para "Gerar perguntas em missing_info_questions somente quando houver lacuna explícita no bug report; se não houver lacuna explícita, não gerar perguntas".
- Adicionado na rodada: condição explícita de não gerar perguntas quando não houver lacuna explícita.
- Removido na rodada: gatilho anterior que vinculava perguntas a relatos incompletos/ambíguos de forma mais ampla.
- Ajustado na rodada: somente a regra 5 em `prompts/bug_to_user_story_v2.yml`.
- Resultado da rodada: H 0.83, C 0.75, F1 0.68, Cl 0.85, P 0.82, média 0.7879; status reprovado; comparação vs Rodada 7: H -0.01, C -0.01, F1 -0.01, Cl +0.01, P -0.01, média -0.0041.

9. Rodada 9 (rollback controlado da Rodada 8)
- Técnica(s) aplicada(s): rollback pontual da regra 5 para o estado da Rodada 7, mantendo inalterados few-shot, schema, persona, metadata e demais regras.
- Justificativa: validar regressão isolando exclusivamente a mudança da Rodada 8 em `missing_info_questions`, com o menor diff possível.
- Exemplo prático: regra 5 restaurada para "Se o relato estiver incompleto ou ambíguo, use linguagem conservadora, registre suposições mínimas em assumptions e faça perguntas objetivas em missing_info_questions".
- Adicionado na rodada: gatilho explícito de perguntas quando o relato estiver incompleto ou ambíguo, com orientação de linguagem conservadora e suposições mínimas.
- Removido na rodada: condição da Rodada 8 que limitava perguntas apenas a lacuna explícita e vedava perguntas quando não houvesse lacuna explícita.
- Ajustado na rodada: somente a regra 5 em `prompts/bug_to_user_story_v2.yml`.
- Resultado da rodada: H 0.83, C 0.75, F1 0.69, Cl 0.85, P 0.81, média 0.7868; status reprovado.
- Comparação Rodada 9 vs Rodada 7: H -0.01, C -0.01, F1 +0.00, Cl +0.01, P -0.02, média -0.0052.
- Comparação Rodada 9 vs Rodada 8: H +0.00, C +0.00, F1 +0.01, Cl +0.00, P -0.01, média -0.0011.

10. Rodada 10 (avaliação da versão v2 já refatorada)
- Técnica(s) aplicada(s): avaliação controlada (push + evaluate único) da versão refatorada em `prompts/bug_to_user_story_v2.yml`, já consolidada com arquitetura reduzida de 13 para 6 princípios, few-shot mais enxuto (2 exemplos) e política factual unificada.
- Justificativa: validar o desempenho da refatoração estrutural já incorporada ao prompt publicado no Hub, mantendo rastreabilidade objetiva da versão avaliada na rodada.
- Exemplo prático: `src/push_prompts.py` executado para publicar `joaofayad/bug_to_user_story_v2` (versão com 6 princípios obrigatórios), seguido de uma única execução de `src/evaluate.py` com persistência de saída via `tee` em `logs/rodada10_eval_20260418_183651.log`.
- Adicionado na rodada: registro cumulativo da avaliação da versão refatorada no README com métricas e deltas.
- Removido na rodada: nenhuma remoção adicional nesta rodada; a simplificação estrutural e do few-shot já estava incorporada na versão avaliada.
- Ajustado na rodada: sem novo diff de prompt após publicação; ajuste desta rodada foi de validação e documentação do estado refatorado.
- Resultado da rodada: H 0.83, C 0.74, F1 0.67, Cl 0.84, P 0.82, média 0.7784; status reprovado.
- Comparação Rodada 10 vs Rodada 9: H +0.00, C -0.01, F1 -0.02, Cl -0.01, P +0.01, média -0.0084.

11. Rodada 11 (reset estratégico para baseline Rodada 7)
- Técnica(s) aplicada(s): reset estratégico controlado com restauração integral de `prompts/bug_to_user_story_v2.yml` para o baseline da Rodada 7 (arquitetura anterior com 13 regras e few-shot médio+complexo), seguido de push e evaluate único.
- Justificativa: remover o efeito da refatoração da Rodada 10 (13 -> 6 princípios) e reestabelecer um baseline confiável para continuidade da Rodada 7+ sem introduzir hipótese nova.
- Exemplo prático: restauração exata do prompt com `Regras obrigatórias` 1..13 e Exemplo 1 de estoque no checkout (caso médio) + Exemplo 2 de checkout com falhas críticas (caso complexo), publicação via `src/push_prompts.py` e avaliação única via `src/evaluate.py | tee logs/rodada11_eval_20260418_184839.log`.
- Adicionado na rodada: registro cumulativo da Rodada 11 com reset estratégico, métricas e deltas comparativos.
- Removido na rodada: versão refatorada da Rodada 10 em `prompts/bug_to_user_story_v2.yml` (arquitetura de 6 princípios).
- Ajustado na rodada: conteúdo do prompt v2 restaurado exatamente para o baseline da Rodada 7; sem nova hipótese.
- Resultado da rodada: H 0.84, C 0.76, F1 0.69, Cl 0.85, P 0.84, média 0.7972; status reprovado.
- Comparação Rodada 11 vs Rodada 10: H +0.01, C +0.02, F1 +0.02, Cl +0.01, P +0.02, média +0.0188.
- Comparação Rodada 11 vs Rodada 7: H +0.00, C +0.00, F1 +0.00, Cl +0.01, P +0.01, média +0.0052.

12. Rodada 12 (ajuste pontual no few-shot complexo + avaliação)
- Técnica(s) aplicada(s): ajuste único no Exemplo 2 (few-shot complexo), com mapeamento mais explícito de problema -> critério de aceitação, seguido de push + evaluate único.
- Justificativa: aumentar F1/Correctness em casos complexos por cobertura factual mais direta dos problemas críticos explícitos no relato.
- Exemplo prático: no Exemplo 2, critérios foram ajustados para explicitar (i) tratamento de timeout 504 e encerramento de loading infinito com status claro, (ii) caso de cobrança sem pedido com orientação objetiva ao usuário, e (iii) vínculo explícito entre transação confirmada e criação do pedido correspondente.
- Adicionado na rodada: ajuste no Exemplo 2 para tornar explícito o mapeamento entre problemas críticos e acceptance_criteria, além do registro cumulativo da Rodada 12 com métricas e deltas vs Rodada 11.
- Removido na rodada: nenhuma remoção estrutural; somente substituição pontual de redação no Exemplo 2.
- Ajustado na rodada: conteúdo do Exemplo 2 (few-shot complexo) em `prompts/bug_to_user_story_v2.yml`; sem mudanças nas regras, schema, persona ou Exemplo 1.
- Resultado da rodada: H 0.83, C 0.76, F1 0.71, Cl 0.83, P 0.82, média 0.7908; status reprovado.
- Comparação Rodada 12 vs Rodada 11: H -0.01, C +0.00, F1 +0.02, Cl -0.02, P -0.02, média -0.0064.

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
