# MSE API

API REST central do ecossistema de soluções MSE, desenvolvida em parceria entre MSE e AutoU. Construída em Python com Flask, é o backend principal para os módulos de Survey Reports (Mobile App, Portal do Cliente e Portal do Admin) e para operações críticas do Gestão de Demandas que excedem as capacidades nativas do Bubble.

A API é hospedada no **Google Cloud Run** e acessível exclusivamente através do **API Gateway**, que centraliza autenticação e controle de acesso. A conexão com o banco de dados PostgreSQL é realizada via **Cloud SQL Auth Proxy sidecar**, utilizando socket Unix.

Para uma visão completa da infraestrutura do ecossistema, consulte o **Registro de Infraestrutura MSE** e a **Documentação do Ecossistema MSE**.

---

## Desenvolvimento Local

### Pré-requisitos

- Python 3.11+
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) instalado e autenticado
- Acesso ao projeto `msesolucoes` no GCP

### 1. Clonar o repositório

```bash
git clone <repository-url>
cd mse-api
```

### 2. Criar e ativar o ambiente virtual

**Windows:**
```bash
py -3 -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto. Para desenvolvimento local, use uma `DATABASE_URL` direta. Em produção no Cloud Run, a conexão é feita via socket Unix do Auth Proxy — o `config.py` detecta automaticamente qual modo usar com base na presença da variável `INSTANCE_CONNECTION_NAME`.

```env
# Desenvolvimento local — conexão direta
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_banco

# Produção (Cloud Run) — via Cloud SQL Auth Proxy sidecar
# DB_USER=
# DB_PASS=
# DB_NAME=
# INSTANCE_CONNECTION_NAME=msesolucoes:southamerica-east1:mse-db
```

> Nunca commite o arquivo `.env`. Ele já está incluído no `.gitignore`.

### 5. Autenticar credenciais Google localmente

Necessário para serviços que utilizam o SDK do Google (ex: leitura de PDFs via Document AI):

```bash
gcloud auth application-default login
```

### 6. Executar a aplicação

```bash
flask --app main run
```

A API estará disponível em `http://localhost:5000`.

---

## Deploy — CI/CD Automatizado

O deploy é totalmente automatizado via **GitHub Actions**. Qualquer push na branch `main` aciona o pipeline que:

1. Constrói a imagem Docker e envia ao **Artifact Registry** (`mse-api-repo`), tagueada com o SHA do commit
2. Faz deploy da nova imagem no **Cloud Run** (`mse-api`, região `southamerica-east1`)
3. Cria uma nova configuração do **API Gateway** a partir do `api-gateway.yaml`
4. Ativa a nova configuração no gateway

> Para acionar o deploy, basta fazer push em `main`. Não é necessário rodar comandos manuais.

### Atualizando rotas no API Gateway

Sempre que uma rota for adicionada ou modificada, é necessário:

1. Atualizar o arquivo `api-gateway.yaml` incluindo a nova rota
2. **Incrementar o campo `version`** dentro do `api-gateway.yaml` — o pipeline usa esse valor para nomear a nova configuração do gateway. Se a versão não for incrementada, o deploy falhará com erro de configuração duplicada

Todas as rotas devem referenciar a URL correta do Cloud Run e incluir o `jwt_audience`:

```yaml
/exemplo/rota:
  get:
    ...
    x-google-backend:
      address: https://mse-api-ayddoiktrq-rj.a.run.app
      path_translation: APPEND_PATH_TO_ADDRESS
      jwt_audience: https://mse-api-ayddoiktrq-rj.a.run.app
```

### Deploy manual (emergência)

Caso seja necessário fazer um deploy manual sem passar pelo CI/CD:

```bash
# 1. Autenticar e definir projeto
gcloud config set project msesolucoes

# 2. Fazer deploy no Cloud Run
gcloud run deploy mse-api \
  --region southamerica-east1 \
  --source . \
  --project msesolucoes

# 3. Criar nova configuração do API Gateway
gcloud api-gateway api-configs create mse-gateway-live-<versao> \
  --api=mse-api-gateway \
  --openapi-spec=api-gateway.yaml \
  --project=msesolucoes \
  --backend-auth-service-account=msegateway-admin@msesolucoes.iam.gserviceaccount.com

# 4. Ativar nova configuração
gcloud api-gateway gateways update mse-api-gateway \
  --api=mse-api-gateway \
  --api-config=mse-gateway-live-<versao> \
  --location=us-west2 \
  --project=msesolucoes
```

---

## Arquitetura de Acesso

```
Cliente (Bubble / FlutterFlow)
        ↓  x-api-key: <chave>
API Gateway (mse-api-gateway)
        ↓  Authorization: Bearer <google-token>
Cloud Run (mse-api)
        ↓  Unix socket
Cloud SQL Auth Proxy sidecar
        ↓
Cloud SQL — PostgreSQL (mse-db)
```

- Requisições sem `x-api-key` válido são rejeitadas pelo gateway com `401`
- Requisições diretas ao Cloud Run sem token do gateway são rejeitadas com `403`
- O Cloud Run nunca é acessado diretamente — apenas pelo gateway

---

## Consumindo a API

### URL Base

```
https://mse-api-gateway-bonpipdg.wl.gateway.dev
```

### Autenticação

Todas as requisições devem incluir o header `x-api-key`:

```json
{
  "x-api-key": "<sua-chave-de-api>"
}
```

> A chave de API é gerenciada no GCP e restrita ao serviço gerenciado do `mse-api-gateway`. Consulte o documento de variáveis de ambiente para referência.

### Formato das Requisições

Parâmetros de rota são indicados com chaves na URL: `/rota/{parametro}`

Requisições com body devem usar `Content-Type: application/json`:

```json
{
  "display_name": "Nome",
  "email": "example@email.com",
  "password": "1234Passw@rd"
}
```

### Códigos de Status

| Código | Descrição |
|---|---|
| `200` | Operação bem-sucedida |
| `201` | Recurso criado com sucesso |
| `400` | Requisição inválida — dados insuficientes ou incorretos |
| `401` | Não autorizado — chave de API ausente ou inválida |
| `403` | Proibido — requisição não veio pelo API Gateway |
| `404` | Recurso não encontrado |
| `500` | Erro interno do servidor |

---

## Variáveis de Ambiente

Para referência completa de todas as variáveis de ambiente utilizadas neste serviço e nos demais do ecossistema, consulte o documento **Variáveis de Ambiente — Ecossistema MSE**.

---

## Observações Técnicas

- **Strict slashes desabilitado**: a aplicação usa `app.url_map.strict_slashes = False` globalmente, evitando redirecionamentos 308 que quebrariam o fluxo de autenticação do API Gateway
- **Pool de conexões**: o engine SQLAlchemy é configurado com `pool_size=5` e `max_overflow=2`, adequado para o ambiente serverless do Cloud Run onde múltiplas instâncias podem ser iniciadas simultaneamente
- **Autenticação do banco**: em produção, a conexão usa socket Unix via Auth Proxy sidecar — não há senha de banco trafegando pela rede