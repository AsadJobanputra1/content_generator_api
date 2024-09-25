import openai
import os, json
from content_generator import Article
from pydantic import ValidationError
from flask import Flask, abort
from pydantic import BaseModel, ConfigDict

# Fetch configuration from environment variables with defaults
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 1500))  # Default to 1500 if not set
ENGINE = os.getenv('OPENAI_MODEL', 'text-davinci-003')  # Default to 'text-davinci-003' if not set
TEMPERATURE = 0.5
NUM_CHOICES = 1

def edit_article(article, guidance=''):

        # parse article into article object, if parsing fails reutrn an error
    try:
        # Parse the JSON string into a dictionary
        #data = json.loads(article)
        # Create an Article object from the dictionary
        article = Article(**article)
    except json.JSONDecodeError as json_err:
        abort( 400, description = f"Error decoding JSON: {json_err}")
    except ValidationError as val_err:
        abort( 400, description = f"Validation error: {val_err}")

    # Create a chat client
    reviewer_conversation=[
            {
                "role": "system",
                "content": f"""
                You are an editor for the new york times newspaper.  You pay close attention to content style.
                Your target audience has a grade 6 reading level, and has a technical background.
                Your content is written in an informative and interesting way that captures the readers' interest.

                you will be provided a section of an article with feedback from the article.  Use the feedback to reflect on the existing content and find ways to re-write the section in a better way.

                please consider this additional guidance:
                {guidance}
                """
            }
    ]

    class Section_content_final (BaseModel):
       section_final_draft:str

    client = openai.Client(api_key=os.getenv('OPENAPI_KEY') )
    
    for s in article.sections:
        feedback_prompt= reviewer_conversation 
        feedback_prompt.append(
                {
                    "role": "user",
                    "content": f"""

                    You are reviewing a document, provide helpful feedback on the document.  You will be presented with three drafts for each section.
                    describe which one you think is the best, and provide comments and feedback on the document.

                    this is the description of the response parameters:
                    - section_content_final: final content after reviewing section content for easy_reading, section_content, and informative version; as well as feedback on all content drafts

                    #title: {article.title}
                    #objective: {article.summary}
        
                    #section: {s.section_name}
                    #content option : section_content: 
                    {s.section_content}
                    #content option : easy_reading: 
                    {s.easy_reading}
                    #content option: informative_version: 
                    {s.informative_version}

                    # feedback on content drafts:
                    {s.feedback}
        """
                }
            )


        # Start the chat with the initial prompt
        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=feedback_prompt, # type: ignore
            response_format=Section_content_final
        )
        
        finaldraft = response.choices[0].message.parsed
        s.section_content_final = finaldraft.section_final_draft


    return article.model_dump()