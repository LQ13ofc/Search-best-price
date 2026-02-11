# ⚡ Guia de Otimização e Boas Práticas

Maximize o desempenho do Caçador de Preços!

---

## 🚀 Performance

### Cache Inteligente

O cache é seu melhor amigo! Use-o sabiamente:

**✅ BOM:**
```python
# Busca a primeira vez - vai para a API
buscar("iPhone 15")  # ~5 segundos

# Busca novamente - vem do cache
buscar("iPhone 15")  # ~0.1 segundos
```

**❌ EVITE:**
```python
# Limpar cache a todo momento
limpar_cache()  # Você vai perder todos os benefícios!
```

### Intervalo de Verificação

Ajuste conforme necessário:

```python
# Para monitoramento frequente
CHECK_INTERVAL = 900  # 15 minutos

# Para economia de recursos
CHECK_INTERVAL = 3600  # 1 hora

# Padrão recomendado
CHECK_INTERVAL = 1800  # 30 minutos
```

### Limite de Resultados

Menos resultados = mais rápido:

```python
# Rápido mas menos resultados
"limit": 20

# Equilibrado (padrão)
"limit": 50

# Muitos resultados (mais lento)
"limit": 100
```

---

## 💾 Gerenciamento de Dados

### Tamanho do Histórico

Mantenha um tamanho razoável:

```python
# Leve e rápido
max_historico = 20

# Equilibrado (padrão)
max_historico = 30

# Muito histórico (pode ficar lento)
max_historico = 100
```

### Limpeza Automática

Configure limpeza periódica:

```python
# Limpar histórico antigo (>30 dias)
def limpar_historico_antigo():
    cutoff = datetime.now() - timedelta(days=30)
    data["price_history"] = {
        k: v for k, v in data["price_history"].items()
        if datetime.fromisoformat(v[-1]["date"]) > cutoff
    }
```

### Backup de Dados

Proteja seus dados:

```bash
# Linux/Mac
cp data.json data.json.backup

# Windows
copy data.json data.json.backup
```

**Automatize:**
```python
import shutil
from datetime import datetime

def backup_dados():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy("data.json", f"backup/data_{timestamp}.json")
```

---

## 🔍 Buscas Eficientes

### Termos Específicos

**✅ BOM:**
- "iPhone 15 Pro Max 256GB Titânio"
- "RTX 4090 Gigabyte Gaming OC"
- "Samsung Galaxy S24 Ultra 512GB"

**❌ EVITE:**
- "celular"
- "placa de vídeo"
- "notebook"

### Use Filtros

Economize tempo com filtros:

```python
# Busca ampla (muitos resultados irrelevantes)
buscar("tênis")

# Busca focada (resultados relevantes)
buscar("tênis", max_price=500, frete_gratis=True, loja="ml")
```

### Horários Recomendados

Aproveite os horários de menor tráfego:

- 🌙 **Madrugada (2h-6h):** Melhor performance
- 🌅 **Manhã (6h-10h):** Boa performance
- ☀️ **Tarde (14h-18h):** Performance normal
- 🌆 **Noite (20h-23h):** Mais lento

---

## 🔔 Alertas Inteligentes

### Quantidade Ideal

**✅ Recomendado:** 5-10 alertas ativos

**⚠️ Cuidado:** 20+ alertas podem sobrecarregar

### Preços Realistas

```python
# BOM ✅
iPhone 15: R$ 4.500 (preço real de mercado)

# RUIM ❌
iPhone 15: R$ 100 (nunca vai alertar!)
```

### Produtos Certos

Alertas funcionam melhor para:
- ✅ Eletrônicos (preços variam bastante)
- ✅ Games (promoções frequentes)
- ✅ TVs e monitores (boas ofertas)

Alertas menos úteis para:
- ❌ Comida perecível
- ❌ Produtos artesanais únicos
- ❌ Itens descontinuados

---

## 🎯 Favoritos Organizados

### Categorias

Organize por tipo:

```python
favoritos = {
    "eletronicos": [...],
    "games": [...],
    "casa": [...]
}
```

### Limpeza Regular

```python
# Remover favoritos antigos (>90 dias)
def limpar_favoritos_antigos():
    cutoff = datetime.now() - timedelta(days=90)
    data["favorites"] = [
        f for f in data["favorites"]
        if datetime.strptime(f["saved_date"], "%d/%m/%Y") > cutoff
    ]
```

---

## 📊 Análise de Dados

### Melhor Dia para Comprar

Analise seu histórico:

```python
def melhor_dia_semana():
    dias = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    
    for produto in data["price_history"].values():
        for registro in produto:
            data_obj = datetime.fromisoformat(registro["date"])
            dia = data_obj.weekday()
            dias[dia].append(registro["price"])
    
    # Calcular média por dia
    medias = {dia: sum(precos)/len(precos) for dia, precos in dias.items() if precos}
    melhor = min(medias, key=medias.get)
    
    dias_nome = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    return dias_nome[melhor]
```

### Economia Total

Veja quanto economizou:

```python
def calcular_economia():
    economia = 0
    for produto in data["favorites"]:
        historico = data["price_history"].get(produto["id"], [])
        if len(historico) >= 2:
            maior = max(h["price"] for h in historico)
            menor = min(h["price"] for h in historico)
            economia += (maior - menor)
    return economia
```

---

## 🛡️ Segurança

### Proteja sua API Key

```bash
# NUNCA faça isso:
SERPAPI_KEY="sk-1234567890"  # Commitado no Git!

# SEMPRE use variáveis de ambiente:
export SERPAPI_KEY="sk-1234567890"
```

### Gitignore

Certifique-se de ignorar:

```
data.json
cache.json
*.csv
.env
```

### Rate Limiting

Respeite os limites das APIs:

```python
# Mercado Livre: ~1000 requisições/dia
# SerpAPI Grátis: 100 requisições/mês

# Use cache para evitar atingir limites!
```

---

## 🔧 Troubleshooting Avançado

### Logs Detalhados

Ative logs para debug:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)
```

### Monitoramento de Performance

```python
import time

def buscar_com_timing(query):
    inicio = time.time()
    results = buscar(query)
    duracao = time.time() - inicio
    print(f"Busca levou {duracao:.2f}s")
    return results
```

### Verificar Integridade de Dados

```python
def verificar_dados():
    # Verificar estrutura
    assert "history" in data
    assert "favorites" in data
    assert "price_history" in data
    assert "alerts" in data
    
    # Verificar tipos
    assert isinstance(data["history"], list)
    assert isinstance(data["favorites"], list)
    
    print("✅ Dados OK!")
```

---

## 📱 Otimização Mobile (Futuro)

Preparando o código para mobile:

```python
# Usar async/await para não travar a UI
async def buscar_async(query):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Lazy loading de imagens
def carregar_imagem_lazy(url):
    # Carregar apenas quando visível
    pass

# Pagination
def paginar_resultados(results, page=1, per_page=20):
    start = (page - 1) * per_page
    end = start + per_page
    return results[start:end]
```

---

## 🎓 Dicas Pro

### 1. Combine Estratégias

```python
# Busca inicial ampla
buscar("notebook gamer")

# Refinar com filtros
buscar("notebook gamer", max_price=5000, frete_gratis=True)

# Adicionar aos favoritos os melhores
# Configurar alertas com preços-alvo
```

### 2. Monitore Tendências

```python
def detectar_tendencia(product_id):
    """Detecta se preço está subindo ou descendo."""
    historico = data["price_history"].get(product_id, [])
    if len(historico) < 3:
        return "Dados insuficientes"
    
    ultimos_3 = [h["price"] for h in historico[-3:]]
    if ultimos_3[-1] < ultimos_3[0]:
        return "📉 Tendência de queda"
    elif ultimos_3[-1] > ultimos_3[0]:
        return "📈 Tendência de alta"
    return "➡️ Estável"
```

### 3. Automatize Rotinas

```python
# Script para rodar toda noite
import schedule

def rotina_noturna():
    # Verificar alertas
    verificar_todos_alertas()
    
    # Atualizar favoritos
    atualizar_precos_favoritos()
    
    # Fazer backup
    backup_dados()
    
    # Limpar cache antigo
    limpar_cache_antigo()

schedule.every().day.at("03:00").do(rotina_noturna)
```

---

## 📚 Recursos Adicionais

### APIs Úteis

- **Mercado Livre:** https://developers.mercadolivre.com.br/
- **SerpAPI:** https://serpapi.com/google-shopping-api
- **Zoom:** https://developers.zoom.com.br/

### Bibliotecas Complementares

```bash
# Para web scraping avançado
pip install beautifulsoup4 selenium

# Para análise de dados
pip install pandas matplotlib

# Para notificações
pip install plyer  # Desktop
pip install twilio  # SMS
```

### Comunidade

- 💬 Discord: [link]
- 📧 Email: [email]
- 🐦 Twitter: [@usuario]

---

**Aproveite ao máximo o Caçador de Preços! 🚀**

*Dica final: A melhor otimização é comprar no preço certo! 💰*
