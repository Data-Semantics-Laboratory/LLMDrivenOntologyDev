#!/usr/bin/env python
# coding: utf-8

# In[33]:


# Generate Holistic Summary
import os
import openai

# Define your OpenAI API key
api_key = "your openAI key"
openai.api_key = api_key

# Function to generate summaries based on a query prompt using GPT-3
def generate_summary_with_modules(query, text_chunks, module_file_path):
    # Read module file content
    with open(module_file_path, "r", encoding="utf-8") as module_file:
        module_content = module_file.read()

    summaries = []
    chunk = ""
    for paragraph in text_chunks:
        # Check if adding the next paragraph will exceed the chunk size limit
        if len(chunk) + len(paragraph) <= 7000: #change the chunk size limit based on your text file
            # Add the paragraph to the current chunk
            chunk += paragraph + "\n"
        else:
            # Generate summary for the current chunk
            summary = generate_summary(query, chunk, module_content)
            summaries.append(summary)
            # Start a new chunk with the current paragraph
            chunk = paragraph + "\n"

    # Generate summary for the remaining chunk, if any
    if chunk:
        summary = generate_summary(query, chunk, module_content)
        summaries.append(summary)

    return summaries

# Function to generate summary for a single chunk
def generate_summary(query, chunk, module_content):
    # Concatenate the query, text chunk, and module content as input
    prompt = f"""{query},by keeping the relevant information from these modules (if any):
    {module_content}.
    The birth and death dates are mentioned in parenthesis after the agent name. For example : Joseph Vance Lewis (December 25, 1853 – April 24, 1925), was a slave who was freed. Here the Birth date is December 25, 1853 and Death date is April 24, 1925. So keep those informations in the summery.
    The given text to summarize:{chunk}"""

    # Use GPT-4 to generate summary
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Choose the gpt-4 model
        messages=[{"role": "user", "content": prompt}],
        temperature=0,  # Adjust the temperature for generating diverse responses
        stop="\n"  # Stop generation at a newline to ensure a concise summary
    )

    # Extract and return the generated summary from the response
    return response["choices"][0]["message"]["content"]

# Function to read input text from file and split into paragraphs
def read_text_and_split_into_paragraphs(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    # Split text into paragraphs
    paragraphs = text.split("\n")
    return paragraphs

# Function to generate holistic summary for a text file
def generate_holistic_summary(file_name, context, module_content, holistic_query):
    # Use GPT-4 to generate a holistic summary
    holistic_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{holistic_query}\n{context}"}],
        temperature=0,  # Adjust the temperature for generating diverse responses
        stop="\n"  # Stop generation at a newline to ensure a concise summary
    )

    # Extract the generated holistic summary from the response
    holistic_summary = holistic_response.choices[0].message.content.strip()

    # Save the holistic summary to a file
    response_file_path = os.path.join("OntoLLM/summaries", f"{os.path.splitext(file_name)[0]}_summary.txt")
    with open(response_file_path, "w", encoding="utf-8") as response_file:
        response_file.write(holistic_summary)

# Main function to process text files and generate summaries
def process_text_files(folder_path, module_file_path):
    # Create the responses folder if it doesn't exist
    os.makedirs("OntoLLM/summaries", exist_ok=True)

    # Define your query prompt
    query = "Summarize the following text"

    # Read module file content
    with open(module_file_path, "r", encoding="utf-8") as module_file:
        module_content = module_file.read()

    # Define the query prompt for the holistic summary
    holistic_query = f"""Here is an example summary that highlights the key points from a text file based on the given module. The text file discusses a single agent or person who is introduced initially. So, the summary should focus solely on that particular agent. The birth and death dates are mentioned in parenthesis after the agent name. For example : Joseph Vance Lewis (December 25, 1853 – April 24, 1925), was a slave who was freed. Here the Birth date is December 25, 1853 and Death date is April 24, 1925. The Interagent Relationship Record Module describes whether the agent has a relationship with another Enslaver or Owner. The Person Status Module indicates whether the agent is an enslaved person and mentions any status-generating events.

                    Example summary: The text provides information about Joseph Vance Lewis, who was born on December 25, 1853, and died on April 24, 1925. From the Name Record Module, his first name is Joseph, surname is Lewis, and he doesn't have an alternate name mentioned. The Interagent Relationship Record Module doesn't apply as no other agent who is an enslaver or owner is mentioned. The Participant Role Record Module doesn't apply as he was not a participant in any event. The Sex Record Module identifies him as male. From the Occupation Record Module, his occupation was a slave, educator, lawyer, and autobiographer. The Age Record Module indicates he was born on December 25, 1853, and died on April 24, 1925. So, his age was 72. The Race Record Module and Ethnolinguistic Descriptor Record Module are not explicitly mentioned in the text. From the Person Status Record Module, he was an enslaved person and was sold during the Sale of estate of Joseph Dubreuil, indicating the status-generating event. His status changed from being a slave to a lawyer, with emancipation being the status-generating event.

                    Please provide a holistic summary from the given text that follows the format of the example summary and keeps the relevant information from these modules (if any): 
                    {module_content}. 
                    The given text is: """
    # Iterate over text files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            # Path to the current text file
            text_file_path = os.path.join(folder_path, file_name)

            # Read input text from file and split into paragraphs
            paragraphs = read_text_and_split_into_paragraphs(text_file_path)

            # Generate summaries based on the query prompt, input text paragraphs, and module file
            summaries = generate_summary_with_modules(query, paragraphs, module_file_path)

            # Concatenate all individual summaries into context for generating holistic summary
            context = "\n".join(summaries)

            # Generate and save holistic summary for the current text file
            generate_holistic_summary(file_name, context, module_content, holistic_query)

            print(f"Holistic summary generated and saved for {file_name}")

# Example usage
if __name__ == "__main__":
    # Path to the folder containing input text files
    folder_path = "/Users/adrita/Downloads/OntoLLM/Text_files"

    # Path to the module file containing relevant information
    module_file_path = "/Users/adrita/Downloads/OntoLLM/WB_Schema_Relationships.txt"

    # Process text files and generate summaries
    process_text_files(folder_path, module_file_path) 


# In[48]:


#Populate the ontology
import os
import openai

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to interact with ChatGPT and ask questions
def populate_ontology(file_name, text_file, module_content, query):
    # Use GPT-4 to populate the ontology modules
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{query}\n{text_file}"}],
        temperature=0,  # Adjust the temperature for generating diverse responses
    )

    # Extract the generated response text from the response
    response_text = response.choices[0].message.content.strip()

    # Save the holistic summary to a file
    response_file_path = os.path.join("OntoLLM/responses", f"{os.path.splitext(file_name)[0]}_response.txt")
    with open(response_file_path, "w", encoding="utf-8") as response_file:
        response_file.write(response_text)

# Main function to process text files and generate summaries
def process_text_files(folder_path, module_file_path):
    # Create the responses folder if it doesn't exist
    os.makedirs("OntoLLM/responses", exist_ok=True)

    # Read module file content
    with open(module_file_path, "r", encoding="utf-8") as module_file:
        module_content = module_file.read()
        
    # Define the query prompt
    query = f""" Populate the ontology modules based on the information given in the text file, follwoing the example format. Use the keywords used to describe the relations in the example format.
            Example format:
            Name Record Module: 
            1. has_Name(Agent, Name): has_Name(Joseph Vance Lewis, "Joseph Vance Lewis")
            2. has_Surname(Agent, Surname): has_Surname(Joseph Vance Lewis, "Lewis")
            3. has_First_Name(Agent, First_Name): has_First_Name(Joseph Vance Lewis, "Joseph").
            
            Interagent Relationship Record Module:
            1. has_Interagent_Relationship_Type_To(Agent, Relationship_Type): has_Interagent_Relationship_Type_To(Joseph Vance Lewis, "Enslaver or Owner") 
            2. is_Relationship_To(Agent, Agent): is_Relationship_To(Joseph Vance Lewis, "Bwril Nate").
            Note: The Interagent Relationship Record Module describes the relationship to another agent who is an enslaver or owner. So use the keywords Enslaver or Owner to describe the relationship type. 
            
            Sex Record Module:
            1. has_Sex(Agent, Sex_Type): has_Sex(Joseph Vance Lewis, "Male").
            
            Occupation Record Module: 
            1. has_Occupation(Agent, Occupation): has_Occupation(Joseph Vance Lewis, "Slave, Educator, Lawyer, and Autobiographer").

            Age Record Module: 
            1. has_Age(Agent, Age): has_Age(Joseph Vance Lewis, 72)
            2. has_BirthDate(Agent, Date_of_Birth): has_BirthDate(Joseph Vance Lewis, "December 25, 1853")
            3. has_DeathDate(Agent, Date_of_Death): has_DeathDate(Joseph Vance Lewis, "April 24, 1925").

            Person Status Record Module: 
            1. has_Person_Status (Agent, Person_Status): has_Person_Status(Joseph Vance Lewis, "Enslaved Person, Lawyer")
            2. has_Status_Generating_Event(Person_Status, Event): has_Status_Generating_Event(Enslaved Person, "Sale of estate of Joseph Dubreuil"), has_Status_Generating_Event(Lawyer, "Emancipation")
            3. recorded_At(Person_Status_information, Event): recorded_At(Enslaved Person, "Sale of estate of Joseph Dubreuil"), recorded_At(Lawyer, "Emancipation").
            Note: Skip the relations for which there is no information listed in the text file.
            The given ontology modules: 
            {module_content}.
            The given text file is:"""

    # Iterate over text files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            # Path to the current text file
            text_file_path = os.path.join(folder_path, file_name)
            
            # Read input text from file
            text_file = read_text_file(text_file_path)
            
            # Generate and save response for the current text file
            populate_ontology(file_name, text_file, module_content, query)
            
            print(f"The response is generated and saved for {file_name}")


# Example usage
if __name__ == "__main__":
    # Path to the folder containing input text files
    folder_path = "/Users/adrita/Downloads/OntoLLM/summaries"

    # Path to the module file containing relevant information
    module_file_path = "/Users/adrita/Downloads/OntoLLM/WB_Schema_Relationships.txt"

    # Process text files and generate summaries
    process_text_files(folder_path, module_file_path) 

