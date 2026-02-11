# Contribuindo

Obrigado por considerar contribuir! Aqui vão algumas diretrizes.

## Como contribuir

### Reportando bugs

Abra uma issue com:
- O que você estava fazendo
- O que esperava que acontecesse
- O que realmente aconteceu
- Seu OS e versão do Python

### Sugerindo funcionalidades

Abra uma issue explicando:
- Qual problema você quer resolver
- Como você imagina a solução
- Se pensou em alternativas

### Enviando código

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona funcionalidade X'`)
4. Push pra sua branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Style guide

O código segue mais ou menos o PEP 8, mas sem ser muito chato:
- Nomes de variáveis em português (já tá assim, vamos manter)
- Funções descritivas
- Comentários quando necessário, mas o código deve ser auto-explicativo
- Máximo 120 caracteres por linha

## Commits

Prefira commits em português e descritivos:
- `Adiciona filtro de frete grátis`
- `Corrige erro ao exportar CSV`
- `Melhora performance da busca`

## Testando

Antes de submeter:
```bash
# Instale as dependências
pip install -r requirements.txt

# Rode o app e teste manualmente
python main.py
```

Não temos testes automatizados ainda (PRs bem-vindos!), então teste bem antes de enviar.

## O que é bem-vindo

- Correção de bugs
- Novas funcionalidades
- Melhorias de performance
- Documentação
- Testes automatizados
- Integrações com outras lojas

## O que não vai ser aceito

- Mudanças que quebram compatibilidade sem justificativa
- Código ofuscado ou difícil de entender
- Features muito específicas que só você vai usar

## Dúvidas?

Abra uma issue ou manda uma mensagem.
