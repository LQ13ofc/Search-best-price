# Política de Segurança

## Versões suportadas

| Versão | Suportada          |
| ------ | ------------------ |
| 5.x    | :white_check_mark: |
| < 5.0  | :x:                |

## Reportando vulnerabilidades

Se você encontrou uma vulnerabilidade de segurança, **não abra uma issue pública**.

Em vez disso:

1. Envie um email para [seu-email]
2. Descreva a vulnerabilidade em detalhes
3. Inclua passos para reproduzir, se possível

Vamos responder em até 48 horas e trabalhar numa correção.

## Boas práticas

- Não compartilhe sua API key publicamente
- Não commite arquivos `config.json` ou `data.json`
- Mantenha suas dependências atualizadas
- Use senhas fortes se adicionar autenticação

## Dados pessoais

Este app não coleta dados pessoais. Tudo fica local no seu computador.

As únicas requisições externas são para:
- API do Mercado Livre (buscar produtos)
- SerpAPI (se configurada, para Google Shopping)
