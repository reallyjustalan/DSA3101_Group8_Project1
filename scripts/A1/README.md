# Disney Review Analysis System - Technical Documentation

This document explains the architecture and functioning of the Disney Review Analysis System, which uses Google's Gemini 2.0 Flash API to extract structured insights from theme park reviews.

## System Architecture Overview

The system consists of several Python modules that work together to process and analyze Disneyland reviews:

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│ Input Data  │────▶│ Data Cleaning │────▶│ API Request  │
└─────────────┘     └───────────────┘     └──────────────┘
                                                 │
┌─────────────┐     ┌───────────────┐            ▼
│ Final CSV   │◀────│ JSON to       │◀────┌──────────────┐
│ Output      │     │ DataFrame     │     │ API Response │
└─────────────┘     └───────────────┘     └──────────────┘
```

## Core Components

### 1. llm_generator.py

This is the main orchestration script that ties all components together:

The script:
1. Loads and cleans the original Disney reviews dataset
2. Takes a random sample of 1000 reviews
3. Saves this sample as a CSV file
4. Formats each review for API submission
5. Processes reviews through the API
6. Transforms API responses into a structured dataframe
7. Saves the final analysis as a CSV

### 2. apigenerator.py
This module handles the API interaction and defines the data schema:

Key functions:
- Defines Pydantic models for structured data validation
- Sets up the Gemini API client
- Makes API calls with properly formatted prompts
- Handles batch processing with progress tracking

### 3. dfhelper.py

This utility module handles data manipulation:

Key functions:
- Data cleaning and preprocessing
- Random sampling with seed for reproducibility
- Converting API JSON responses to a structured dataframe

### 4. configurations.py

A simple configuration file that stores the Gemini API key. If you want to run this, make your own configurations.py:

```python
GEMINI = #your API key here
```

### 5. prompt.py

Contains the system instructions for the Gemini AI model:

The prompt:
- Defines the structure and categories for analysis
- Provides detailed guidelines for coding and categorization
- Sets expectations for output format
- Contains examples to guide the model

## Data Flow

1. **Raw Data Input**: The system starts with a CSV file containing Disney reviews
2. **Data Preparation**: Reviews are cleaned and sampled
3. **API Submission**: Each review is formatted and sent to the Gemini API
4. **AI Analysis**: The API processes each review according to the prompt instructions
5. **Response Processing**: JSON responses are validated and structured
6. **Output Generation**: All analyzed reviews are combined into a final CSV output

