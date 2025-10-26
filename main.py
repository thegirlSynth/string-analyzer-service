from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from datetime import datetime, timezone
from schema import StringInput
import hashlib


app = FastAPI()


STRING_DICT = {}


def generate_sha256_hash_string(input_string: str):
    hashed_string = hashlib.sha256(input_string.encode('utf-8')).hexdigest()
    return hashed_string


@app.post("/strings", status_code=201)
async def analyze_string(request: Request):
    """
    Analyzes a given string and returns it with specific properties
    """
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid JSON format in request body"}
        )

    # Manual check for field presence and type
    if "value" not in data:
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid request body or missing 'value' field"}
        )

    if not isinstance(data["value"], str):
        return JSONResponse(
            status_code=422,
            content={"detail": "Invalid data type for 'value' (must be string)"}
        )


    validated = StringInput(**data)
    value = validated.value
    sha256_hash = generate_sha256_hash_string(value)
    if sha256_hash in STRING_DICT:
        raise HTTPException(status_code=409, detail="String already exists in the system")

    reversed_string = value[::-1]
    string_length = len(value)
    is_palindrome = reversed_string.lower() == value.lower()
    unique_characters = len(set(value.lower()))
    word_count = len(value.split() if value.strip() else 0)
    time_now = datetime.now(timezone.utc).isoformat()
    character_frequency_map = {char: value.count(char) for char in set(value)}

    result = {
        "id": sha256_hash,
        "value": value,
        "properties": {
            "length": string_length,
            "is_palindrome": is_palindrome,
            "unique_characters": unique_characters,
            "word_count": word_count,
            "sha256_hash": sha256_hash,
            "character_frequency_map": character_frequency_map
        },
        "created_at": time_now
    }

    STRING_DICT.update({sha256_hash: result})
    return result


@app.get("/strings/{string_value}")
def get_specific_string(string_value: str):
    """
    Retrieves an already analyzed string from the storage object
    """
    hashed_string = generate_sha256_hash_string(string_value)
    string_properties = STRING_DICT.get(hashed_string)
    if string_properties:
        return string_properties
    raise HTTPException(status_code=404, detail="String does not exist in the system")


@app.get("/strings")
def get_strings_filtered(
    is_palindrome: bool | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    word_count: int | None = None,
    contains_character: str | None = None
):
    results = []
    for item in STRING_DICT.values():
        p = item["properties"]
        if is_palindrome is not None and p["is_palindrome"] != is_palindrome:
            continue
        if min_length is not None and p["length"] < min_length:
            continue
        if max_length is not None and p["length"] > max_length:
            continue
        if word_count is not None and p["word_count"] != word_count:
            continue
        if contains_character and contains_character not in item["value"]:
            continue
        results.append(item)

    filters_applied = {k: v for k, v in {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character
    }.items() if v is not None}

    return {
        "data": results,
        "count": len(results),
        "filters_applied": filters_applied
    }


@app.get("/strings/filter-by-natural-language")
def filter_by_natural_language(query: str = Query(...)):
    q = query.lower()
    filters = {}

    if "palindrom" in q:
        filters["is_palindrome"] = True
    if "single word" in q or "one word" in q:
        filters["word_count"] = 1
    if "longer than" in q:
        num = int(re.findall(r"\d+", q)[0])
        filters["min_length"] = num + 1
    if "contain" in q:
        match = re.search(r"letter\s+([a-z])", q)
        if match:
            filters["contains_character"] = match.group(1)

    if not filters:
        raise HTTPException(status_code=400, detail="Unable to parse natural language query")

    # Reuse the main filtering logic
    return get_strings_filtered(**filters) | {
        "interpreted_query": {
            "original": query,
            "parsed_filters": filters
        }
    }



@app.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str):
    """
    Delete a string
    """
    hashed_string = generate_sha256_hash_string(string_value)
    if STRING_DICT.pop(hashed_string, None) is None:
        raise HTTPException(status_code=404, detail="String does not exist in the system")
