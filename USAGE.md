# Guia Rápido

## Instalação

```bash
pip install -r requirements.txt
python main.py
```

## Uso básico

1. **Buscar produto**: Digite o nome e clique em "Buscar"
2. **Filtrar**: Use os filtros de preço máximo, frete grátis, ou loja específica
3. **Favoritar**: Clique no coração para salvar produtos
4. **Alertas**: Configure alertas para ser notificado quando o preço baixar
5. **Exportar**: Exporte os resultados para CSV

## Configurando Google Shopping

1. Vá na aba "Configurações"
2. Crie conta em [serpapi.com](https://serpapi.com)
3. Cole sua API key
4. Clique em "Testar" e depois "Salvar"

## Dicas

- Use termos específicos para melhores resultados
- Configure alertas nos produtos que você realmente quer
- O cache é válido por 1 hora, então resultados recentes são instantâneos
- Limpe o cache se os preços parecerem desatualizados

## Problemas comuns

**App não abre**
```bash
pip install --upgrade -r requirements.txt
```

**Sem resultados do Google Shopping**
- Verifique se configurou a API key
- Veja se a key é válida
- Lembre que funciona perfeitamente só com Mercado Livre

**Alertas não funcionam**
- O app precisa estar rodando
- Produto precisa estar nos favoritos
- Alerta precisa estar ativado

## Estrutura de dados

Todos os seus dados ficam locais:
- `data.json` - Favoritos, histórico, alertas
- `cache.json` - Cache de buscas
- `config.json` - Suas configurações
