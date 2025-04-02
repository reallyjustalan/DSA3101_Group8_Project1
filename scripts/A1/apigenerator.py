import pandas as pd
import seaborn as sns
import configurations as c
from google import genai
from pydantic import BaseModel
from typing import List, Optional
import prompt
import tqdm
import time

class CodedElement(BaseModel):
    touchpoint: str
    sentiment: str # "positive" or "negative" or "neutral"
    code: str
    text_excerpt: str

class DemographicInfo(BaseModel):
    travel_party: Optional[str] = None
    first_visit: Optional[str] = None # "Yes", "No", or "Unknown"
    visit_timing: Optional[str] = None # Season, holiday, time of day, day of week

class ReviewAnalysis(BaseModel):
    review_id: str
    coded_elements: List[CodedElement]
    demographic_info: DemographicInfo


#if you want to run this yourself, create a configurations.py file with the following content:
# GEMINI = your_gemini_api_key

secret = c.GEMINI
client = genai.Client(api_key = secret)
def chatgpt(input):
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=input,
        config={
            'response_mime_type': 'application/json',
            'response_schema': ReviewAnalysis,
            'system_instruction': prompt.prompt() 
        },
    )
    return response.text


def process_inputs(inputs, delay=0): #rate limit in seconds
    """
    Processes a list of inputs using the chatgpt function, with a progress bar and rate limiting.

    Args:
        inputs: A list of inputs to process.
        delay:  The number of seconds to wait between API calls (rate limiting). Defaults to 1 second.
    Returns:
        A list of results from the chatgpt function.
    """
    results = []
    for i in tqdm.tqdm(range(len(inputs)), desc="Processing Inputs"):  # Initialize progress bar
        input_item = inputs[i]
        try:
            result = chatgpt(input_item)
            results.append(result)
        except Exception as e:
            print(f"Error processing input {i+1}: {e}")
            results.append(None)  # Or handle the error differently
    time.sleep(delay)  # Rate limiting: Wait before the next request
    return results


