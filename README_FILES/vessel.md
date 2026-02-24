# API de Gerenciamento de Embarcações

Rotas dedicadas às embarcações, guindastes e capacidades SWL (Safe Working Load) utilizadas pelas aplicações a seguir: Ferramentas Digitais, Survey Reports e Gestão de Demandas.

## Get All Vessels
> GET /vessels/

Este endpoint retorna uma lista de todas as embarcações cadastradas no sistema, ordenadas por nome.

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| vessel_id | Integer | Identificador único da embarcação | 1 |
| imo_number | String | Número IMO da embarcação | "IMO9876543" |
| vessel_name | String | Nome da embarcação | "Navio Exemplo" |
| vessel_type | String | Tipo da embarcação | "Barge" |
| vessel_length | Float | Comprimento da embarcação (m) | 120.5 |
| vessel_breadth | Float | Largura da embarcação (m) | 22.3 |
| vessel_beam | Float | Boca da embarcação (m) | 22.3 |
| vessel_depth | Float | Profundidade da embarcação (m) | 10.2 |
| loaded_draft | Float | Calado carregado (m) | 8.5 |
| light_draft | Float | Calado leve (m) | 3.2 |
| gross_tonnage | Float | Tonelagem bruta | 15000.0 |
| bollard_pull | Float | Tração estática (apenas para rebocadores) | 80.0 |
| has_crane | Boolean | Indica se a embarcação possui guindastes | true |
| country_flag | String | Bandeira do país | "Brasil" |
| year_of_built | String | Ano de construção | "2015" |
| dwt | Float | Deadweight tonnage | 25000.0 |
| client_id | Integer | ID do cliente proprietário | 5 |

## Get Vessel by ID
> GET /vessels/{vessel_id}

Este endpoint recupera os detalhes de uma embarcação específica com base em seu ID, incluindo todos os seus guindastes e capacidades SWL associadas em uma estrutura hierárquica.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_id | Integer | ID da embarcação (parte da URL) | Sim | 1 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| vessel_id | Integer | Identificador único da embarcação | 1 |
| imo_number | String | Número IMO da embarcação | "IMO9876543" |
| vessel_name | String | Nome da embarcação | "Navio Exemplo" |
| vessel_type | String | Tipo da embarcação | "Barge" |
| vessel_length | Float | Comprimento da embarcação (m) | 120.5 |
| vessel_breadth | Float | Largura da embarcação (m) | 22.3 |
| vessel_beam | Float | Boca da embarcação (m) | 22.3 |
| vessel_depth | Float | Profundidade da embarcação (m) | 10.2 |
| loaded_draft | Float | Calado carregado (m) | 8.5 |
| light_draft | Float | Calado leve (m) | 3.2 |
| gross_tonnage | Float | Tonelagem bruta | 15000.0 |
| bollard_pull | Float | Tração estática (apenas para rebocadores) | 80.0 |
| has_crane | Boolean | Indica se a embarcação possui guindastes | true |
| country_flag | String | Bandeira do país | "Brasil" |
| year_of_built | String | Ano de construção | "2015" |
| dwt | Float | Deadweight tonnage | 25000.0 |
| client_id | Integer | ID do cliente proprietário | 5 |
| cranes | Array | Lista de guindastes com suas capacidades SWL | [Objeto Crane] |

## Add Vessel
> POST /vessels/

Este endpoint permite adicionar uma nova embarcação ao sistema, opcionalmente com guindastes e capacidades SWL associadas.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_name | String | Nome da embarcação | Sim | "Navio Exemplo" |
| vessel_type | String | Tipo da embarcação (Barge ou Tugboat) | Sim | "Barge" |
| vessel_length | Float | Comprimento da embarcação (m) | Sim | 120.5 |
| vessel_breadth | Float | Largura da embarcação (m) | Sim | 22.3 |
| vessel_beam | Float | Boca da embarcação (m) | Sim | 22.3 |
| vessel_depth | Float | Profundidade da embarcação (m) | Sim | 10.2 |
| loaded_draft | Float | Calado carregado (m) | Sim | 8.5 |
| light_draft | Float | Calado leve (m) | Sim | 3.2 |
| gross_tonnage | Float | Tonelagem bruta | Sim | 15000.0 |
| has_crane | Boolean | Indica se a embarcação possui guindastes | Sim | true |
| bollard_pull | Float | Tração estática (apenas para rebocadores) | Não | 80.0 |
| imo_number | String | Número IMO da embarcação | Não | "IMO9876543" |
| country_flag | String | Bandeira do país | Não | "Brasil" |
| year_of_built | String | Ano de construção | Não | "2015" |
| dwt | Float | Deadweight tonnage | Não | 25000.0 |
| client_id | Integer | ID do cliente proprietário | Não | 5 |
| cranes | Array | Lista de guindastes da embarcação | Não | [Objeto Crane] |

### Modelo do Objeto Crane

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| position_on_vessel | String | Posição do guindaste na embarcação | Sim | "PS" |
| swl_capacities | Array | Lista de capacidades SWL do guindaste | Não | [Objeto SWL] |

### Modelo do Objeto SWL

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| weight | Float | Capacidade de peso (t) | Sim | 50.0 |
| radius_start | Float | Raio inicial (m) | Sim | 5.0 |
| radius_end | Float | Raio final (m) | Sim | 15.0 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "Vessel created successfully" |
| vessel_id | Integer | ID da embarcação criada | 1 |

## Update Vessel
> PUT /vessels/{vessel_id}

Este endpoint permite atualizar informações de uma embarcação específica, incluindo seus guindastes e capacidades SWL. O tipo da embarcação não pode ser alterado após a criação. A operação suporta atualizações parciais e permite adicionar novos guindastes ou capacidades SWL.

Novos guindastes e capacidades SWL devem ser incluídos no corpo da requisição seguindo o modelo de Crane e SWL Objects **sem o id**, assim a rota perceberá o novo objeto e fará a inclusão.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_id | Integer | ID da embarcação (parte da URL) | Sim | 1 |
| vessel_name | String | Nome da embarcação | Não | "Navio Exemplo Atualizado" |
| vessel_length | Float | Comprimento da embarcação (m) | Não | 125.5 |
| vessel_breadth | Float | Largura da embarcação (m) | Não | 23.3 |
| vessel_beam | Float | Boca da embarcação (m) | Não | 23.3 |
| vessel_depth | Float | Profundidade da embarcação (m) | Não | 11.2 |
| loaded_draft | Float | Calado carregado (m) | Não | 9.5 |
| light_draft | Float | Calado leve (m) | Não | 3.5 |
| gross_tonnage | Float | Tonelagem bruta | Não | 16000.0 |
| has_crane | Boolean | Indica se a embarcação possui guindastes | Não | true |
| bollard_pull | Float | Tração estática (apenas para rebocadores) | Não | 85.0 |
| imo_number | String | Número IMO da embarcação | Não | "IMO9876544" |
| country_flag | String | Bandeira do país | Não | "Portugal" |
| year_of_built | String | Ano de construção | Não | "2016" |
| dwt | Float | Deadweight tonnage | Não | 26000.0 |
| client_id | Integer | ID do cliente proprietário | Não | 6 |
| cranes | Array | Lista de guindastes a atualizar ou adicionar | Não | [Objeto Crane] |

### Modelo do Objeto Crane para Atualização

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| crane_id | Integer | ID do guindaste (necessário para atualização) | Não | 1 |
| position_on_vessel | String | Posição do guindaste na embarcação | Sim | "SB" |
| swl_capacities | Array | Lista de capacidades SWL a atualizar ou adicionar | Não | [Objeto SWL] |

### Modelo do Objeto SWL para Atualização

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| swl_capacity_id | Integer | ID da capacidade SWL (necessário para atualização) | Não | 1 |
| weight | Float | Capacidade de peso (t) | Sim | 60.0 |
| radius_start | Float | Raio inicial (m) | Sim | 6.0 |
| radius_end | Float | Raio final (m) | Sim | 16.0 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "Vessel and all related data updated successfully" |

## Delete Vessel
> DELETE /vessels/{vessel_id}

Este endpoint permite remover uma embarcação específica do sistema, junto com todos os seus guindastes e capacidades SWL associados.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_id | Integer | ID da embarcação a ser excluída (parte da URL) | Sim | 1 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "Vessel and all related data deleted successfully" |

## Get Vessel Cranes
> GET /vessels/{vessel_id}/cranes

Este endpoint recupera todos os guindastes associados a uma embarcação específica.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_id | Integer | ID da embarcação (parte da URL) | Sim | 1 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| crane_id | Integer | Identificador único do guindaste | 1 |
| vessel_id | Integer | ID da embarcação a que pertence | 1 |
| position_on_vessel | String | Posição do guindaste na embarcação | "PS" |

## Get Crane by ID
> GET /vessels/{vessel_id}/cranes/{crane_id}

Este endpoint recupera os detalhes de um guindaste específico em uma embarcação.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_id | Integer | ID da embarcação (parte da URL) | Sim | 1 |
| crane_id | Integer | ID do guindaste (parte da URL) | Sim | 1 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| crane_id | Integer | Identificador único do guindaste | 1 |
| vessel_id | Integer | ID da embarcação a que pertence | 1 |
| position_on_vessel | String | Posição do guindaste na embarcação | "PS" |

## Update Crane
> PUT /vessels/{vessel_id}/cranes/{crane_id}

Este endpoint permite atualizar informações de um guindaste específico em uma embarcação.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_id | Integer | ID da embarcação (parte da URL) | Sim | 1 |
| crane_id | Integer | ID do guindaste (parte da URL) | Sim | 1 |
| position_on_vessel | String | Nova posição do guindaste na embarcação | Sim | "SB" |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "Crane updated successfully" |

## Delete Crane
> DELETE /vessels/{vessel_id}/cranes/{crane_id}

Este endpoint permite remover um guindaste específico de uma embarcação, junto com todas as suas capacidades SWL associadas.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_id | Integer | ID da embarcação (parte da URL) | Sim | 1 |
| crane_id | Integer | ID do guindaste a ser excluído (parte da URL) | Sim | 1 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "Crane and all related SWL capacities deleted successfully" |

## Get Crane SWL Capacities
> GET /vessels/{vessel_id}/cranes/{crane_id}/swl

Este endpoint recupera todas as capacidades SWL associadas a um guindaste específico em uma embarcação.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_id | Integer | ID da embarcação (parte da URL) | Sim | 1 |
| crane_id | Integer | ID do guindaste (parte da URL) | Sim | 1 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| swl_capacity_id | Integer | Identificador único da capacidade SWL | 1 |
| crane_id | Integer | ID do guindaste a que pertence | 1 |
| weight | Float | Capacidade de peso (t) | 50.0 |
| radius_start | Float | Raio inicial (m) | 5.0 |
| radius_end | Float | Raio final (m) | 15.0 |

## Update SWL Capacity
> PUT /vessels/{vessel_id}/cranes/{crane_id}/swl/{swl_capacity_id}

Este endpoint permite atualizar informações de uma capacidade SWL específica de um guindaste.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_id | Integer | ID da embarcação (parte da URL) | Sim | 1 |
| crane_id | Integer | ID do guindaste (parte da URL) | Sim | 1 |
| swl_capacity_id | Integer | ID da capacidade SWL (parte da URL) | Sim | 1 |
| weight | Float | Nova capacidade de peso (t) | Sim | 60.0 |
| radius_start | Float | Novo raio inicial (m) | Sim | 6.0 |
| radius_end | Float | Novo raio final (m) | Sim | 16.0 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "SWL capacity updated successfully" |

## Delete SWL Capacity
> DELETE /vessels/{vessel_id}/cranes/{crane_id}/swl/{swl_capacity_id}

Este endpoint permite remover uma capacidade SWL específica de um guindaste.

### Parâmetros de Requisição

| Nome | Tipo | Descrição | Obrigatório | Exemplo |
|------|------|-----------|-------------|---------|
| vessel_id | Integer | ID da embarcação (parte da URL) | Sim | 1 |
| crane_id | Integer | ID do guindaste (parte da URL) | Sim | 1 |
| swl_capacity_id | Integer | ID da capacidade SWL a ser excluída (parte da URL) | Sim | 1 |

### Dados de Resposta

| Nome | Tipo | Descrição | Exemplo |
|------|------|-----------|---------|
| message | String | Mensagem de confirmação | "SWL capacity deleted successfully" |