
# Sistema de Precificação e Orçamentos - Consilium Business

Este é um sistema interativo desenvolvido em Streamlit para auxiliar na precificação de projetos e na geração de orçamentos e propostas para clientes.

## Funcionalidades

- **Calculadora de Orçamento**: Permite inserir dados como horas/dia, dias úteis, número de pessoas, valor da hora, custo operacional e adicionais para calcular diferentes cenários de preço (mínimo, médio, negociação).
- **Geração de Orçamento (PDF)**: Gera um documento PDF formatado para o cliente com os detalhes da proposta, resumo do projeto, investimento e condições de pagamento.
- **Geração de Documento Interno (CSV)**: Gera um arquivo CSV com todos os inputs e resultados detalhados dos cálculos para uso interno da equipe.
- **Log de Ações**: Registra cada orçamento gerado em um arquivo `orcamentos_log.csv` para histórico.

## Estrutura do Projeto

- `app.py`: O arquivo principal da aplicação Streamlit, contendo a interface do usuário e a orquestração das funcionalidades.
- `calculadora.py`: Módulo responsável pela lógica de cálculo do orçamento, validações e formatação de moeda.
- `documentos.py`: Módulo para a geração dos documentos em PDF (para cliente) e CSV (interno).
- `config.py`: Arquivo de configuração contendo todas as constantes e textos padrão, facilitando a personalização.
- `requirements.txt`: Lista de bibliotecas Python necessárias para rodar a aplicação.
- `orcamentos_log.csv`: Arquivo de log que será criado automaticamente ao gerar orçamentos.

## Como Usar (Localmente)

Siga os passos abaixo para configurar e rodar o sistema em sua máquina local:

### 1. Pré-requisitos

Certifique-se de ter o Python 3.8 ou superior instalado em seu sistema.

### 2. Clonar o Repositório (ou baixar o ZIP)

Se você recebeu um arquivo ZIP, descompacte-o em uma pasta de sua preferência. Se for um repositório Git, clone-o:

```bash
git clone <URL_DO_REPOSITORIO>
cd streamlit_orcamento
```

### 3. Criar e Ativar um Ambiente Virtual (Recomendado)

É uma boa prática usar um ambiente virtual para gerenciar as dependências do projeto:

```bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

### 4. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias usando o `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Rodar a Aplicação Streamlit

Após a instalação das dependências, você pode iniciar a aplicação:

```bash
streamlit run app.py
```

Isso abrirá o aplicativo no seu navegador padrão. Se não abrir automaticamente, copie e cole o URL fornecido no terminal (geralmente `http://localhost:8501`).

## Personalização

Todas as constantes configuráveis, como valores padrão, margens, textos de rodapé e mensagens, estão centralizadas no arquivo `config.py`. Edite este arquivo para adaptar o sistema às suas necessidades sem modificar a lógica principal da aplicação.

## Contato

Para dúvidas ou sugestões, entre em contato com a equipe da Consilium Business.
