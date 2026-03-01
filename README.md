# openai-compatible-orchestration

## Introduction

Hello, world! This is a repo that provide a super simple proxy (for now)
 to forward openai request and response.  
This is my exercise to enrich my knowledge in Python,
 [FastAPI](https://fastapi.tiangolo.com/learn/), [OpenAI-compatible API](https://developers.openai.com/api/reference/overview) and [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html).

---

## File structure

```txt
.
├── adapters
│   ├── controllers
│   │   ├── external_to_internal_openai.py
│   │   └── interfaces
│   │       └── i_in_converter.py
│   ├── gateways
│   ├── openai_schema.py
│   └── presenters
│       ├── interfaces
│       │   └── i_out_converter.py
│       └── internal_to_external_openai.py
├── dependencies.py
├── domain
│   └── models.py
├── infrastructure
│   ├── interfaces
│   │   └── i_provider.py
│   └── providers
│       └── ollama.py
├── main.py
├── README.md
├── requirements.txt
└── use_cases
    ├── generate_text_completion.py
    └── interfaces
        └── i_generate_text_completion.py

13 directories, 14 files

```
