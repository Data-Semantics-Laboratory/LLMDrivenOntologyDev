#Populate the ontology
import os
import openai

# Define your OpenAI API key
from openai import OpenAI
client = OpenAI(api_key = 'your API key')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to interact with ChatGPT and ask questions
def populate_ontology(file_name, text_file, module_content, query):
    # Use GPT-4 to populate the ontology modules
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{query}\n{text_file}"}],
        temperature=0,  # Adjust the temperature for generating diverse triples
    )

    # Extract the generated response text from the response
    response_text = response.choices[0].message.content.strip()

    # Save the triples to a file
    response_file_path = os.path.join("WBOntoLLM/triples", f"{os.path.splitext(file_name)[0]}_response.txt")
    with open(response_file_path, "w", encoding="utf-8") as response_file:
        response_file.write(response_text)

# Main function to populate the ontology
def process_text_files(folder_path, module_file_path):
    # Create the triples folder if it doesn't exist
    os.makedirs("WBOntoLLM/triples", exist_ok=True)

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
    folder_path = "/Users/adrita/WBOntoLLM/summaries"

    # Path to the module file containing relevant information
    module_file_path = "/Users/adrita/WBOntoLLM/WB_Schema_Relationships.txt"

    # Process text files and generate summaries
    process_text_files(folder_path, module_file_path) 

