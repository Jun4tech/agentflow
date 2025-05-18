# Agentflow
Agentic workflow

Package Specs:
- streamlit
- fastapi
- pydantic
- langgraph
- langchain

Tools Support:
- tavily-python
- MSSQL

LLM Support:
- OpenAPI
- DeepSeekt-r1 (exclude with bind tools)

LLM Ops:
- Langsmith

RAG:
- pgvectorscale
https://github.com/timescale/pgvectorscale
-https://python.langchain.com/docs/integrations/vectorstores/timescalevector/#what-is-timescale-vector

Prequsite:
- apt-get update && apt-get install -y libpq-dev
- sudo apt-get install python3-dev

# Docker Setup
To start running in local would need to spin up docker with
```
docker compose up -d
```

To stop docker compose of running
```
docker compose down
```

# ODBC 18 Driver required to connect SQL
https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline