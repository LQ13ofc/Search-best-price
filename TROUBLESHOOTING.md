# Solucionando Problemas

## App não abre / Não acontece nada

### Verificar se Python está instalado

```bash
python --version
```

**Se der erro "python não encontrado":**

**Windows:**
1. Baixe Python em [python.org](https://www.python.org/downloads/)
2. Durante a instalação, **MARQUE** "Add Python to PATH"
3. Reinicie o computador
4. Tente novamente

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Mac:**
```bash
brew install python3
```

### Reinstalar dependências

```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

### Executar com debug

**Windows:**
```bash
python main.py
```

**Linux/Mac:**
```bash
python3 main.py
```

**Se aparecer erro**, copie a mensagem completa e:
1. Pesquise no Google
2. Ou abra uma issue no GitHub

### Erro comum: "ModuleNotFoundError: No module named 'flet'"

**Solução:**
```bash
pip install flet httpx
```

### Erro: "Permission denied"

**Linux/Mac:**
```bash
chmod +x run.sh
chmod +x install.sh
./run.sh
```

## Sem resultados na busca

### Problema: Nenhum produto aparece

**Causas possíveis:**
1. Termo muito específico (tente algo mais genérico)
2. Preço máximo muito baixo
3. Conexão com internet
4. API do Mercado Livre fora do ar (raro)

**Soluções:**
1. Tente buscar algo comum (ex: "notebook")
2. Remova o filtro de preço máximo
3. Verifique sua internet
4. Tente novamente em alguns minutos

### Problema: Só aparecem resultados do Mercado Livre

Isso é normal! O Google Shopping precisa de configuração:
1. Vá em "Configurações"
2. Crie conta em serpapi.com
3. Cole a API key
4. Clique em "Salvar"

## Alertas não funcionam

### Alerta não notifica

**Verifique:**
1. ✅ App está rodando? (precisa estar aberto)
2. ✅ Produto está nos favoritos?
3. ✅ Alerta está ativado? (switch verde)
4. ✅ Preço do alerta está correto?

**Como funciona:**
- O app verifica a cada 30 minutos
- Se o preço atual ≤ preço do alerta → notifica
- Precisa estar rodando (minimize na bandeja)

## Cache desatualizado

### Preços parecem velhos

**Solução:**
1. Vá em "Configurações"
2. Clique em "Limpar cache"
3. Faça a busca novamente

**Por que acontece:**
- Cache dura 1 hora
- Economiza requisições às APIs
- Se quiser preços atualizados, limpe o cache

## Exportação CSV não funciona

### Erro ao exportar

**Verifique:**
1. Você fez uma busca antes de exportar?
2. Tem permissão de escrita na pasta?

**Windows - Permissão negada:**
1. Execute como Administrador
2. Ou mude a pasta do projeto pra Documentos

## Configuração da API não salva

### API key não persiste

**Solução:**
1. Verifique permissões de escrita
2. Veja se `config.json` foi criado
3. Se não existir, crie manualmente:

```json
{
  "serpapi_key": "SUA_CHAVE_AQUI"
}
```

## Problemas de performance

### App está lento

**Soluções:**
1. Limpe o cache
2. Reduza os filtros
3. Feche outros programas
4. Reduza o limite de resultados no código

### Muita memória / CPU

**Normal se:**
- Tem muitos favoritos (50+)
- Muitos alertas ativos (20+)
- Histórico de preços grande

**Solução:**
- Limpe favoritos antigos
- Desative alertas desnecessários

## Ainda com problemas?

1. Leia o [USAGE.md](USAGE.md)
2. Veja as [issues no GitHub](https://github.com/seu-usuario/cacador-precos/issues)
3. Abra uma nova issue com:
   - Seu OS (Windows/Linux/Mac)
   - Versão do Python
   - Mensagem de erro completa
   - O que você estava fazendo
