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

LLM Support:
- OpenAPI
- DeepSeekt not with bind tools

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