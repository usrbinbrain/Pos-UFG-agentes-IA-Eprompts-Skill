---
name: code-token-optimizer
description: Minifica arquivos de código-fonte nativamente pelo LLM, modificando os arquivos originais diretamente no projeto. Exclui documentações e configurações. Reduz o tamanho do código preservando o comportamento original, sem usar scripts externos.
---

# Code Token Optimizer — Agent-native

## Objetivo
Você, o agente, deve inspecionar e minificar os arquivos de código-fonte **manualmente e diretamente nos originais (in-place)**. **NÃO** use scripts de terceiros, bundlers ou compiladores. O objetivo é reduzir o número de caracteres de forma segura, sem alterar a lógica ou o comportamento do código.

## Escopo e Exclusões
1. **Inclua** apenas arquivos de código-fonte escritos por humanos.
2. **Exclua** documentação, arquivos de configuração e dependências. Exemplos: `README*`, `*.md`, `*.json`, `*.yaml`, `*.toml`, `*.env`, `Dockerfile`, lockfiles, arquivos de teste e assets.
3. **Ignore** diretórios gerados ou externos: `.git/`, `.github/`, `node_modules/`, `vendor/`, `dist/`, `build/` e a pasta `.ai-context/`.
4. **Nunca** leia ou altere chaves privadas e segredos.

## Procedimento (Para cada arquivo válido)
1. **Analise:** Leia o arquivo original e entenda as restrições da linguagem (sintaxe, dependências, sensibilidade a espaços).
2. **Minifique:** Reduza os caracteres. Remova espaços em branco, quebras de linha e comentários não essenciais sempre que a linguagem permitir.
   - *Segurança:* Não renomeie variáveis exportadas ou interfaces públicas. Preserve a indentação obrigatória (ex: Python) e comentários vitais (licenças, pragmas). Se não tiver certeza sobre uma alteração, não faça.
3. **Sobrescreva:** Aplique o código minificado **diretamente no arquivo original**, substituindo seu conteúdo.
4. **testes/execução:** Não realize validações automáticas. Se o projeto tiver testes ou linting configurados, não os rode para garantir que a alteração não quebrou o código. Não é necessário executar o código, apenas minificá-lo.
5. **Registre as Métricas:** Anote o tamanho exato de caracteres antes e depois da minificação para gerar o relatório final.

## Finalização e Resposta
1. **Relatório de Modificações:** Crie (ou atualize) o arquivo `.ai-context/minification-report.md` com uma tabela detalhada contendo:
   - Nome do arquivo modificado
   - Status (Processado / Ignorado)
   - Caracteres Originais vs Minificados
   - Redução total em quantidade absoluta (ex: -150 caracteres)
   - Redução em porcentagem (ex: -12%)
2. **Responda no Chat:** Apresente um resumo claro e direto informando quais arquivos foram modificados e a redução total alcançada (quantidade absoluta de caracteres economizados e o percentual geral de redução).
