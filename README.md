git add . 
git commit -m "qualuqer frase"--no-verify
git push

# 📊 Sistema de Precificação Consilius Business (v3.4)

Este é o sistema institucional permanente de precificação e geração de orçamentos da **Consilius Business**. A versão 3.4 introduz o suporte a **Templates PDF Profissionais** para propostas comerciais e melhorias de interface.

---

## 🚀 Como Instalar e Executar

### 1. Instalar o Python
Se você ainda não tem o Python instalado:
1. Acesse [python.org](https://www.python.org/downloads/).
2. Baixe a versão mais recente.
3. **IMPORTANTE:** Durante a instalação, marque a caixa **"Add Python to PATH"**.

### 2. Instalar as Bibliotecas Necessárias
Abra o terminal (ou CMD) e execute:
```bash
pip install streamlit reportlab pandas PyPDF2
```

### 3. Executar o Sistema
Abra a pasta do projeto no terminal do VS Code e use o comando abaixo:

```bash
python -m streamlit run app.py
```

---

## 📂 Estrutura do Projeto

- **`app.py`**: Interface do usuário (Streamlit).
- **`pricing.py`**: Lógica matemática institucional.
- **`services.py`**: Banco de dados de serviços e multiplicadores.
- **`pdf_generator.py`**: Motor de geração de PDFs (Template + Sobreposição).
- **`pdf_layout_config.py`**: Configuração de coordenadas (x, y) para o template.
- **`assets/logo.png`**: Logo oficial da Consilius.
- **`templates/template_orcamento.pdf`**: Template de 4 páginas para o orçamento.

---

## 🛠️ Novidades da Versão 3.4

- **Interface Refinada:** Logo pequena no canto superior esquerdo como complemento visual, preservando o título principal.
- **Layout de PDF Corrigido:** Espaçamento aumentado na primeira página para evitar sobreposição ao design superior.
- **Nova Estrutura de Páginas:**
  - **Página 1:** Proposta Comercial, Escopo e Resumo.
  - **Página 2:** Contextualização (Sobre Consilius e IBMEC).
  - **Página 3:** Proposta e Execução, Equipe, Modalidade, Etapas e Pagamento.
- **Rodapé Final:** Footer fixo removido de todas as páginas; agora aparece apenas no final do conteúdo do PDF, de forma discreta.
- **Placeholders Editáveis:** Campos destacados em vermelho para fácil identificação e edição manual pós-geração.

---

## 🛠️ Como Modificar o Sistema

### Ajustar Posições no PDF
Se você alterar o design do `template_orcamento.pdf` e os textos ficarem desalinhados, abra o arquivo `pdf_layout_config.py` e ajuste as coordenadas `(x, y)` de cada campo.

### Alterar a Logo
Substitua o arquivo em `assets/logo.png`. O sistema atualizará automaticamente na interface e no documento interno.

### Alterar o Template
Substitua o arquivo em `templates/template_orcamento.pdf`. Certifique-se de que o novo arquivo tenha o mesmo número de páginas ou ajuste a lógica em `pdf_generator.py`.

---
**Consilius Business 2026**  
*Sistema de Precificação Oficial*
