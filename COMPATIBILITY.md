# Compatibilidade de Versões

## Versões do Flet

O app foi testado e funciona com:

### ✅ Versões Compatíveis
- **Flet 0.24.x - 0.80.x+** (Todas funcionam!)
- **Recomendado:** Use a versão mais recente

### ⚠️ Versões com Problemas
- **Flet < 0.24.x**: API de Tabs incompatível

## Erro Comum

### "Tab.__init__() got an unexpected keyword argument 'text'"

**Causa:** Versão antiga do Flet (< 0.24.0)

**Solução:**
```bash
pip install --upgrade flet
```

Ou especifique a versão:
```bash
pip install flet>=0.24.0
```

## Mudanças na API do Flet

### Flet 0.80.0+ (Versões Recentes)

**Mudanças:**
- `ft.app()` → `ft.run()` (app está deprecated)
- `ft.Icons.*` → `ft.icons.*` (minúsculo)
- Tabs mantém sintaxe: `ft.Tab(text="...", icon=...)`

**Código atualizado (v5.0.3+):**
```python
# ✅ Correto para Flet 0.80.0+
ft.run(target=main)
ft.Tab(text="Buscar", icon=ft.icons.SEARCH)
```

### Tabs (v0.23 → v0.24)

**Antes (0.23.x):**
```python
ft.Tab(text="Buscar", icon=ft.Icons.SEARCH)
```

**Agora (0.24.x+):**
```python
ft.Tab(
    tab_content=ft.Row([
        ft.Icon(ft.Icons.SEARCH),
        ft.Text("Buscar")
    ])
)
```

## Verificar Versão Instalada

```bash
pip show flet
```

**Saída esperada:**
```
Name: flet
Version: 0.24.0 ou superior
```

## Reinstalação Limpa

Se estiver com problemas:

```bash
# Desinstalar
pip uninstall flet

# Limpar cache
pip cache purge

# Reinstalar
pip install -r requirements.txt
```

## Outras Dependências

### HTTPX
- **Mínimo:** 0.27.0
- **Testado:** 0.27.2
- **Status:** ✅ Estável

### PyInstaller
- **Mínimo:** 6.0.0
- **Testado:** 6.10.0
- **Status:** ✅ Estável (opcional)

## Problemas Conhecidos

### Windows + Flet < 0.24
- Abas não aparecem corretamente
- Erro ao iniciar

**Solução:** Atualize o Flet

### Linux + Python < 3.8
- Algumas features do Flet não funcionam

**Solução:** Use Python 3.8+

### Mac M1/M2
- Algumas versões do Flet têm problemas com ARM

**Solução:** Use Flet 0.24.1+

## Suporte

Se encontrar problemas de compatibilidade:

1. Verifique versões: `pip list`
2. Atualize tudo: `pip install --upgrade -r requirements.txt`
3. Reporte no GitHub com:
   - Versão do Flet
   - Versão do Python
   - Sistema operacional
   - Mensagem de erro completa
