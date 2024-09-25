import openai, json, os
from content_generator import Article
from pydantic import ValidationError
from flask import Flask, abort
from pydantic import BaseModel, ConfigDict
    
def analyze_article(article, persona='', persona_concerns='', job_description=''):

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
                    You are a content reviewer
                    Your are a helpful {persona}.

                    your job description includes:
                    {job_description}

                    your top concerns are:
                    {persona_concerns}
                """
            }
    ]

    class Section_feedback(BaseModel):
        section_name : str
        best_content : str
        feedback : str
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
                    - section_name : the name of the section
                    - best_content : best content that was preferred from the available options
                    - feedback : suggestions on how to write the feedback

                    #title: {article.title}
                    #objective: {article.summary}
        
                    #section: {s.section_name}
                    #content option : easy_reading: 
                    {s.easy_reading}
                    #content option : section_content: 
                    {s.section_content}
                    #content option: informative_version: 
                    {s.informative_version}
        """
                }
            )


        # Start the chat with the initial prompt
        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=feedback_prompt, # type: ignore
            response_format=Section_feedback
        )
        
        feedback = response.choices[0].message.parsed
        s.feedback = feedback.feedback # type: ignore


    return article.model_dump()
