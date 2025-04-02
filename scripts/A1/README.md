# Disney Review Analysis System - Technical Documentation

This document provides a comprehensive overview of the Disney Review Analysis System, which extracts structured insights from theme park reviews using Google's Gemini AI models.

## System Overview

The system analyzes Disneyland reviews to identify key drivers of guest satisfaction across the entire guest journey. It uses two main processing pipelines:

1. **LLM Analysis Pipeline**: Uses Gemini-2.0-Flash to extract structured touchpoints, sentiments, and demographic information from reviews
2. **RAG (Retrieval-Augmented Generation) Pipeline**: Creates embeddings of the extracted insights for clustering and semantic search

## System Architecture

```
┌─────────────────┐     ┌───────────────┐     ┌──────────────────┐
│  Disney Review  │────▶│ Data Cleaning │────▶│ LLM Analysis     │
│  Dataset (CSV)  │     │ & Sampling    │     │ (Gemini-2.0-Flash)│
└─────────────────┘     └───────────────┘     └──────────────────┘
                                                      │
                                                      ▼
┌─────────────────┐     ┌───────────────┐     ┌──────────────────┐
│  Enriched       │◀────│ Structured    │◀────│ JSON Response    │
│  Dataset with   │     │ DataFrame     │     │ Processing       │
│  Embeddings     │     │ Conversion    │     │                  │
└─────────────────┘     └───────────────┘     └──────────────────┘
         ▲
         │
┌────────┴────────┐
│ RAG Embedding   │
│ Generation      │
│ (Gemini-embed)  │
└─────────────────┘
```

## Main Execution Scripts

The system has two main scripts that should be run in sequence:

### 1. llm_generator.py

This script orchestrates the first phase of analysis:

```bash
python llm_generator.py  # First run this
```

**What it does:**
- Loads and cleans the original Disneyland reviews dataset
- Samples 1000 reviews for analysis
- Formats each review for Gemini API submission
- Processes reviews through Gemini-2.0-Flash using a detailed prompt
- Extracts structured touchpoints, sentiments, and demographic information
- Converts the API responses to a structured DataFrame
- Saves the analysis as "DisneylandReviews_Coded.csv"

### 2. rag_generator.py

This script performs the embedding generation for semantic analysis:

```bash
python rag_generator.py  # Run this after llm_generator.py completes
```

**What it does:**
- Loads the coded review data from "DisneylandReviews_Coded.csv"
- Creates rich text representations for each touchpoint and code
- Generates semantic embeddings using Gemini-embedding-exp-03-07 model
- Implements batch processing with exponential backoff for API rate limits
- Saves progress periodically during the embedding process
- Outputs the final embedded dataset as "DisneylandReviews_Embedded.csv"

## Core Component Modules

### apigenerator.py

Handles API interaction and defines the data schema:

- Implements Pydantic models for structured data validation (CodedElement, DemographicInfo, ReviewAnalysis)
- Configures the Gemini API client
- Contains the core function for making API calls
- Provides batch processing capabilities with progress tracking and rate limiting

### dfhelper.py

Utility module for data manipulation:

- Cleans and preprocesses the Disneyland reviews dataset
- Provides functionality for random sampling with reproducible results
- Converts API JSON responses to a structured DataFrame following the Pydantic schema

### prompt.py

Contains the detailed system instructions for the Gemini AI model:

- Defines the analysis objectives
- Specifies the guest journey touchpoint categories
- Provides guidelines for coding guest sentiments
- Sets expectations for capturing demographic information
- Contains examples to guide the model's analysis

### configurations.py

Configuration file storing API credentials:

- Contains the Gemini API key (you'll need to create your own)

## Data Models

The system uses Pydantic models to validate and structure the data:

- **CodedElement**: Represents a specific touchpoint mention
  - touchpoint: The category (staff, attractions, etc.)
  - sentiment: positive/negative/neutral
  - code: A specific descriptive code (3-5 words)
  - text_excerpt: The exact text from the review

- **DemographicInfo**: Captures visitor demographics
  - travel_party: Family, couple, solo, friends
  - first_visit: Yes/No/Unknown
  - visit_timing: Season, holiday, time of day, day of week

- **ReviewAnalysis**: The top-level model
  - review_id: Unique identifier for the review
  - coded_elements: List of CodedElement instances
  - demographic_info: DemographicInfo instance

## Setup Instructions

1. Clone this repository
2. Install required packages:
   ```
   pip install pandas seaborn google-generativeai pydantic tqdm numpy
   ```
3. Create a `configurations.py` file with your Gemini API key:
   ```python
   GEMINI = 'your_api_key_here'
   ```
4. Ensure the Disneyland review dataset is in the correct path
5. Run the main scripts in sequence:
   ```
   python llm_generator.py
   python rag_generator.py
   ```

## Output Files

- **DisneylandReviews_Sample.csv**: 1000-review sample from the original dataset
- **DisneylandReviews_Coded.csv**: Reviews analyzed with touchpoints and sentiments
- **DisneylandReviews_Embedded_progress_*.csv**: Checkpoint files during embedding generation
- **DisneylandReviews_Embedded.csv**: Final dataset with embeddings for semantic analysis

## API Usage Notes

- Both scripts implement rate limiting and error handling for Gemini API
- The RAG generator includes exponential backoff to handle API rate limits
- Progress tracking and periodic saves ensure resilience against failures