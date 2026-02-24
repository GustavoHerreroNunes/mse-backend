# MSE API

Este projeto é uma API para acesso ao banco de dados central para os projetos da MSE em conjunto com a AutoU. A API foi desenvolvida em Flask e aponta para um servidor PostgreSQL.

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd mse-api
   ```

2. **Create a virtual environment:**
   ```
   py -3 -m venv .venv;
   .venv\Scripts\activate;
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   - Crie um arquivo .env com a url para o servidor/database

5. **Google Credentials**
   - Execute o comando abaixo para salvar suas credenciais de acesso no ambiente local para uso do SDK do Google
   ```
   gcloud auth application-default login
   ```

6. **Run the application:**
   > Ambiente de desenvolvimento
   ```
   flask --app main run
   ```
## Deploy to Cloud Instructions

0. **Switch to correct Environment**
   ```
   gcloud config set project msenaval-453016
   ```

1. **Deploy api to Google Cloud Run (with PDF processing support)**
   ```
   gcloud run deploy mse-api --region southamerica-east1 --source .
   ```
   
   **Note:** Increased memory, CPU, and timeout for PDF/OCR processing

2. **Update api-gateway.yaml**
   Garanta que todas a rotas adicionadas ou atualizadas estão incluídas no arquivo de configuração do gateway. Depois, incremente o valor do atributo "version" dentro do arquivo.

   **Importante:** Todas as rotas documentadas no *api-gateway.yaml* devem referenciar o host do Cloud Run de TESTE:
   
   ```yaml
   /example/of/route/:
    get:
      ...
      x-google-backend:
        address: https://mse-api-152754594972.southamerica-east1.run.app -- CLOUD RUN
        path_translation: APPEND_PATH_TO_ADDRESS
   ```

3. **Deploy the new api configuration**
   ```
   gcloud api-gateway api-configs create mse-gateway-live-<version_num> --api=mse-api-gateway --openapi-spec=api-gateway.yaml --project=msenaval-453016 --backend-auth-service-account=msegateway-admin@msenaval-453016.iam.gserviceaccount.com
   ```
4. **Activate new API Gateway configuration**
   ```
   gcloud api-gateway gateways update mse-api-gateway --api=mse-api-gateway --api-config=mse-gateway-live-<version_num> --location=us-west2 --project=msenaval-453016
   ```

## Documentação da API

### API de Gerenciamento de Usuários Surveyor

Esta API fornece endpoints para gerenciar usuários surveyor no sistema. Ela permite listar, criar, visualizar, atualizar e excluir usuários, com suporte para autenticação segura através de senhas com hash.


### Configurações e Requisitos

Para garantir a segurança no acesso ao serviço, esta api só está disponível através do API gateway mse-api-gateway no Google Cloud. por isso a URL base de todas as requisições deve ser:


```
https://mse-api-gateway-1y6a53to.wl.gateway.dev
```

Além disso, todas as requisições devem ser feitas com uma chave de API no header **x-api-key** com o seguinte valor:

```json
{
   "x-api-key": "AIzaSyAWtIMnJZAWvXGd5qLjzhAF_a7kch7LoFA"
}
```

Cada enpoint tem seus próprios requisitos para cada método solicitado, podendo ser um query pararemter (indicado no enpoint entre chaves **{<parameter>}**) ou um body de requisição com parâmetros específicos (indicados nas tabelas).

```json
//Exemplo de body

{
   "display_name": "Nome",
   "email": "example@email",
   "password": "1234Passw@rd"
}

```

### Códigos de Status

As APIs utilizam os seguintes códigos de status HTTP:

- 200: Operação bem-sucedida
- 201: Recurso criado com sucesso
- 400: Requisição inválida (dados insuficientes ou incorretos)
- 401: Não autorizado (credenciais inválidas)
- 404: Recurso não encontrado
- 500: Erro interno do servidor

