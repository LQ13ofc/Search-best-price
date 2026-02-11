# Correções de Bugs - v5.0.1

Este documento lista todas as correções críticas implementadas baseadas no relatório técnico.

## 🐛 Bugs Corrigidos

### 1. Lógica de Atualização das Abas (CRÍTICO)

**Problema:** O handler `tabs.on_change` era sobrescrito, impedindo a atualização de dados ao navegar entre abas.

**Solução:** Unificamos a lógica em uma única função `update_tab_content()` que:
- Troca o conteúdo visual
- Atualiza os dados (histórico, favoritos, gráficos, alertas)
- Tudo em uma única chamada

**Arquivo:** `main.py`

---

### 2. Cálculo de Preço do Google Shopping (CRÍTICO)

**Problema:** O parsing removia pontos decimais incorretamente:
- R$ 1.250,50 → "125050" → R$ 125.050,00

**Solução:** Parsing correto em 3 etapas:
1. Remove "R$" e espaços
2. Remove pontos de milhar
3. Converte vírgula para ponto decimal

**Exemplo:**
```python
# Antes: R$ 1.250,50 → 125050.0 ❌
# Agora: R$ 1.250,50 → 1250.5 ✅
```

**Arquivo:** `main.py` (função `buscar_google_shopping`)

---

### 3. Entry Point Inválido (CRÍTICO)

**Problema:** `setup.py` apontava para `main:main`, mas `main()` espera argumento `page`.

**Solução:** 
- Criada função `run_app()` que chama `ft.app(target=main)`
- Entry point agora aponta para `main:run_app`

**Arquivo:** `setup.py` e `main.py`

---

### 4. Perda Silenciosa de Dados (CRÍTICO)

**Problema:** Try/except vazios sobrescreviam arquivos corrompidos sem aviso.

**Solução:** Sistema de backup automático:
- Detecta arquivos JSON corrompidos
- Cria backup com timestamp: `data.json.backup.20240211_153045`
- Informa o usuário via console
- Mantém dados recuperáveis

**Arquivos:** `main.py` (funções `load_data`, `load_config`, `load_cache`)

---

### 5. Concorrência de Threading (GRAVE)

**Problema:** Thread de alertas atualizava UI diretamente, causando race conditions.

**Solução:** Uso de `page.run_task()` para operações thread-safe:
```python
# Antes
page.show_snack_bar(...)  # Chamado de thread ❌

# Agora
page.run_task(_show)  # Thread-safe ✅
```

**Arquivo:** `main.py` (função `show_notification`)

---

## 📊 Impacto das Correções

| Bug | Severidade | Impacto | Status |
|-----|-----------|---------|--------|
| Atualização de abas | 🔴 Crítico | Dados não carregavam | ✅ Corrigido |
| Parsing de preço | 🔴 Crítico | Preços absurdos | ✅ Corrigido |
| Entry point | 🔴 Crítico | App não iniciava via pip | ✅ Corrigido |
| Perda de dados | 🔴 Crítico | Dados apagados sem aviso | ✅ Corrigido |
| Threading | 🟡 Grave | Instabilidade/crashes | ✅ Corrigido |

---

## 🧪 Como Testar

### Teste 1: Navegação entre Abas
1. Execute o app
2. Adicione favoritos
3. Navegue entre abas
4. **Resultado esperado:** Favoritos aparecem corretamente

### Teste 2: Preços do Google Shopping
1. Configure API key da SerpAPI
2. Busque "notebook"
3. Compare preços ML vs Google Shopping
4. **Resultado esperado:** Preços realistas (não milhões)

### Teste 3: Entry Point
```bash
pip install -e .
cacador-precos
```
**Resultado esperado:** App abre normalmente

### Teste 4: Arquivo Corrompido
1. Edite `data.json` e quebre o JSON
2. Execute o app
3. **Resultado esperado:** Backup criado + mensagem de aviso

### Teste 5: Alertas
1. Adicione produto aos favoritos
2. Configure alerta
3. Deixe app rodando 30 min
4. **Resultado esperado:** Notificação aparece sem crash

---

## 📝 Notas Técnicas

### Parsing de Preço
A ordem importa:
```python
# Correto
price_clean = price.replace(".", "")  # Remove milhares
price_clean = price_clean.replace(",", ".")  # Converte decimal

# Incorreto
price_clean = price.replace(",", ".")  # 1.250,50 → 1.250.50
# filter(isdigit) remove TODOS os pontos
```

### Thread-Safety no Flet
Flet usa um event loop interno. Chamadas diretas de threads secundárias podem corromper o estado da UI. Sempre use:
- `page.run_task(func)` para operações assíncronas
- `page.update()` só na thread principal

### Backup de Dados
Os backups ficam no mesmo diretório:
```
data.json
data.json.backup.20240211_153045
data.json.backup.20240211_160230
```

Considere adicionar limpeza automática de backups antigos (>30 dias).

---

## 🚀 Próximos Passos

Bugs identificados mas não corrigidos nesta versão:

1. **Dependências da documentação:** `OTIMIZACAO.md` menciona `pandas`, `matplotlib`, `schedule` que não estão no `requirements.txt`
   - **Solução proposta:** Criar seção "Dependências Opcionais"

2. **Rate limiting:** Sem proteção contra exceder limites da API
   - **Solução proposta:** Implementar contador de requisições

3. **Validação de entrada:** Campos numéricos aceitam texto
   - **Solução proposta:** Validação com regex

---

## 📞 Reportar Novos Bugs

Encontrou um bug? Abra uma issue com:
1. Versão do app
2. Sistema operacional
3. Passos para reproduzir
4. Comportamento esperado vs real
5. Logs de erro (se houver)

---

**Versão:** 5.0.1  
**Data:** 11/02/2024  
**Correções:** 5 bugs críticos
