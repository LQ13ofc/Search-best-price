# 🔥 CORREÇÃO URGENTE - v5.0.2

## ❌ Erro Corrigido

```
Tab.__init__() got an unexpected keyword argument 'text'
```

## ✅ Solução

Atualizado para compatibilidade com **Flet 0.24.x+**

## 🚀 Como Atualizar

### Se você já instalou v5.0.1:

```bash
pip install --upgrade flet
python main.py
```

### Instalação Nova:

```bash
# Windows
install.bat
run.bat

# Linux/Mac
./install.sh
./run.sh
```

## 📋 O Que Mudou

### Código (main.py)
```python
# ANTES (não funciona em Flet 0.24+)
ft.Tab(text="Buscar", icon=ft.Icons.SEARCH)

# AGORA (funciona em todas as versões)
ft.Tab(
    tab_content=ft.Row([
        ft.Icon(ft.Icons.SEARCH),
        ft.Text("Buscar")
    ])
)
```

### Dependências (requirements.txt)
```python
# ANTES
flet>=0.23.0

# AGORA
flet>=0.24.0
```

## 📝 Novos Arquivos

- **COMPATIBILITY.md** - Guia completo de compatibilidade de versões
- Atualizado **TROUBLESHOOTING.md** com esse erro específico

## ✨ Funcionalidades

Tudo da v5.0.1 + correção de compatibilidade:
- ✅ Navegação entre abas funciona
- ✅ Preços do Google Shopping corretos
- ✅ pip install funciona
- ✅ Backup automático de dados
- ✅ Threading seguro
- ✅ **NOVO:** Compatível com Flet 0.24.x+

## 🆘 Ainda com Problemas?

1. **Atualize o Flet:**
   ```bash
   pip install --upgrade flet
   ```

2. **Verifique a versão:**
   ```bash
   pip show flet
   ```
   Deve mostrar 0.24.0 ou superior

3. **Reinstale tudo:**
   ```bash
   pip uninstall flet
   pip install -r requirements.txt
   ```

4. **Consulte:** [COMPATIBILITY.md](COMPATIBILITY.md) e [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Versão:** 5.0.2  
**Data:** 11/02/2024  
**Tipo:** Hotfix (correção urgente)  
**Status:** ✅ Testado e funcionando
