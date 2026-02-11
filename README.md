# Caçador de Preços

Compare preços entre Mercado Livre e Google Shopping.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Instalação

### Passo 1: Instalar Python

Se ainda não tem Python instalado:
- **Windows**: Baixe em [python.org](https://www.python.org/downloads/)
  - ⚠️ **IMPORTANTE**: Marque "Add Python to PATH" durante a instalação!
- **Linux**: `sudo apt install python3 python3-pip`
- **Mac**: `brew install python3`

### Passo 2: Instalar dependências

**Windows**: Clique duas vezes em `install.bat`

**Linux/Mac**:
```bash
chmod +x install.sh
./install.sh
```

Ou manualmente:
```bash
pip install -r requirements.txt
```

### Passo 3: Executar

**Windows**: Clique duas vezes em `run.bat`

**Linux/Mac**:
```bash
chmod +x run.sh
./run.sh
```

Ou manualmente:
```bash
python main.py
```

## Primeiros passos

1. Digite o nome do produto (ex: "iPhone 15")
2. Clique em "Buscar"
3. Veja os resultados e clique no coração para favoritar
4. (Opcional) Configure alertas na aba "Alertas"

## Configurar Google Shopping (opcional)

O app funciona perfeitamente só com Mercado Livre. Mas se quiser buscar no Google Shopping também:

1. Execute o app
2. Vá na aba "Configurações"
3. Crie conta grátis em [serpapi.com](https://serpapi.com)
4. Copie sua API key
5. Cole no campo e clique em "Salvar"

Pronto! Agora você tem acesso a mais lojas.

## Funcionalidades

- ✅ Busca simultânea em múltiplas lojas
- ✅ Filtros (preço máximo, frete grátis, loja específica)
- ✅ Sistema de favoritos
- ✅ Alertas de preço (te avisa quando baixar)
- ✅ Histórico de preços
- ✅ Exportar para CSV
- ✅ Cache inteligente (1 hora)

## Problemas?

### App não abre

**Solução 1**: Verifique se Python está instalado
```bash
python --version
```
Deve mostrar algo como `Python 3.11.5`

**Solução 2**: Reinstale as dependências
```bash
pip install --upgrade -r requirements.txt
```

**Solução 3**: Execute direto
```bash
python main.py
```

Se aparecer erro, copie a mensagem e abra uma issue.

### Sem resultados do Google Shopping

Isso é normal! O app funciona só com Mercado Livre. Para adicionar Google Shopping, configure a API key (veja acima).

### Alertas não funcionam

- O app precisa estar rodando
- O produto precisa estar nos favoritos
- O alerta precisa estar ativado (switch verde)

## Estrutura de arquivos

Ao executar pela primeira vez, o app cria:
- `data.json` - Seus favoritos, histórico e alertas
- `cache.json` - Cache de buscas
- `config.json` - Suas configurações

Tudo fica no seu computador, nada vai pra nuvem.

## Contribuindo

PRs são bem-vindos! Veja [CONTRIBUTING.md](CONTRIBUTING.md)

## Licença

MIT - Use como quiser.

## Créditos

- [Mercado Livre API](https://developers.mercadolibre.com.br/)
- [SerpAPI](https://serpapi.com/) (Google Shopping)
- [Flet](https://flet.dev/) (Framework)
