# Changelog

## [5.0.3] - 2024-02-11

### 🔧 Correção de Compatibilidade - Flet 0.80.0+

- **API atualizada**: Migrado de `ft.app()` para `ft.run()`
- **Ícones**: Corrigido `ft.Icons` para `ft.icons` (minúsculo)
- **Tabs**: Sintaxe correta para Flet versões mais recentes
- **Compatibilidade**: Testado com Flet 0.24.x até 0.80.x+

### ⚡ Melhorias

- Removido PyInstaller dos requirements (opcional)
- Código otimizado para versões mais recentes do Flet

---

## [5.0.2] - 2024-02-11

### 🐛 Correção de Compatibilidade

- **Flet API**: Corrigido erro `Tab.__init__() got an unexpected keyword argument 'text'`
- **Tabs**: Atualizado para sintaxe do Flet 0.24.x+ usando `tab_content`
- **Requirements**: Atualizado mínimo do Flet para 0.24.0

### 📝 Documentação

- Adicionado `COMPATIBILITY.md` com guia de versões compatíveis
- Instruções de troubleshooting para problemas de versão

---

## [5.0.1] - 2024-02-11

### 🐛 Correções Críticas

- **Navegação entre abas**: Corrigido bug que impedia dados de carregar ao trocar de aba
- **Parsing de preços**: Corrigido cálculo incorreto de preços do Google Shopping (valores exagerados)
- **Entry point**: Corrigido comando `cacador-precos` para funcionar após instalação via pip
- **Perda de dados**: Implementado sistema de backup automático para arquivos corrompidos
- **Threading**: Corrigido problema de concorrência ao atualizar UI de threads secundárias

### 📝 Melhorias

- Mensagens de erro mais descritivas no console
- Backup automático de arquivos JSON corrompidos
- Tratamento robusto de exceções

Veja [BUGFIXES.md](BUGFIXES.md) para detalhes técnicos.

---

## [5.0.0] - 2024-02-10

### ✨ Lançamento Inicial

#### Funcionalidades Principais

- Busca simultânea em Mercado Livre e Google Shopping
- Sistema de favoritos com persistência
- Alertas de preço com verificação automática
- Histórico de preços para análise
- Gráficos de tendência
- Exportação para CSV
- Cache inteligente (1 hora)

#### Interface

- 6 abas organizadas (Buscar, Histórico, Favoritos, Gráficos, Alertas, Configurações)
- Tema claro/escuro
- Filtros avançados (preço, frete grátis, loja)
- Badges visuais (menor preço, frete grátis)

#### Configuração

- Tela de configurações integrada
- Teste de API key dentro do app
- Sem necessidade de variáveis de ambiente

---

## Roadmap

### [5.1.0] - Planejado

- [ ] Notificações por email
- [ ] Mais gráficos de análise
- [ ] Suporte a mais marketplaces
- [ ] Testes automatizados

### [6.0.0] - Futuro

- [ ] App mobile (Android/iOS)
- [ ] Sincronização na nuvem
- [ ] Compartilhar listas
- [ ] Sistema de cupons

---

**Legenda:**
- 🐛 Correção de bug
- ✨ Nova funcionalidade
- 📝 Documentação
- 🔒 Segurança
- ⚡ Performance
