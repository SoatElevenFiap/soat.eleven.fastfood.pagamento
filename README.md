# Microservice Payment

Microserviço responsável por gerenciar pagamentos através de provedores externos (como Mercado Pago), processar webhooks de notificações de pagamento e notificar sistemas clientes sobre atualizações de status.

![Arquitetura Macro](docs/.assets/images/macro-architeture.png)

## 📋 Índice

- [Sobre o Microserviço](#sobre-o-microserviço)
- [Objetivos](#objetivos)
- [Arquitetura](#arquitetura)
- [Endpoints](#endpoints)
- [Stack Tecnológica](#stack-tecnológica)
- [Configuração](#configuração)
- [Desenvolvimento](#desenvolvimento)
- [Deploy](#deploy)
- [Segurança](#segurança)

## 🎯 Sobre o Microserviço

Este microserviço é parte do sistema FastFood e é responsável por:

- **Gerenciamento de Pagamentos**: Criar e gerenciar ordens de pagamento através de provedores externos
- **Processamento de Webhooks**: Receber e processar notificações de provedores de pagamento (Mercado Pago)
- **Notificação de Clientes**: Enviar atualizações de status de pagamento para sistemas clientes cadastrados
- **Gerenciamento de Clientes**: Cadastrar e gerenciar clientes que utilizam o serviço de pagamento

### Funcionalidades Principais

- ✅ Criação de ordens de pagamento com múltiplos itens
- ✅ Integração com provedores externos (Mercado Pago)
- ✅ Processamento assíncrono de webhooks
- ✅ Notificação automática de clientes sobre mudanças de status
- ✅ Cache de dados para melhor performance
- ✅ Persistência de dados em MongoDB
- ✅ Integração com Azure Key Vault para secrets

## 🎯 Objetivos

### Objetivos Gerais

1. **Centralizar o Gerenciamento de Pagamentos**: Fornecer uma API única para gerenciar pagamentos através de múltiplos provedores
2. **Desacoplar Sistemas**: Permitir que outros microserviços criem pagamentos sem conhecer detalhes dos provedores
3. **Garantir Rastreabilidade**: Manter histórico completo de todas as operações de pagamento
4. **Notificação em Tempo Real**: Garantir que sistemas clientes sejam notificados sobre mudanças de status
5. **Segurança**: Proteger informações sensíveis usando Azure Key Vault em produção

### Objetivos Técnicos

- Arquitetura limpa e desacoplada (Clean Architecture)
- Alta disponibilidade e escalabilidade
- Observabilidade através de logs estruturados
- Testes automatizados com alta cobertura
- CI/CD completo com validação de qualidade

## 🏗️ Arquitetura

O microserviço segue uma arquitetura em camadas (Clean Architecture) com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (Controllers)               │
│  PaymentController | ClientController | WebhookController│
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              Application Layer (Services)                │
│  CreatePaymentOrderService | GetPaymentService | ...     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                Domain Layer (Services)                    │
│  CreatePaymentService | NotifyListenersService | ...     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│            Infrastructure Layer (Repositories)           │
│  PaymentRepository | ClientRepository | MongoService     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              External Services                           │
│  MongoDB | Redis | Azure Key Vault | Mercado Pago       │
└─────────────────────────────────────────────────────────┘
```

### Fluxo de Pagamento

1. Cliente envia requisição → `POST /v1/payment/`
2. Sistema cria ordem no provedor externo (Mercado Pago)
3. Retorna URL de redirecionamento para pagamento
4. Usuário final realiza pagamento no provedor
5. Provedor envia webhook → `POST /v1/webhook/mercado-pago/`
6. Sistema processa notificação e atualiza status
7. Sistema notifica cliente cadastrado via webhook

## 🔌 Endpoints

### Health Check

```http
GET /health-check
```

Retorna informações sobre o status do microserviço.

**Response:**
```json
{
  "message": "Microservice Payment is running",
  "version": "0.1.0",
  "environment": "development"
}
```

### Clientes

#### Criar Cliente

```http
POST /v1/client/
```

Cria um novo cliente no sistema.

**Request Body:**
```json
{
  "name": "sistema-pedidos",
  "notification_url": "https://api.exemplo.com/webhook/payment"
}
```

**Response:** `ClientDto`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "sistema-pedidos",
  "notification_url": "https://api.exemplo.com/webhook/payment",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Listar Clientes

```http
GET /v1/client/
```

Retorna lista de todos os clientes cadastrados.

**Response:** `List[ClientDto]`

### Pagamentos

#### Criar Pagamento

```http
POST /v1/payment/
```

Cria uma nova ordem de pagamento.

**Request Body:**
```json
{
  "end_to_end_id": "pedido-12345",
  "client_id": "507f1f77bcf86cd799439011",
  "items": [
    {
      "title": "Hambúrguer",
      "quantity": 2,
      "unit_price": 25.50
    },
    {
      "title": "Batata Frita",
      "quantity": 1,
      "unit_price": 12.00
    }
  ],
  "description": "Pedido #12345",
  "provider": "mercadopago",
  "metadata": {
    "order_id": "12345",
    "customer_id": "67890"
  }
}
```

**Response:** `PaymentDto`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "end_to_end_id": "pedido-12345",
  "client_id": "507f1f77bcf86cd799439011",
  "value": 63.00,
  "provider": "mercadopago",
  "status": "pending",
  "redirect_url": "https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=...",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Buscar Pagamento

```http
GET /v1/payment/?id={payment_id}
GET /v1/payment/?end_to_end_id={end_to_end_id}
```

Busca um pagamento por ID ou `end_to_end_id`.

**Query Parameters:**
- `id` (opcional): ID do pagamento
- `end_to_end_id` (opcional): ID externo do pagamento

**Response:** `PaymentDto`

### Webhooks

#### Webhook Mercado Pago

```http
POST /v1/webhook/mercado-pago/
```

Endpoint para receber notificações do Mercado Pago sobre atualizações de pagamento.

**⚠️ Acesso:** Este endpoint é exposto externamente via API Gateway. Outros endpoints são apenas para acesso interno.

**Request Body:** (Enviado pelo Mercado Pago)
```json
{
  "action": "payment.created",
  "api_version": "v1",
  "data": {
    "id": "123456789"
  },
  "date_created": "2024-01-15T10:30:00Z",
  "id": 123456789,
  "live_mode": true,
  "type": "payment",
  "user_id": "123456789"
}
```

**Response:**
```json
{
  "message": "External feedback processed successfully"
}
```

## 🛠️ Stack Tecnológica

### Backend
- **Python**: 3.12+
- **FastAPI**: Framework web assíncrono
- **Pydantic**: Validação de dados e settings
- **uv**: Gerenciador de pacotes moderno

### Banco de Dados e Cache
- **MongoDB**: Banco de dados NoSQL (via pymongo)
- **Redis**: Cache em memória

### Integrações
- **Mercado Pago SDK**: Integração com provedor de pagamento
- **Azure Key Vault**: Gerenciamento de secrets em produção
- **Azure Identity**: Autenticação Azure

### Ferramentas de Desenvolvimento
- **pytest**: Framework de testes
- **ruff**: Linter rápido
- **black**: Formatador de código
- **isort**: Organizador de imports
- **pyright**: Type checker

### Infraestrutura
- **Docker**: Containerização
- **Kubernetes**: Orquestração (AKS)
- **Azure Container Registry**: Registry de imagens
- **GitHub Actions**: CI/CD

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Ambiente
ENVIRONMENT=development

# Banco de Dados
MONGO_CONNECTION_STRING=mongodb://localhost:27017
REDIS_CONNECTION_STRING=redis://localhost:6379

# Azure Key Vault (Produção)
AZURE_KEY_VAULT_ENABLED=false
AZURE_KEY_VAULT_URL=https://seu-keyvault.vault.azure.net/

# Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN=seu_token_aqui
```

### Configuração por Ambiente

#### Development
- Usa variáveis de ambiente do `.env`
- Key Vault desabilitado
- Logs detalhados

#### Production
- Usa Azure Key Vault para secrets (Redis e MongoDB)
- Fallback para variáveis de ambiente se Key Vault não disponível
- Logs otimizados

### Azure Key Vault

Em produção, os seguintes secrets devem estar configurados no Key Vault:
- `redis-connection-string`: String de conexão do Redis
- `mongo-connection-string`: String de conexão do MongoDB

## 🚀 Desenvolvimento

### Pré-requisitos

- Python 3.12+
- uv instalado
- MongoDB rodando (ou via Docker)
- Redis rodando (ou via Docker)

### Instalação

```bash
# Instalar dependências
uv sync

# Instalar dependências de desenvolvimento
uv sync --dev
```

### Executar Localmente

```bash
# Modo desenvolvimento
uv run task run_dev

# A API estará disponível em http://localhost:8000
# Documentação interativa em http://localhost:8000/docs
```

### Docker Compose

```bash
# Subir infraestrutura (MongoDB e Redis)
docker-compose -f docker-compose.infra.yml up -d

# Subir aplicação
docker-compose up -d
```

### Comandos Úteis

```bash
# Linting
uv run task lint

# Type checking
uv run task typecheck

# Testes
uv run task test

# Testes em modo watch
uv run task test_watch
```

## 📦 Deploy

### Kubernetes (AKS)

O microserviço é implantado no Azure Kubernetes Service (AKS) através do workflow de CI/CD.

**Configuração:**
- **Namespace**: `fastfood`
- **Service**: `ClusterIP` (acesso apenas interno)
- **Webhook**: Exposto externamente via API Gateway

### CI/CD Pipeline

O pipeline GitHub Actions executa:

1. **Quality Check** (Pull Requests):
   - Lint e formatação
   - Testes unitários
   - Análise SonarCloud

2. **Deploy** (Push para `main`):
   - Build da imagem Docker
   - Push para Azure Container Registry
   - Deploy no AKS

### Secrets Necessários

Configure os seguintes secrets no GitHub:

- `AZURE_CREDENTIALS`: Service Principal do Azure (JSON)
- `SONAR_TOKEN`: Token do SonarCloud

## 🔒 Segurança

### Acesso

- **Acesso Interno**: Todos os endpoints são acessíveis apenas dentro do cluster Kubernetes
- **Acesso Externo**: Apenas `/v1/webhook/mercado-pago/` é exposto via API Gateway
- **Network Policy**: Configurada para permitir acesso apenas de microserviços internos e API Gateway

### Secrets

- **Development**: Secrets armazenados em `.env` (não commitar)
- **Production**: Secrets armazenados no Azure Key Vault
- **Fallback**: Se Key Vault não disponível, usa variáveis de ambiente

### Autenticação Azure

O microserviço usa `DefaultAzureCredential` que tenta autenticar na seguinte ordem:
1. Variáveis de ambiente
2. Managed Identity (quando rodando no Azure)
3. Azure CLI (desenvolvimento local)

## 📊 Status de Pagamento

Os pagamentos podem ter os seguintes status:

- `pending`: Aguardando pagamento
- `paid`: Pago com sucesso
- `failed`: Falha no pagamento
- `cancelled`: Cancelado
- `refund_requested`: Reembolso solicitado
- `refunded`: Reembolsado
- `error`: Erro no processamento

## 🔄 Fluxo de Notificação

1. Cliente cria pagamento via `POST /v1/payment/`
2. Sistema cria ordem no provedor externo
3. Retorna `redirect_url` para pagamento
4. Usuário final realiza pagamento
5. Provedor envia webhook para `/v1/webhook/mercado-pago/`
6. Sistema processa notificação e atualiza status
7. Sistema busca cliente pelo `client_id`
8. Sistema envia notificação para `notification_url` do cliente
9. Cliente recebe atualização de status

## 📝 Observações Importantes

- O microserviço não expõe endpoints HTTP diretamente ao mundo externo
- Apenas a rota de webhook é exposta via API Gateway
- Todos os outros endpoints são acessíveis apenas internamente
- O sistema usa correlation ID para rastreamento de requisições
- Logs incluem correlation ID automaticamente

## 🧪 Testes

```bash
# Executar todos os testes
uv run task test

# Executar testes unitários
pytest src/tests/ -m unit

# Executar testes de integração
pytest src/tests/ -m integration

# Ver cobertura
uv run task test
# Relatório HTML em htmlcov/index.html
```

## 📚 Documentação Adicional

- **Arquitetura Macro**: Ver `docs/.assets/images/macro-architeture.png`
- **API Docs**: Disponível em `/docs` quando a aplicação está rodando
- **Swagger UI**: Disponível em `/docs`
- **ReDoc**: Disponível em `/redoc`

## 🤝 Contribuindo

1. Crie uma branch a partir de `main`
2. Faça suas alterações
3. Execute `uv run task lint` e `uv run task test`
4. Abra um Pull Request
5. O pipeline de qualidade será executado automaticamente

## 📄 Licença

Este projeto faz parte do sistema FastFood desenvolvido para o SOAT Eleven.
