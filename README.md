# Atendimento Automatizado via WhatsApp com IA

API REST desenvolvida em **Python e FastAPI** para automatizar o atendimento de clientes via **WhatsApp**, utilizando a **Gemini API** para geração de respostas contextualizadas e **MariaDB** para armazenamento e consulta dos dados dos clientes.

O projeto foi desenvolvido com foco em criar um sistema capaz de identificar o cliente a partir do número de telefone, recuperar seus dados e histórico de conversas e utilizar essas informações como contexto para gerar respostas personalizadas.

---

## Funcionalidades

### Atendimento via WhatsApp

Integração com a **WhatsApp Cloud API** para receber e enviar mensagens automaticamente.

O sistema utiliza **webhooks** para receber eventos enviados pela Meta em tempo real.

Fluxo simplificado:

```text
Cliente
   │
   ▼
WhatsApp
   │
   ▼
WhatsApp Cloud API
   │
   ▼
Webhook (FastAPI)
   │
   ├── Identificação do cliente
   │
   ├── Recuperação dos dados
   │
   ├── Recuperação do histórico
   │
   ▼
Gemini API
   │
   ▼
Resposta gerada
   │
   ▼
WhatsApp Cloud API
   │
   ▼
Cliente
```

---

### Geração de respostas com Gemini

A aplicação utiliza a **Gemini API** para gerar respostas automaticamente.

O prompt enviado ao modelo pode considerar informações como:

* Nome do cliente;
* Valor da dívida;
* Data de vencimento;
* Status da negociação;
* Histórico da conversa;
* Mensagens enviadas anteriormente pelo cliente.

Dessa forma, a IA não trata cada mensagem como uma conversa isolada.

---

### Contexto individual por cliente

O histórico das conversas é separado por cliente.

Ao receber uma nova mensagem, o sistema:

1. Identifica o número de telefone do remetente;
2. Localiza o cliente correspondente no banco de dados;
3. Recupera o histórico daquela conversa;
4. Registra a nova mensagem;
5. Utiliza o histórico como contexto para o Gemini;
6. Gera uma resposta contextualizada;
7. Envia a resposta de volta ao WhatsApp.

Isso permite que a IA mantenha o contexto da conversa em vez de responder somente com base na última mensagem recebida.

---

### Integração com MariaDB

O sistema consulta os dados dos clientes diretamente no banco de dados.

As informações recuperadas são transformadas em objetos utilizados pela aplicação, permitindo que os dados do cliente sejam utilizados tanto na construção dos prompts quanto na identificação e gerenciamento das conversas.

---

## Arquitetura

O projeto utiliza uma organização em camadas, separando responsabilidades entre diferentes componentes:

```text
MiniDigiSacFastAPI/
│
├── database/
│
├── models/
│
├── repositories/
│
├── routes/
│
├── services/
│
└── main.py
```

### `routes`

Responsável pelos endpoints da API e pelo recebimento das requisições.

Exemplo:

```text
POST /webhook
```

Endpoint utilizado pela WhatsApp Cloud API para enviar eventos e mensagens recebidas.

### `services`

Contém a lógica de negócio da aplicação, incluindo:

* Processamento dos clientes;
* Construção dos prompts;
* Integração com o Gemini;
* Gerenciamento do contexto;
* Construção das mensagens para o WhatsApp.

### `repositories`

Responsável pelo acesso e manipulação dos dados persistidos.

### `models`

Contém os modelos utilizados pela aplicação, utilizando **Pydantic** para validação e estruturação dos dados.

### `database`

Responsável pela conexão com o banco de dados.

---

## Tecnologias utilizadas

| Tecnologia             | Utilização                             |
| ---------------------- | -------------------------------------- |
| **Python**             | Linguagem principal                    |
| **FastAPI**            | Desenvolvimento da API REST            |
| **Pydantic**           | Modelagem e validação dos dados        |
| **MariaDB**            | Banco de dados                         |
| **WhatsApp Cloud API** | Comunicação com os clientes            |
| **Gemini API**         | Geração das respostas utilizando IA    |
| **Webhooks**           | Recebimento de mensagens em tempo real |

---

## Comunicação com a Meta

O projeto utiliza um endpoint público para receber os webhooks enviados pela Meta.

O webhook possui dois comportamentos principais:

### GET `/webhook`

Utilizado pela Meta durante a verificação do endpoint.

A aplicação valida o `hub.verify_token` e retorna o `hub.challenge` quando a requisição é válida.

### POST `/webhook`

Recebe os eventos enviados pela WhatsApp Cloud API, incluindo mensagens recebidas pelos clientes.

A aplicação extrai informações como:

* Número do remetente;
* Nome do contato;
* ID da mensagem;
* Timestamp;
* Conteúdo da mensagem;
* Tipo da mensagem.

---

# Possíveis melhorias

O projeto foi desenvolvido de forma modular para permitir a expansão das funcionalidades.

## Pagamentos via Pix

Uma possível evolução seria integrar o sistema ao processo de pagamento das dívidas.

O cliente poderia solicitar uma forma de pagamento durante a conversa e o sistema poderia gerar automaticamente:

* Código Pix Copia e Cola;
* QR Code para pagamento;
* Identificação da dívida;
* Valor atualizado da negociação.

Uma integração posterior com um provedor de pagamentos também poderia permitir a confirmação automática do pagamento.

---

## Reconhecimento de mensagens de áudio

Outra evolução seria permitir que o cliente envie mensagens de voz.
Isso permitiria que o chatbot tratasse mensagens de áudio praticamente da mesma maneira que mensagens de texto.

---

## Templates para iniciar conversas

Atualmente o fluxo principal depende de uma mensagem recebida pelo cliente.

Uma futura implementação poderia utilizar os **templates aprovados pela Meta** para iniciar o contato com clientes.

Isso permitiria, por exemplo, enviar automaticamente uma notificação sobre uma dívida antes que o cliente envie qualquer mensagem.

Possíveis aplicações:

* Aviso de vencimento;
* Lembrete de pagamento;
* Oferta de negociação;
* Confirmação de acordo;
* Notificação de pagamento;
* Recuperação de clientes inativos.
