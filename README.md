# LlamaIndex Bedrock RAG Agent Demo

This repository contains a simple demo of the LlamaIndex Agent via Amazon Bedrock Converse API.

## Prerequisites

- Python 3.6+
- awscli with configured AWS Account
- Docker (optional)

## Usage

### Setup AWS Account

Install AWS CLI and run below command to configure default profile

```bash
aws configure
```

### Setup Tavily

1. Sign up for a Tavily account at [Tavily](https://tavily.com/).
2. Create a new project and copy the API Key.

### Setup Langfuse

#### Run Langfuse with Docker

```bash
# Clone the Langfuse repository
git clone https://github.com/langfuse/langfuse.git
cd langfuse

# Start the database and langfuse server
docker compose up
```

#### Configure Langfuse

1. Open `localhost:3000/auth/sign-up` and sign up.
2. Sign-in
3. Create a organization and a project
4. Copy the Public Key and Secret Key from the project settings

### Run demo

copy `env/dev.env` to `.env` and fill in the required fields.

```bash
copy env/dev.env .env
```

Run the app

```bash
python app.py
```

