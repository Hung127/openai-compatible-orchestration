```txt
.
├── adapters
│   ├── controllers
│   │   ├── external_to_internal_openai.py
│   │   └── interfaces
│   │       ├── i_in_converter.py
│   │       └── __pycache__
│   │           └── i_in_converter.cpython-313.pyc
│   ├── gateways
│   ├── openai_schema.py
│   └── presenters
│       ├── interfaces
│       │   ├── i_out_converter.py
│       │   └── __pycache__
│       │       └── i_out_converter.cpython-313.pyc
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
├── __pycache__
│   ├── dependencies.cpython-313.pyc
│   └── main.cpython-313.pyc
├── README.md
├── requirements.txt
└── use_cases
    ├── generate_text_completion.py
    └── interfaces
        └── i_generate_text_completion.py

16 directories, 18 files
```
