# ❓ Perguntas Frequentes (FAQ)

## 📥 Instalação

### Como instalo o app?

**Windows:**
1. Clique duas vezes em `instalar.bat`
2. Aguarde a instalação
3. Execute: `python cacador_precos_v5.py`

**Linux/Mac:**
```bash
chmod +x instalar.sh
./instalar.sh
python3 cacador_precos_v5.py
```

### Preciso instalar Python?

**Para rodar o código:** Sim, Python 3.8 ou superior
**Para usar o .exe:** Não! Basta ter o arquivo executável

### Como crio o executável (.exe)?

**Windows:**
```bash
criar_executavel.bat
```

O arquivo estará em: `dist/CacadorPrecos.exe`

---

## 🔑 Google Shopping

### Preciso da chave SerpAPI?

**Não é obrigatório!** O app funciona apenas com Mercado Livre.

Mas para ter mais resultados do Google Shopping:
1. Crie conta grátis em [serpapi.com](https://serpapi.com)
2. 100 buscas/mês grátis
3. Configure: `set SERPAPI_KEY=sua_chave`

### Como sei se a chave está funcionando?

Se você ver resultados de lojas como "Amazon", "Magazine Luiza" além do Mercado Livre, está funcionando!

---

## 🔍 Buscas

### Por que não encontro resultados?

**Possíveis causas:**
1. Termo muito genérico ("celular")
2. Produto não existe nessas lojas
3. Preço máximo muito baixo
4. Filtros muito restritivos

**Solução:** Use termos específicos e remova filtros.

### Quantos resultados aparecem?

- Mercado Livre: até 50 produtos
- Google Shopping: até 30 produtos
- Total: até 80 produtos por busca

### Os preços são atualizados?

- **Cache:** Válido por 1 hora
- **Favoritos:** Atualize manualmente
- **Alertas:** Verificados a cada 30 minutos

---

## ⭐ Favoritos

### Como adiciono favoritos?

Clique no ícone ❤️ em qualquer produto.

### Favoritos são salvos?

Sim! Tudo é salvo em `data.json` no seu computador.

### Posso exportar favoritos?

Sim! Vá em Favoritos → Exportar CSV

---

## 🔔 Alertas

### Como funcionam os alertas?

1. Adicione produto aos favoritos
2. Configure alerta com preço desejado
3. O app verifica a cada 30 minutos
4. Você recebe notificação quando o preço baixar

### Preciso deixar o app aberto?

**Sim!** Alertas só funcionam com o app rodando.

**Dica:** Minimize o app na bandeja do sistema.

### Por que não recebo notificações?

**Verifique:**
1. App está rodando?
2. Produto está nos favoritos?
3. Alerta está ativado (switch ligado)?
4. Preço atual já está abaixo do alerta?

---

## 📊 Gráficos

### Por que não vejo gráficos?

Você precisa:
1. Adicionar produtos aos favoritos
2. Aguardar algumas buscas/verificações
3. Ter pelo menos 2 registros de preço

### Como funciona o histórico?

O app salva automaticamente:
- Cada vez que você busca
- Cada verificação de alertas
- Até 30 registros por produto

---

## 💾 Dados e Privacidade

### Onde meus dados são salvos?

**Localmente** no seu computador:
- `data.json` - Favoritos, histórico, alertas
- `cache.json` - Cache de buscas

### Meus dados vão para a internet?

**Não!** Tudo é 100% local.

As únicas requisições são para:
- API do Mercado Livre (buscar produtos)
- SerpAPI (se configurada)

### Posso deletar tudo?

Sim! Delete os arquivos:
- `data.json`
- `cache.json`

Ou use as opções de limpar no app.

---

## 📥 Exportação

### Como exporto resultados?

1. Faça uma busca
2. Clique no ícone 📥 no topo
3. Arquivo CSV será salvo

### Formato do CSV

```
Loja, Produto, Preço (R$), Frete Grátis, Link
Mercado Livre, iPhone 15, 4999.00, Sim, https://...
```

---

## ⚙️ Configurações

### Como altero o tema?

Clique no ícone 🌓 no topo da janela.

### Como limpo o cache?

Clique no ícone 🧹 no topo da janela.

### Cache está desatualizado?

Cache expira em 1 hora. Ou limpe manualmente!

---

## 🐛 Problemas Comuns

### "Module not found"

```bash
pip install -r requirements.txt
```

### "Permission denied" (Linux/Mac)

```bash
chmod +x instalar.sh
chmod +x cacador_precos_v5.py
```

### App não abre

1. Verifique se Python está instalado
2. Reinstale dependências:
```bash
pip install --upgrade -r requirements.txt
```

### Resultados duplicados

Normal! Mesmos produtos aparecem em múltiplas lojas.

### App está lento

1. Limpe o cache
2. Reduza filtros
3. Use termos mais específicos

---

## 🔧 Personalização

### Posso mudar as cores?

Sim! Edite o código:
```python
page.theme_mode = ft.ThemeMode.DARK  # ou LIGHT
```

### Posso adicionar mais lojas?

Sim! Crie funções similares a `buscar_mercado_livre()` e integre outras APIs.

### Posso mudar o intervalo de alertas?

Sim! No código:
```python
CHECK_INTERVAL = 1800  # segundos (30 min)
```

---

## 💡 Dicas Avançadas

### Melhor horário para buscar?

**Madrugada** (2h-6h) - Menos concorrência na API

### Como encontrar os melhores preços?

1. Use filtro de frete grátis
2. Ordene por menor preço
3. Verifique o histórico de preços
4. Configure alertas

### Como monitorar Black Friday?

1. Adicione todos os produtos desejados aos favoritos
2. Configure alertas com preços-alvo
3. Deixe o app rodando
4. Seja notificado das promoções!

---

## 📞 Ainda tem dúvidas?

Consulte o **README.md** completo ou abra uma issue no GitHub!

**Boas compras! 🛒**
