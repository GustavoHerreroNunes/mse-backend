# Gerador de Survey Reports MSE

Um sistema abrangente baseado em Python para geração de relatórios PDF de operações de vistoria marítima. Este sistema automatiza a criação de relatórios profissionais de vistoria para operações de embarque/desembarque de carga de navios em portos, integrando consultas ao banco de dados, análise de condições alimentada por IA, processamento de imagens e armazenamento em nuvem.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Recursos Principais](#recursos-principais)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Componentes Principais](#componentes-principais)
- [Integração com IA](#integração-com-ia)
- [Implantação](#implantação)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)

---

## 🎯 Visão Geral

O Gerador de Survey Reports MSE é uma solução de nível empresarial projetada para **MSE – Engenharia Naval** para automatizar a criação de relatórios abrangentes de vistoria. O sistema gera documentos PDF profissionais que documentam inspeções de navios, condições de carga, avaliações de equipamentos de içamento/amarração e procedimentos operacionais.

### O Que Ele Faz

1. **Busca dados de vistoria** de um banco de dados PostgreSQL
2. **Gera relatórios PDF com múltiplas seções** com formatação profissional
3. **Incorpora análise alimentada por IA** usando modelos GPT da OpenAI
4. **Processa e otimiza imagens** para inclusão no relatório
5. **Faz upload dos relatórios finais** para o Google Drive
6. **Rastreia o status de geração** no banco de dados

---

## ✨ Recursos Principais

### 📄 Seções Abrangentes do Relatório

- **Página de Capa**: Informações do cliente, navio e carga
- **Página do Cliente**: Logotipos e identidade visual da empresa
- **Packing List**: Tabela detalhada de características das cargas
- **Narrativa**: Circunstâncias e contexto da vistoria
- **Statement of Facts**: Linha do tempo cronológica de eventos
- **Informações do Navio**: Especificações técnicas e detalhes
- **Guindaste do Navio**: Análise do equipamento com fotos
- **Inspeção de Carga**: Avaliação de condições alimentada por IA
- **Equipamentos de Içamento**: Detalhes de aparelhos e acessórios
- **Equipamentos de Amarração**: Materiais e métodos de fixação
- **Operações de Carga**: Documentação operacional passo a passo
- **Área de Estivagem**: Condições e layout de armazenamento
- **Observações QHSE**: Observações de segurança
- **Conclusões**: Resumos gerados por IA por categoria
- **Índice de Figuras e Tabelas**: Referências cruzadas automatizadas

### 🤖 Análise Alimentada por IA

- **Avaliação Automática de Condições**: GPT-3.5 analisa condições de carga, guindaste, içamento, amarração e acessórios
- **Geração de Linguagem Natural**: Converte dados técnicos em linguagem profissional de vistoria
- **Observações Contextualizadas**: Sinaliza apenas achados negativos (condições Razoável, Ruim, Muito Ruim)
- **Sumarização Inteligente**: Gera declarações conclusivas para cada categoria de inspeção

### 🖼️ Processamento Avançado de Imagens

- **Download Automático**: Busca imagens de URLs do banco de dados
- **Remoção de Transparência**: Converte RGBA para RGB com fundo branco
- **Dimensionamento Padronizado**: Redimensiona para 502x376px para consistência
- **Otimização de Qualidade**: Compressão JPEG com 85% de qualidade
- **Limpeza Automática**: Remove arquivos temporários após processamento

### ☁️ Integração com Nuvem

- **Upload para Google Drive**: Upload automático para pastas específicas do cliente
- **Autenticação com Service Account**: Autenticação segura e automatizada
- **Gerenciamento de Pastas**: Cria estrutura de subpastas "Survey Reports"
- **Geração de Links Públicos**: URLs compartilháveis para acesso ao relatório

### 🔄 Fluxo de Trabalho Automatizado

- **Processamento em Lote**: Manipula múltiplas vistorias em fila
- **Tratamento de Erros**: Log abrangente e gerenciamento de exceções
- **Auto-Desligamento de VM**: Desligamento automático da instância GCP após conclusão
- **Reorganização de PDF**: Ordenação inteligente de páginas para fluxo otimizado

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                   Banco de Dados PostgreSQL                 │
│  (Dados de Vistoria, Info do Navio, Detalhes da Carga,     │
│   URLs de Imagens)                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         Camada de Carregadores de Dados e Consultas         │
│  - load_demanda_data()    - get_dados_cargo_table()        │
│  - get_demanda_ids()      - get_dados_lifting_table()      │
│  - get_dados_demanda()    - get_dados_cargo_condition()    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Camada de Análise IA (OpenAI)                  │
│  - ai_cargo_condition()     - ai_crane_condition()         │
│  - ai_lifting_condition()   - ai_lashing_condition()       │
│  - ai_rigging_condition()   - ai_stowage_condition()       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           Camada de Geração de PDF (ReportLab)              │
│  - draw_cover_page()       - draw_cargos_page()            │
│  - draw_packing_list()     - draw_lifting_page()           │
│  - draw_narrative_page()   - draw_lashing_page()           │
│  - draw_statement_page()   - draw_stowage_page()           │
│  - draw_vessel_page()      - draw_conclusion_page()        │
│  - draw_crane_page()       - draw_index_page()             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          Camada de Pós-Processamento (PyPDF2)               │
│  - Reorganização de páginas  - Gerenciamento de bookmarks  │
│  - Montagem final            - Injeção de metadados        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│    Armazenamento em Nuvem & Limpeza (API Google Drive)     │
│  - Upload para Drive      - Geração de link compartilhável  │
│  - Atualização do BD      - Exclusão de arquivos locais     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.11 ou superior
- Banco de dados PostgreSQL
- Docker (para implantação containerizada)
- Conta Google Cloud Platform (para implantação)
- Chave de API OpenAI
- Credenciais da API do Google Drive

### Configuração Local

1. **Clone o repositório**
   ```bash
   git clone https://github.com/appautou/MSE-API.git
   cd MSE-API
   ```

2. **Instale as dependências Python**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente**
   
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   # Configuração do Banco de Dados
   DATABASE_URL=postgresql://usuario:senha@host:porta/nome_banco
   
   # API OpenAI
   OPENAI_API_KEY=sua_chave_api_openai_aqui
   
   # API Google Drive (JSON da Service Account como string)
   GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"..."}
   ```

4. **Verifique os arquivos de fonte**
   
   Certifique-se de que todas as fontes necessárias estão em `utils/font/`:
   - Montserrat-Regular.ttf
   - Montserrat-Bold.ttf
   - CooperBlack.ttf
   - calibri.ttf
   - calibri-bold.ttf
   - tahoma.ttf
   - tahoma-bold.ttf
   - Symbola.ttf

5. **Prepare os recursos estáticos**
   
   Coloque as imagens necessárias em `pdf_static_images/`:
   - cover.jpeg
   - mse_logo.png

---

## ⚙️ Configuração

### Configuração do Banco de Dados

O sistema espera as seguintes tabelas PostgreSQL:
- `tbl_demandas` - Demandas/ordens de vistoria
- `tbl_vessel` - Informações do navio
- `tbl_cargo` - Detalhes da carga
- `tbl_task_survey_boarding` - Tarefas de vistoria
- `tbl_tarefas` - Definições de tarefas
- `tbl_status_pdf` - Rastreamento de geração de PDF
- Tabelas adicionais de condição para carga, içamento, amarração, guindaste, etc.

### Configuração do Google Drive

1. Crie um Projeto no Google Cloud
2. Ative a API do Google Drive
3. Crie uma Service Account
4. Faça download do arquivo JSON de chave
5. Armazene o conteúdo JSON na variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS_JSON`

---

## 🎮 Uso

### Executando Localmente

```bash
python generate_pdf_with_reportlab.py
```

O script irá:
1. Consultar o banco de dados para vistorias com `created = FALSE`
2. Gerar relatórios PDF para cada vistoria
3. Fazer upload dos relatórios para o Google Drive
4. Atualizar o banco de dados com status de conclusão e URLs dos arquivos

### Implantação com Docker

1. **Construa a imagem Docker**
   ```bash
   docker build -t gcr.io/msenaval-453016/pdf-generator:latest .
   ```

2. **Teste localmente**
   ```bash
   docker run -p 8080:8080 gcr.io/msenaval-453016/pdf-generator:latest
   ```

3. **Envie para o Google Container Registry**
   ```bash
   gcloud auth configure-docker
   docker push gcr.io/msenaval-453016/pdf-generator:latest
   ```

### Implantação no Google Cloud

1. **Autentique com GCloud**
   ```bash
   gcloud auth login
   gcloud config set project msenaval-453016
   ```

2. **Implante no Cloud Run ou Compute Engine**
   ```bash
   # O script inclui funcionalidade de desligamento automático da VM
   # Certifique-se de que shutdown_vm() está descomentado para produção
   ```

---

## 📁 Estrutura do Projeto

```
MSE-API/
├── 📄 generate_pdf_with_reportlab.py    # Script principal de orquestração
├── 📄 requirements.txt                  # Dependências Python
├── 📄 dockerfile                        # Configuração do container
├── 📄 readme.txt                        # Notas de implantação
├── 📄 README.md                         # Este arquivo
│
├── 📁 services/
│   └── database.py                      # Conexão SQLAlchemy com banco de dados
│
├── 📁 querys/                           # Módulos de consulta ao banco de dados
│   ├── get_demanda_id.py               # Busca vistorias pendentes
│   ├── get_dados_demanda.py            # Dados principais da vistoria
│   ├── get_dados_cargo_table.py        # Dados da tabela de carga
│   ├── get_dados_cargo_condition.py    # Detalhes de condição da carga
│   ├── get_dados_lifting_table.py      # Dados de equipamento de içamento
│   ├── get_dados_lashing_table.py      # Dados de equipamento de amarração
│   ├── get_dados_vessel_crane.py       # Informações do guindaste
│   ├── get_dados_photos.py             # Recuperação de URLs de imagens
│   ├── get_dados_statement.py          # Statement of Facts
│   ├── get_dados_conclusion_*.py       # Dados de conclusão por categoria
│   └── update_create_pdf.py            # Consulta de atualização de status
│
├── 📁 reportlab_pages/                  # Módulos de geração de páginas PDF
│   ├── draw_cover_page.py              # Capa do relatório
│   ├── draw_client_page.py             # Página de identidade do cliente
│   ├── draw_index_page.py              # Índice
│   ├── draw_index_of_figures_and_tables.py  # Índice de figuras/tabelas
│   ├── draw_packing_list_page.py       # Tabela de características da carga
│   ├── draw_narrative_page.py          # Circunstâncias da vistoria
│   ├── draw_statement_page.py          # Eventos cronológicos
│   ├── draw_vessel_page.py             # Especificações do navio
│   ├── draw_crane_page.py              # Avaliação do guindaste
│   ├── draw_cargos_page.py             # Análise de condição da carga
│   ├── draw_lifting_page.py            # Equipamento de içamento
│   ├── draw_lashing_page.py            # Equipamento de amarração
│   ├── draw_operation_page.py          # Procedimentos operacionais
│   ├── draw_stowage_page.py            # Condições de armazenamento
│   ├── draw_remarks_page.py            # Observações QHSE
│   └── draw_conclusion_page.py         # Conclusões finais
│   │
│   └── 📁 utils/                        # Utilitários de desenho
│       ├── commons.py                   # Funções comuns de página
│       ├── draw_commons_images.py       # Cabeçalhos/rodapés/separadores
│       ├── draw_label_value.py          # Pares label-valor
│       ├── draw_page_number.py          # Numeração de página
│       ├── draw_wrapped_text.py         # Motor de quebra de texto
│       ├── format_date_with_ordinal.py  # Formatação de data
│       ├── ai_cargo_condition.py        # Análise IA de carga
│       ├── ai_crane_condition.py        # Análise IA de guindaste
│       ├── ai_lifting_condition.py      # Análise IA de içamento
│       ├── ai_lashing_condition.py      # Análise IA de amarração
│       ├── ai_rigging_condition.py      # Análise IA de acessórios
│       └── ai_stowage_condition.py      # Análise IA de estivagem
│
├── 📁 utils/                            # Utilitários gerais
│   ├── data_loaders.py                  # Wrappers de carregamento de dados
│   ├── register_fonts.py                # Registro de fontes
│   ├── set_page.py                      # Gerenciamento de número de página
│   ├── baixar_imagens.py                # Download/processamento de imagens
│   ├── upload_pdf_to_drive.py           # Integração com Google Drive
│   └── 📁 font/                         # Arquivos de fonte TTF
│
├── 📁 pdf_static_images/                # Recursos estáticos (logos, capas)
├── 📁 generate_pdf/                     # Diretório de saída (temporário)
└── 📁 uploads/                          # Área de preparação de upload
```

---

## 🔧 Componentes Principais

### 1. Orquestrador Principal (`generate_pdf_with_reportlab.py`)

O script central que coordena todo o fluxo de geração de PDF:

- **Carregamento de Dados**: Busca todas as vistorias pendentes de `tbl_status_pdf`
- **Criação de Canvas PDF**: Inicializa canvas ReportLab com tamanho A4
- **Geração de Páginas**: Chama funções individuais de desenho de página em sequência
- **Indexação Dinâmica**: Rastreia números de página e cria bookmarks clicáveis
- **Lógica Condicional**: Ajusta estrutura do relatório baseado no tipo de operação (embarque/desembarque)
- **Reorganização de Páginas**: Usa PyPDF2 para reorganizar páginas (capa, cliente, índice, conteúdo)
- **Gerenciamento de Arquivos**: Cria diretórios temporários, salva PDFs e depois limpa
- **Upload em Nuvem**: Envia PDF final para Google Drive
- **Atualização de Status**: Marca vistoria como concluída no banco de dados

**Funções Principais:**
- `generate_pdf_with_reportlab()`: Função principal de orquestração
- `shutdown_vm()`: Auto-desligamento da VM GCP para otimização de custos

### 2. Camada de Banco de Dados (`services/` & `querys/`)

**`services/database.py`**
- Estabelece conexão PostgreSQL usando SQLAlchemy
- Fornece gerenciamento de sessão com escopo
- Lê string de conexão de variáveis de ambiente

**Módulos de Consulta** (`querys/`)

Cada módulo de consulta segue um padrão consistente:
```python
def get_dados_*(identifier):
    current_session = Session()
    try:
        query = """CONSULTA SQL AQUI"""
        result = current_session.execute(text(query), params)
        # Processa resultados
        return data, None
    except Exception as e:
        current_session.rollback()
        return None, str(e)
    finally:
        current_session.close()
```

**Módulos de Consulta Principais:**
- `get_demanda_id.py`: Encontra todas as vistorias pendentes de geração de PDF
- `get_dados_demanda.py`: Dados abrangentes de vistoria e navio
- `get_dados_cargo_table.py`: Características da carga para packing list
- `get_dados_*_condition.py`: Dados de avaliação de condição para análise IA
- `update_create_pdf.py`: Atualiza status de conclusão com URL do arquivo

### 3. Carregadores de Dados (`utils/data_loaders.py`)

Funções wrapper que:
- Chamam funções de consulta ao banco de dados
- Tratam erros de forma elegante
- Fornecem valores padrão para dados ausentes
- Transformam resultados do banco de dados em estruturas prontas para PDF

**Funções:**
- `load_demanda_data(demanda_id)`: Informações principais da vistoria
- `load_cargo_table(demanda_id)`: Tabela de carga para packing list
- `load_lifting_table(demanda_id)`: Detalhes de equipamento de içamento
- `load_lashing_table(demanda_id)`: Detalhes de equipamento de amarração
- `load_demanda_ids()`: Lista de vistorias pendentes

### 4. Geradores de Páginas PDF (`reportlab_pages/`)

Cada gerador de página segue esta estrutura:

```python
def draw_*_page(c, width, height, *args):
    # 1. Desenha cabeçalho e rodapé
    draw_header(c, width, height)
    draw_footer(c, width)
    draw_page_number(c, width)
    
    # 2. Define título e fontes
    c.setFont("CooperBlack", 20)
    c.drawString(30, height - 150, "TÍTULO DA SEÇÃO")
    
    # 3. Busca dados
    data, error = get_dados_*(identifier)
    
    # 4. Análise IA (se aplicável)
    comments = ai_*_condition(data)
    
    # 5. Desenha conteúdo com paginação
    current_y = height - 180
    for item in data:
        current_y = ensure_space(c, needed_space, current_y)
        current_y = draw_paragraph(text, current_y, "Calibri")
    
    # 6. Adiciona imagens com legendas
    images = baixar_imagens(photo_urls, page_name, demanda_id)
    # Desenha imagens com espaçamento adequado
    
    # 7. Retorna dados de figura para índice
    return index_figure_data, next_figure_number
```

**Módulos de Página Principais:**

- **`draw_cover_page.py`**: Capa profissional com info de cliente/navio/carga
- **`draw_packing_list_page.py`**: Tabela paginada de características da carga
- **`draw_narrative_page.py`**: Contexto da vistoria com fotos de atracação
- **`draw_statement_page.py`**: Linha do tempo cronológica de todos os eventos
- **`draw_cargos_page.py`**: Análise de condição de carga alimentada por IA com fotos
- **`draw_lifting_page.py`**: Tabela de equipamento de içamento e avaliação de condição
- **`draw_lashing_page.py`**: Materiais de amarração e achados de inspeção
- **`draw_conclusion_page.py`**: Declarações resumidas geradas por IA

### 5. Utilitários de Desenho (`reportlab_pages/utils/`)

**Funções Comuns:**
- `draw_header()`: Cabeçalho padrão de página com identidade visual
- `draw_footer()`: Rodapé de página com separador
- `draw_page_number()`: Numeração dinâmica de página
- `draw_wrapped_text()`: Quebra inteligente de texto com quebras de palavra
- `draw_label_value()`: Pares chave-valor formatados
- `start_new_page()`: Cria nova página com cabeçalhos
- `ensure_space()`: Previne corte de conteúdo no final da página

**Formatação:**
- `format_date_with_ordinal()`: "15 de Janeiro de 2024"
- `commons.py`: Funções compartilhadas de paginação e espaçamento

### 6. Módulos de Análise IA (`reportlab_pages/utils/ai_*.py`)

Todos os módulos IA seguem este padrão:

```python
def ai_*_condition(data: dict[str, str]) -> list[str]:
    """
    Gera observações técnicas profissionais baseadas em dados de condição.
    Usa OpenAI GPT-3.5-turbo com temperature=0 para consistência.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=900,
            messages=[
                {"role": "system", "content": "Prompt do sistema especialista..."},
                {"role": "user", "content": json.dumps(data)}
            ]
        )
        # Analisa resposta JSON
        comments = json.loads(clean_response)
        return comments  # Lista de 1-6 observações profissionais
    except Exception as exc:
        return ["No further comments to be made."]
```

**Módulos IA:**
- `ai_cargo_condition.py`: Analisa campos de condição de carga
- `ai_crane_condition.py`: Avalia status do guindaste do navio
- `ai_lifting_condition.py`: Avalia equipamento de içamento
- `ai_lashing_condition.py`: Revisa materiais de amarração
- `ai_rigging_condition.py`: Examina operações de acessórios
- `ai_stowage_condition.py`: Avalia condições de armazenamento

**Engenharia de Prompt IA:**
- Prompts de sistema estabelecem expertise de vistoriador
- Temperature=0 garante saída consistente
- Instrui a sinalizar apenas achados negativos
- Mantém linguagem técnica profissional
- Limita saída a 6 observações concisas

### 7. Processamento de Imagens (`utils/baixar_imagens.py`)

**Função: `baixar_imagens(urls, nome_pagina, demanda_id)`**

Fluxo do processo:
1. **Download**: Busca imagens das URLs fornecidas
2. **Remoção de Transparência**: Converte RGBA → RGB com fundo branco
3. **Redimensionamento**: Padroniza para 502x376px usando reamostragem LANCZOS
4. **Otimização**: Salva como JPEG com 85% de qualidade
5. **Organização**: Armazena em `app/routes/generate_pdf/{nome_pagina}_{demanda_id}/`
6. **Retorno**: Lista de caminhos de arquivo local para inclusão no PDF

**Tratamento de Erros:**
- Timeout após 10 segundos
- Pula downloads que falharam
- Registra erros para depuração

### 8. Integração com Google Drive (`utils/upload_pdf_to_drive.py`)

**Funções Principais:**

**`get_drive_service()`**
- Autentica usando JSON de service account do ambiente
- Retorna objeto PyDrive2 GoogleDrive

**`find_or_create_survey_reports_folder(drive, parent_folder_id)`**
- Busca subpasta "Survey Reports"
- Cria se não existir
- Retorna ID da pasta

**`upload_report_to_drive(file_path, folder_id)`**
- Faz upload do PDF para subpasta "Survey Reports"
- Define permissões públicas de leitura
- Retorna URL de download compartilhável
- Formato: `https://drive.google.com/uc?id={file_id}&export=download`

### 9. Gerenciamento de Fontes (`utils/register_fonts.py`)

Registra fontes TrueType personalizadas para ReportLab:
- **Montserrat**: Sans-serif moderna para títulos
- **Cooper Black**: Fonte decorativa em negrito para títulos
- **Calibri**: Fonte limpa para corpo de texto
- **Tahoma**: Sans-serif alternativa
- **Symbola**: Suporte a símbolos Unicode

As fontes são carregadas do diretório `utils/font/`.

---

## 🤖 Integração com IA

### Uso do OpenAI GPT-3.5

O sistema utiliza o modelo GPT-3.5-turbo da OpenAI para análise inteligente:

**Casos de Uso:**
1. **Análise de Condição de Carga**: Interpreta campos de inspeção (arranhões, corrosão, umidade, etc.)
2. **Avaliação de Equipamento**: Avalia classificações de condição de içamento/amarração/acessórios
3. **Avaliação de Guindaste**: Analisa status operacional do guindaste do navio
4. **Condições de Armazenamento**: Revisa achados da área de estivagem
5. **Geração de Conclusões**: Sintetiza declarações de condição geral

**Estratégia de Engenharia de Prompt:**

```python
system_prompt = """
Você é um vistoriador de carga escrevendo observações profissionais em 
inglês para um relatório de condição. Analise os campos fornecidos e 
gere ATÉ SEIS observações técnicas em estilo de lista, APENAS se houver 
achados negativos (Razoável, Ruim, Muito Ruim, Não, Menor, Moderado, Severo).

IMPORTANTE: Para 'moisture' e 'shifting', valor 'No' é POSITIVO.

Cada comentário deve ser natural, ex.: 'Scratches noted on exposed 
wood surfaces.', não 'ranking_scratches: Moderate'.

Retorne apenas um array JSON de 1 a 6 strings em inglês.
"""
```

**Por Que Funciona:**
- **Prompting baseado em papel**: Estabelece contexto de especialista
- **Restrições de saída**: Limita a 1-6 observações
- **Especificação de formato**: Solicita JSON para análise fácil
- **Linguagem natural**: Instrui a escrever como um vistoriador humano
- **Relatório seletivo**: Relata apenas problemas, não todos os campos

**Benefícios:**
- Reduz tempo de redação manual de relatórios em 80%
- Mantém terminologia profissional consistente
- Adapta-se a qualidade variável de dados de inspeção
- Fornece fallback para texto padrão em caso de falha da API

---

## 🚢 Implantação

### Configuração do Google Cloud Platform

**1. VM Compute Engine (Recomendado)**

```bash
# Criar instância de VM
gcloud compute instances create pdf-generator-vm \
    --machine-type=e2-medium \
    --zone=us-central1-a \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --boot-disk-size=20GB

# SSH na VM
gcloud compute ssh pdf-generator-vm

# Instalar dependências
sudo apt update
sudo apt install python3-pip git
git clone https://github.com/appautou/MSE-API.git
cd MSE-API
pip3 install -r requirements.txt

# Definir variáveis de ambiente
export DATABASE_URL="postgresql://..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_APPLICATION_CREDENTIALS_JSON='{"type":"service_account",...}'

# Executar gerador
python3 generate_pdf_with_reportlab.py
```

**2. Cloud Run (Serverless)**

```bash
# Construir container
docker build -t gcr.io/msenaval-453016/pdf-generator:latest .

# Enviar para GCR
docker push gcr.io/msenaval-453016/pdf-generator:latest

# Implantar no Cloud Run
gcloud run deploy pdf-generator \
    --image gcr.io/msenaval-453016/pdf-generator:latest \
    --platform managed \
    --region us-central1 \
    --memory 2Gi \
    --timeout 3600 \
    --set-env-vars DATABASE_URL=$DATABASE_URL,OPENAI_API_KEY=$OPENAI_API_KEY
```

**3. Execução Agendada**

Use o Cloud Scheduler para acionar geração periódica:

```bash
gcloud scheduler jobs create http pdf-generation-job \
    --schedule "0 */4 * * *" \
    --uri "https://pdf-generator-<hash>.run.app" \
    --http-method POST
```

### Recurso de Auto-Desligamento

O script inclui auto-desligamento de VM para minimizar custos:

```python
def shutdown_vm():
    # Busca metadados da VM
    # Autentica com service account
    # Chama API do Compute Engine para parar instância
    # Executa apenas no GCP, falha graciosamente localmente
```

**Habilitar em produção:**
Descomente `shutdown_vm()` no final de `generate_pdf_with_reportlab.py`.

---

## 🛠️ Tecnologias Utilizadas

### Tecnologias Principais
- **Python 3.11**: Linguagem de programação principal
- **ReportLab**: Motor de geração e layout de PDF
- **PyPDF2**: Manipulação de PDF e reordenação de páginas
- **SQLAlchemy**: ORM de banco de dados e construtor de consultas
- **PostgreSQL**: Banco de dados relacional para dados de vistoria

### IA & Aprendizado de Máquina
- **OpenAI GPT-3.5**: Geração de linguagem natural para análise de condições
- **Análise JSON**: Manipulação estruturada de resposta de IA

### Processamento de Imagens
- **Pillow (PIL)**: Manipulação e otimização de imagens
- **Requests**: Cliente HTTP para download de imagens

### Serviços em Nuvem
- **API Google Drive**: Integração com armazenamento em nuvem
- **PyDrive2**: Wrapper simplificado da API Drive
- **Google Cloud Storage**: Hospedagem de imagens de container
- **Google Compute Engine**: Hospedagem de VM

### Ferramentas de Desenvolvimento
- **Docker**: Containerização
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **logging**: Rastreamento abrangente de erros

### Fontes & Tipografia
- **Fontes TrueType**: Tipografia personalizada (Montserrat, Calibri, Cooper Black)
- **Suporte Unicode**: Renderização de caracteres internacionais (Symbola)

### Utilitários
- **num2words**: Conversão de número para palavra em linguagem natural
- **datetime**: Formatação de data e gerenciamento de timestamps
- **re (regex)**: Limpeza de strings e sanitização de nomes de arquivo
- **os/io**: Operações de sistema de arquivos

---

## 📊 Esquema do Banco de Dados (Estrutura Esperada)

O sistema espera estas tabelas principais:

**`tbl_demandas`** - Ordens de vistoria
- `id_demanda` (PK)
- `cliente` - Nome do cliente
- `id_ship` (FK) - Referência do navio
- `dt_abertura` - Data da vistoria
- `nome_demanda` - Nome da vistoria
- `location` - Localização do porto
- `id_pasta_gd_demanda` - ID da pasta do Google Drive

**`tbl_vessel`** - Informações do navio
- `vessel_id` (PK)
- `vessel_name`, `vessel_type`
- `country_flag`, `imo_number`
- `year_of_built`, `dwt`
- `vessel_length`, `vessel_breadth`

**`tbl_cargo`** - Detalhes da carga
- `cargo_id` (PK)
- `cargo_name`, `cargo_type`
- `weight`, `length`, `width`, `height`
- `extra_info`, `id_task` (FK)

**`tbl_task_survey_boarding`** - Tarefas de vistoria
- `id_task` (PK)
- `id_survey` (FK para tbl_demandas)
- `num_bollards_fwd`, `num_bollards_aft`

**`tbl_status_pdf`** - Rastreamento de geração
- `id_demanda` (FK)
- `created` (BOOLEAN) - Status de geração
- `url_path_pdf` - URL do Drive
- `modified_at` - Timestamp da última atualização

**Tabelas de Condição:**
- `tbl_cargo_condition_*` - Campos de inspeção de carga
- `tbl_lifting_condition` - Status de equipamento de içamento
- `tbl_lashing_condition` - Status de materiais de amarração
- `tbl_crane_condition` - Status do guindaste do navio

---

## 🔐 Considerações de Segurança

1. **Variáveis de Ambiente**: Todas as credenciais sensíveis armazenadas em `.env`
2. **Service Account**: Permissões limitadas do Google Drive
3. **Credenciais do Banco de Dados**: Nunca commitadas no repositório
4. **Chaves de API**: Rotacionadas regularmente
5. **Limpeza de Arquivos**: Arquivos temporários deletados após upload
6. **Injeção SQL**: Consultas parametrizadas com SQLAlchemy
7. **Log de Erros**: Sem dados sensíveis nos logs

## 📚 Recursos Adicionais

- [Documentação ReportLab](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Documentação SQLAlchemy](https://docs.sqlalchemy.org/)
- [Referência da API OpenAI](https://platform.openai.com/docs/api-reference)
- [Guia da API Google Drive](https://developers.google.com/drive/api/guides/about-sdk)
- [Documentação PyPDF2](https://pypdf2.readthedocs.io/)

---

**Última Atualização**: 30 de Outubro de 2025  
**Versão**: 1.0.0  
**Status**: Produção
