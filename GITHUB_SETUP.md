# Como Publicar no GitHub

Siga estes passos para publicar o projeto:

## 1. Criar repositório

1. Vá em https://github.com/new
2. Nome: `cacador-precos`
3. Descrição: `Compare preços entre Mercado Livre e Google Shopping`
4. Público ou Privado (sua escolha)
5. **NÃO** marque "Initialize with README" (já temos um)
6. Clique em "Create repository"

## 2. Configurar Git localmente

```bash
# Inicialize o repositório (se ainda não fez)
git init

# Adicione todos os arquivos
git add .

# Primeiro commit
git commit -m "Versão inicial"

# Conecte ao GitHub (substitua seu-usuario)
git remote add origin https://github.com/seu-usuario/cacador-precos.git

# Crie a branch main
git branch -M main

# Faça o push
git push -u origin main
```

## 3. Configurar GitHub

### Habilitar Issues
1. Vá em Settings > Features
2. Marque "Issues"

### Habilitar GitHub Actions
Já está configurado! O workflow em `.github/workflows/tests.yml` vai rodar automaticamente.

### Adicionar Topics
1. Vá na página principal do repo
2. Clique em "Add topics"
3. Adicione: `python`, `price-comparison`, `mercado-libre`, `shopping`, `flet`

### Configurar About
1. Clique no ⚙️ ao lado de "About"
2. Description: `Compare preços entre Mercado Livre e Google Shopping`
3. Website: (opcional)
4. Topics: já adicionados
5. Marque "Releases" e "Packages"

## 4. Criar primeira Release

1. Vá em "Releases" > "Create a new release"
2. Tag: `v5.0.0`
3. Title: `v5.0.0 - Lançamento Inicial`
4. Descrição:
```
## Funcionalidades

- Busca em múltiplas lojas
- Sistema de favoritos
- Alertas de preço
- Histórico de preços
- Exportação para CSV
- Cache inteligente

## Instalação

```bash
pip install -r requirements.txt
python main.py
```

Veja o [README](README.md) para mais detalhes.
```
5. Clique em "Publish release"

## 5. Customizar perfil

Edite estes arquivos com suas informações:
- `setup.py` - Altere author, author_email, url
- `README.md` - Ajuste o link do GitHub no final
- `SECURITY.md` - Coloque seu email
- `CODE_OF_CONDUCT.md` - Coloque seu email

## 6. Dicas extras

### Adicionar badges no README

```markdown
![GitHub stars](https://img.shields.io/github/stars/seu-usuario/cacador-precos)
![GitHub forks](https://img.shields.io/github/forks/seu-usuario/cacador-precos)
![GitHub issues](https://img.shields.io/github/issues/seu-usuario/cacador-precos)
```

### Habilitar Discussions
Settings > Features > Discussions

### Adicionar GitHub Pages (opcional)
Settings > Pages > Source: main branch

### Proteger branch main
Settings > Branches > Add rule > main > Require pull request reviews

## Pronto!

Seu projeto está no ar! Compartilhe o link:
`https://github.com/seu-usuario/cacador-precos`
