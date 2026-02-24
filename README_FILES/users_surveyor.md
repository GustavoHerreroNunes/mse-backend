# User Surveyor - MSE API

Rotas dedicadas aos usuários do aplicativo Survey Reports.

## Get Users
> GET /surveyor/users/

Este endpoint retorna uma lista de todos os usuários surveyor cadastrados no sistema.

Este endpoint não requer parâmetros na requisição. Ele consulta todos os registros da tabela `tbl_user_surveyor` e retorna os dados completos de todos os usuários.

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| id | Integer | Identificador único do usuário | 1 |
| display_name | String | Nome de exibição do usuário | "John Doe" |
| email | String | Endereço de email do usuário | "john@example.com" |
| password | String | Senha criptografada do usuário | "pbkdf2:sha256:150000$abc123..." |

## Add User
> POST /surveyor/users/

Este endpoint permite adicionar um novo usuário surveyor ao sistema. O email é único e a senha é armazenada de forma segura com hash.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| email | String | Endereço de email do usuário | Sim | "john@example.com" |
| password | String | Senha do usuário (será convertida em hash) | Sim | "senha123" |
| display_name | String | Nome de exibição do usuário | Não | "John Doe" |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "User created successfully" |

## Get User by ID
> GET /surveyor/users/{id}

Este endpoint recupera os detalhes de um usuário surveyor específico com base em seu ID.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| id | Integer | ID do usuário (parte da URL) | Sim | 1 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| id | Integer | Identificador único do usuário | 1 |
| display_name | String | Nome de exibição do usuário | "John Doe" |
| email | String | Endereço de email do usuário | "john@example.com" |
| password | String | Senha criptografada do usuário | "pbkdf2:sha256:150000$abc123..." |

## Delete User
> DELETE /surveyor/users/{id}

Este endpoint permite remover um usuário surveyor do sistema com base em seu ID.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| id | Integer | ID do usuário a ser excluído (parte da URL) | Sim | 1 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "User deleted successfully" |

## Update User
> PUT /surveyor/users/{id}

Este endpoint permite atualizar informações de um usuário surveyor específico, como nome de exibição ou senha. Pelo menos um campo deve ser fornecido para atualização.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| id | Integer | ID do usuário a ser atualizado (parte da URL) | Sim | 1 |
| display_name | String | Novo nome de exibição do usuário | Não* | "John Smith" |
| password | String | Nova senha do usuário (será convertida em hash) | Não* | "novasenha123" |

*Pelo menos um dos campos (display_name ou password) deve ser fornecido.

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "User updated successfully" |


## Login
> POST /surveyor/auth/login

Este endpoint autentica um usuário surveyor com base nas credenciais fornecidas (email e senha). A senha é verificada de forma segura contra o hash armazenado no banco de dados.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| email | String | Endereço de email do usuário | Sim | "john@example.com" |
| password | String | Senha do usuário | Sim | "senha123" |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "User authorized" |
| user_id | Integer | ID do usuário autenticado | 1 |