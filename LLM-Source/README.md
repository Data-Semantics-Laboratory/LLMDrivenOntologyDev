# Summarizing and Populating Ontologies using LLMs  

## Overview  
This repository contains Python scripts for summarizing large text files of individual enslaved persons, crawled from Wikipedia, and using these summaries to populate two ontologies: **Wikibase** and **Enslaved**.  
We used two methods for this purpose: **Text Summarization** and **RAG**

## Text Summarization :
### Scripts:  
- **`enslaved_summary.py`** - Generates structured and holistic summaries for the Enslaved ontology.  
- **`enslaved_population.py`** - Populates the Enslaved ontology modules using extracted summaries.  
- **`wb_summary.py`** - Generates structured and holistic summaries for the Wikibase ontology.  
- **`wb_population.py`** - Populates the Wikibase ontology modules using extracted summaries.  

## Installation  
Ensure Python is installed, along with the required dependencies. Install OpenAI's Python library if not already installed:  

```sh
pip install openai
```

## Usage  

### Generating Summaries  

#### **For Enslaved Ontology**  
The `enslaved_summary.py` script processes text files and generates structured summaries based on predefined ontology modules.  

**Running the script:**  
```sh
python enslaved_summary.py
```  
**Inputs:**  
- A folder containing text files (e.g., `Absalom Jones.txt`) to be processed.  
- A module file defining relevant ontology relationships (`Enslaved_Schema_Relationships.txt`).  

**Outputs:**  
- Summarized files stored in the `EnslavedOntoLLM/summaries` directory.  

#### **For Wikibase Ontology**  
The `wb_summary.py` script performs the same function as `enslaved_summary.py`, but for the Wikibase ontology.  

**Running the script:**  
```sh
python wb_summary.py
```  
**Inputs:**  
- A folder containing text files (e.g., `Absalom Jones.txt`) to be processed.  
- A module file defining relevant ontology relationships (`WB_Schema_Relationships.txt`).  

**Outputs:**  
- Summarized files stored in the `WBOntoLLM/summaries` directory.  

### Populating Ontology Modules  

#### **For Enslaved Ontology**  
The `enslaved_population.py` script extracts structured knowledge from the summaries and maps it to ontology relationships.  

**Running the script:**  
```sh
python enslaved_population.py
```  
**Inputs:**  
- Summarized text files from `EnslavedOntoLLM/summaries`.  
- A module file with ontology schema relationships (`Enslaved_Schema_Relationships.txt`).  

**Outputs:**  
- Ontology-populated text files stored in `EnslavedOntoLLM/responses`.  

#### **For Wikibase Ontology**  
The `wb_population.py` script performs the same function as `enslaved_population.py`, but for the Wikibase ontology.  

**Running the script:**  
```sh
python wb_population.py
```  
**Inputs:**  
- Summarized text files from `WBOntoLLM/summaries`.  
- A module file with ontology schema relationships (`WB_Schema_Relationships.txt`).  

**Outputs:**  
- Ontology-populated text files stored in `WBOntoLLM/responses`.  

## Configuration  
All scripts require an OpenAI API key. Set your API key in the scripts:  

```python
client = OpenAI(api_key="YOUR_API_KEY")
```

## Example Outputs  

### **Summary Output Format**  
```
The text provides information about Absalom Jones, who was born on November 7, 1746, and died on February 13, 1818. [...]
```

### **Ontology Output Format**  
#### **For Enslaved Ontology**  
```
Name Record Module:
1. hasNameVariant(Absalom Jones, "Absalom Jones")
2. hasPreferredNameVariant(Absalom Jones, "Absalom Jones")
3. fullNameAsString(Absalom Jones, "Absalom Jones")
4. hasSurnameAsString(Absalom Jones, "Jones")
5. hasFirstnameAsString(Absalom Jones, "Absalom")

```

#### **For Wikibase Ontology**  
```
Name Record Module: 
1. has_Name(Agent, Name): has_Name(Absalom Jones, "Absalom Jones")
2. has_Surname(Agent, Surname): has_Surname(Absalom Jones, "Jones")
3. has_First_Name(Agent, First_Name): has_First_Name(Absalom Jones, "Absalom").
  
```
## RAG: 


## Contact  
For queries or contributions, feel free to open an issue or submit a pull request.  

---

**Developed by:** Adrita  


