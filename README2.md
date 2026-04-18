## Técnicas Aplicadas (Fase 2)

1. Few-shot Learning
- Técnica escolhida: few-shot learning com 3 exemplos.
- Justificativa: reduzir ambiguidade sem aumentar verbosidade, cobrindo padrões recorrentes de relato (crítico financeiro, inconsistência funcional, relato incompleto).
- Exemplo prático aplicado: exemplos completos de entrada e saída no system_prompt para checkout, filtros/exportação e login com pouco contexto.

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

1. Iteração 1 -> Iteração 2
- adicionado: persona explícita de Product Manager sênior.
- adicionado: schema de saída fixo em Markdown.
- adicionado: 3 exemplos few-shot completos.
- ajustado: regras de anti-alucinação e tratamento de lacunas.

2. Iteração 2 -> Iteração 3 (atual)
- removido: regra de foco exclusivo em um único bug com citação superficial dos demais.
- ajustado: estratégia para bugs múltiplos (user story principal + cobertura objetiva dos demais críticos em critérios/observações).
- adicionado: restrição adaptativa de quantidade de acceptance criteria por complexidade.
- adicionado: CoT estruturado interno sem exposição de raciocínio.
- ajustado: checklist final para exigir cobertura por complexidade e inclusão de problemas críticos adicionais.
- ajustado: techniques_applied para refletir exatamente as técnicas em uso.

3. Rodada atual (hipótese única focada em Correctness)
- adicionado: exigência explícita de cobertura factual por problema crítico explícito em casos médio/complexo.
- removido: nenhuma regra nesta rodada.
- ajustado: regra de acceptance_criteria para vedar inferência de solução técnica nessa cobertura.

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
