# Generate Holistic Summary
import os
import openai

# Define your OpenAI API key
from openai import OpenAI
client = OpenAI(api_key = 'your API key')

# Function to generate summaries based on a query prompt using GPT-4
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
    response = client.chat.completions.create(
        model="gpt-4",  # Choose the gpt-4 model
        messages=[{"role": "user", "content": prompt}],
        temperature=0,  # Adjust the temperature for generating diverse responses
        stop="\n"  # Stop generation at a newline to ensure a concise summary
    )

    # Extract and return the generated summary from the response
    return response.choices[0].message.content.strip()

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
    holistic_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{holistic_query}\n{context}"}],
        temperature=0,  # Adjust the temperature for generating diverse responses
        stop="\n"  # Stop generation at a newline to ensure a concise summary
    )

    # Extract the generated holistic summary from the response
    holistic_summary = holistic_response.choices[0].message.content.strip()

    # Save the holistic summary to a file
    response_file_path = os.path.join("WBOntoLLM/summaries", f"{os.path.splitext(file_name)[0]}_summary.txt")
    with open(response_file_path, "w", encoding="utf-8") as response_file:
        response_file.write(holistic_summary)

# Main function to process text files and generate summaries
def process_text_files(folder_path, module_file_path):
    # Create the responses folder if it doesn't exist
    os.makedirs("WBOntoLLM/summaries", exist_ok=True)

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
    folder_path = "/Users/adrita/Text_files"

    # Path to the module file containing relevant information
    module_file_path = "/Users/adrita/WB_Schema_Relationships.txt"

    # Process text files and generate summaries
    process_text_files(folder_path, module_file_path) 
