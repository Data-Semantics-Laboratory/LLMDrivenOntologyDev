# Summerizing and Populating the ontologies using LLMs

## Overview
This repository contains Python scripts for summarizing large text files of individual enslaved persons, crawled from Wikipedia, and using these summaries to populate two ontologies: Wikibase and Enslaved.
1. **enslaved_summary.py** - Generates structured and holistic summaries of input text files.
2. **enslaved_population.py** - Populates ontology modules based on the extracted summaries.

## Installation
To use these scripts, ensure you have Python installed along with the required dependencies. Install OpenAI's Python library if not already installed:

```sh
pip install openai
```

## Usage

### 1. Generating Summaries
The `enslaved_summary.py` script processes the text files and generates structured summaries based on predefined ontology modules.

#### **Running the script:**
```sh
python enslaved_summary.py
```
#### **Inputs:**
- A folder containing text files (`Absalom Jones.txt`) to be processed.
- A module file defining relevant ontology relationships (`Enslaved_Schema_Relationships.txt`).

#### **Outputs:**
- Summarized files stored in the `EnslavedOntoLLM/summaries` directory.

### 2. Populating Ontology Modules
The `enslaved_population.py` script extracts structured knowledge from the summaries and maps it to ontology relationships.

#### **Running the script:**
```sh
python enslaved_population.py
```
#### **Inputs:**
- Summarized text files from `EnslavedOntoLLM/summaries`.
- A module file with ontology schema relationships (`Enslaved_Schema_Relationships.txt`).

#### **Outputs:**
- Ontology-populated text files stored in `EnslavedOntoLLM/responses`.

## Configuration
Both scripts require an OpenAI API key. Set your API key in the scripts:
```python
client = OpenAI(api_key="YOUR_API_KEY")
```


## Example Summary Output Format
```
The text provides information about Absalom Jones, who was born on November 7, 1746, and died on February 13, 1818. [...]
```

## Example Ontology Output Format
```
hasNameVariant(Absalom Jones, "Absalom Jones")
hasBirthDate(Absalom Jones, "November 7, 1746")
isRelationshipTo(Absalom Jones, "Mr. Wynkop")
```

## Contact
For queries or contributions, feel free to open an issue or submit a pull request.

---
**Developed by:** Adrita

