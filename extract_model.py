import os, json
from openai import OpenAI
from schema_pk import PK_JSON_SCHEMA

SYSTEM_PROMPT = """You are a PK model extractor. 
From the given biomedical text, infer a minimal ODE-based PK model.
- Only output VALID JSON matching the provided JSON Schema.
- Do not include explanations or any text outside the JSON.
- Use short but precise variable names (e.g., C for concentration).
- Use first-order kinetics when the text implies it.
- Set reasonable default parameter values and bounds from context if missing.
"""
USER_TEMPLATE = """TEXT:
\"\"\"{biomed_text}\"\"\"

TASK:
Return a JSON object that conforms to the schema. If absorption/elimination rates are implied, encode them.
"""


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_pk_json(biomed_text: str, model="gpt-5"):
    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(biomed_text=biomed_text)}
        ],
        # Structured Outputs (JSON Schema enforcement)
        # response_format={
        #     "type": "json_schema",
        #     "json_schema": {
        #         "name": "PKSchema",
        #         "schema": PK_JSON_SCHEMA,
        #         "strict": True  # reject non-conforming output
        #     }
        # },
        # temperature=0  # aim for determinism
    )
    # Responses API returns structured content in .output or .output_parsed for JSON formats
    return resp.output_parsed  # already a dict if schema matched
