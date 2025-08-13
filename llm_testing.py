import asyncio
import json
import random
import time

from pathlib import Path
from string import ascii_lowercase
from typing import Coroutine, TypedDict

from pydantic import BaseModel
import openai
from openai.types.responses import ParsedResponse, ResponseOutputRefusal

_ascii_lowercase: set[str] = set(ascii_lowercase)

CLIENT = openai.AsyncOpenAI()
SAMPLES_DEFAULT: int = 100
SLEEP_TIME: float = (60/500) * 1.5  # seconds, ~180ms, ~333 RPM

class ExperimentData(TypedDict):
    refusals: list[tuple[str, str, str]]
    successes: list[tuple[str, str, int]]

class ExperimentResult(TypedDict):
    type: str
    result: str | tuple[str, str, int] | tuple[str, str, str]
    
class LetterCount(BaseModel):
    count: int


async def one_trial(word: str, letter: str) -> ExperimentResult:
    try:
        response = await CLIENT.responses.parse(
            model="gpt-5-2025-08-07",
            instructions=f"Count the total occurrences of the letter '{letter}' in the provided word.",
            input=f"{word}",
            text_format=LetterCount,
            reasoning={
                "effort": "minimal"
            }
        )
        if isinstance(response, ResponseOutputRefusal):
            return ExperimentResult(
                type="refusal",
                result=(word, letter, response.refusal)
            )
        elif isinstance(response, ParsedResponse) and isinstance(response.output_parsed, LetterCount):
            return ExperimentResult(
                type="success",
                result=(word, letter, response.output_parsed.count)
            )
        return ExperimentResult(
            type="error",
            result=(word, letter, f"Unexpected response type {type(response)}")
        )
    except Exception as e:
        return ExperimentResult(type="error", result=(word, letter, str(e)))


async def main(samples: int = SAMPLES_DEFAULT):
    words: list[str] = _load_dictionary()
    data: ExperimentData = ExperimentData(refusals=[], successes=[])
    
    sem = asyncio.Semaphore(10)  # Limit concurrent requests
    async def bound_trial():
        async with sem:
            w = random.choice(words)
            l = pick_letter(w)
            return await one_trial(w, l)
        
    tasks = [asyncio.create_task(bound_trial()) for _ in range(SAMPLES_DEFAULT)]
    results = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results):
        print(f"Collecting result {str(i + 1).rjust(6)}/{SAMPLES_DEFAULT}...", end='\r')
        if result["type"] == "refusal":
            data["refusals"].append(result["result"]) # type: ignore
        elif result["type"] == "success":
            data["successes"].append(result["result"]) # type: ignore
        else:
            print(f"\nError in trial {i + 1}: {result['result']}")
    
    Path("results").mkdir(exist_ok=True)
    with open(Path("results") / f"{int(time.time())}.json", "w") as file:
        json.dump(data, file)
        
        
def pick_letter(word: str) -> str:
    while (letter := random.choice(word)) not in _ascii_lowercase:
        pass
    return letter


def _load_dictionary() -> list[str]:
    import json
    with open("words_dictionary.json", "r") as file:
        loaded = json.load(file)
    if not isinstance(loaded, dict):
        raise ValueError
    loaded: dict[str, int]
    return sorted(word.lower() for word in loaded.keys())


def run_test(sample_count: int = SAMPLES_DEFAULT):
    asyncio.run(main(samples=sample_count))
