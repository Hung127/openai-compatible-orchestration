from fastapi import Depends, FastAPI

from adapters.openai_schema import OpenAIRequest, OpenAIResponse
from dependencies import *
from use_cases.generate_text_completion import GenerateTextCompletionUseCase

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/v1/chat/completions")
def completions(
    request: OpenAIRequest,
    completion_use_case: GenerateTextCompletionUseCase = Depends(
        get_completion_use_case
    ),
    in_coverter: IInConverter[OpenAIRequest] = Depends(get_openai_in_converter),
    out_converter: IOutConverter[OpenAIResponse] = Depends(get_openai_out_converter),
) -> OpenAIResponse:
    # convert request into internal request
    internal_request = in_coverter.to_internal_request(request)

    # use case
    internal_response = completion_use_case.execute(internal_request)

    # convert to openai response
    openai_response = out_converter.to_external_response(internal_response)
    return openai_response


@app.get("/v1/models")
def get_models():
    # mock
    return {
        "object": "list",
        "data": [
            {
                "id": "gemma3:270m",
                "object": "model",
                "created": 1770289171,
                "owned_by": "library",
            },
            {
                "id": "smallthinker:latest",
                "object": "model",
                "created": 1770095935,
                "owned_by": "library",
            },
        ],
    }
