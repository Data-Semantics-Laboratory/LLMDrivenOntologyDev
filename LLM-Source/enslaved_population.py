#Populate the ontology
import os
import openai
import time

# Define your OpenAI API key
api_key = ""
openai.api_key = api_key

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
    response_file_path = os.path.join("EnslavedOntoLLM/responses", f"{os.path.splitext(file_name)[0]}_response.txt")
    with open(response_file_path, "w", encoding="utf-8") as response_file:
        response_file.write(response_text)

# Main function to process text files and generate summaries
def process_text_files(folder_path, module_file_path):
    # Create the responses folder if it doesn't exist
    os.makedirs("EnslavedOntoLLM/responses", exist_ok=True)

    # Read module file content
    with open(module_file_path, "r", encoding="utf-8") as module_file:
        module_content = module_file.read()
        
    # Define the query prompt
    query = f""" Populate the ontology modules based on the information given in the text file, follwoing the example format. Use the keywords used to describe the relations in the example format.
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
    folder_path = "/Users/ngautam/Desktop/LLMOnto/Untitled/Mini-Files"

    # Path to the module file containing relevant information
    module_file_path = "/Users/ngautam/Desktop/LLMOnto/Untitled/LLM-Source/Enslaved_Schema_Relationships.txt"

    # Process text files and generate summaries
    process_text_files(folder_path, module_file_path) 