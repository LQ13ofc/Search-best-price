# Caçador de Preços

Comparador de preços que busca produtos no Mercado Livre e Google Shopping, com sistema de alertas e rastreamento de preços.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Funcionalidades

- Busca simultânea em múltiplas lojas
- Sistema de favoritos
- Alertas de preço personalizados
- Histórico de variações de preço
- Exportação para CSV
- Cache inteligente

## Instalação

```bash
git clone https://github.com/seu-usuario/cacador-precos.git
cd cacador-precos
pip install -r requirements.txt
python main.py
```

## Configuração

A chave da API do Google Shopping pode ser configurada diretamente no app (aba Configurações) ou via variável de ambiente:

```bash
export SERPAPI_KEY="sua_chave"
```

Obtenha uma chave gratuita em [serpapi.com](https://serpapi.com) (100 buscas/mês).

O app funciona normalmente sem a chave, usando apenas o Mercado Livre.

## Uso

1. Digite o nome do produto
2. Aplique filtros (opcional): preço máximo, frete grátis, loja específica
3. Clique em Buscar
4. Adicione produtos aos favoritos
5. Configure alertas de preço

### Alertas

Configure alertas para ser notificado quando o preço de um produto favorito baixar:

1. Adicione o produto aos favoritos
2. Vá para aba Alertas
3. Defina o preço desejado
4. Deixe o app rodando

### Análise de Preços

O histórico de preços é rastreado automaticamente. Veja a evolução na aba Análise.

## Estrutura

```
cacador-precos/
├── main.py              # Aplicação principal
├── requirements.txt     # Dependências
├── data.json           # Dados persistentes (gerado)
├── cache.json          # Cache de buscas (gerado)
└── config.json         # Configurações (gerado)
```

## Dependências

- flet - Interface gráfica
- httpx - Requisições HTTP assíncronas

## Roadmap

- [ ] App mobile
- [ ] Mais marketplaces
- [ ] Notificações por email
- [ ] Gráficos interativos

## Licença

MIT

## Contribuindo

Pull requests são bem-vindos. Para mudanças maiores, abra uma issue primeiro.
