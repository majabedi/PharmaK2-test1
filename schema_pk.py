PK_JSON_SCHEMA = {
  "type": "object",
  "required": ["states", "parameters", "equations", "initial_conditions", "time"],
  "properties": {
    "states": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "unit", "description"],
        "properties": {
          "name": {"type": "string"},
          "unit": {"type": "string"},
          "description": {"type": "string"}
        }
      },
      "minItems": 1
    },
    "parameters": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "value", "unit", "description", "bounds"],
        "properties": {
          "name": {"type": "string"},
          "value": {"type": "number"},
          "unit": {"type": "string"},
          "description": {"type": "string"},
          "bounds": {
            "type": "object",
            "required": ["min", "max"],
            "properties": {
              "min": {"type": "number"},
              "max": {"type": "number"}
            }
          }
        }
      }
    },
    "equations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["lhs", "rhs"],
        "properties": {
          "lhs": {"type": "string"},  # e.g., "dC/dt"
          "rhs": {"type": "string"}   # e.g., "-k * C"
        }
      }
    },
    "initial_conditions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["state", "value"],
        "properties": {
          "state": {"type": "string"},
          "value": {"type": "number"}
        }
      }
    },
    "time": {
      "type": "object",
      "required": ["t0", "tend", "dt"],
      "properties": {
        "t0": {"type": "number"},
        "tend": {"type": "number"},
        "dt": {"type": "number"}
      }
    }
  }
}
