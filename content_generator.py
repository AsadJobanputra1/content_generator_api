# prompt: create an openai client and start a thread.  initial prompt should be: 'you are a sales director, specializing in creating persuasive proposals'

import openai, json, os 
from pydantic import BaseModel, ConfigDict

class Article(BaseModel):

        class Section(BaseModel):
            section_name: str
            section_content: str
            easy_reading: str
            informative_version: str
            feedback: str
            section_content_final: str

        sections: list[Section]
        title: str
        summary: str
        objective: str
        description: str

def generate_article(topic,
                     target_audience='',
                     audience_questions='',
                     purpose='',
                     detail_info='',
                     length='500 words',
                     style='informative'):
    # Create a chat client
    client = openai.Client(
    api_key=os.getenv('OPENAPI_KEY') )
    conversation = [{
        "role":"system",
        "content":
        f"""
                    You are a marketing content writer.
                    You are tasked with creating a persuasive and engaging content for a marketing campaign.

                    Your target market is: {target_audience}

                    The audience often has questions about:
                    {audience_questions}
                     """
    }]

    # Start the chat with the initial prompt
    response = client.beta.chat.completions.parse(  # original non-beta version ). .chat.completions.create(
        model = os.getenv('OPENAI_MODEL', 'gpt-4o-2024-08-06'),  # Default to 'gpt-4o-2024-08-06' if not set
        messages=conversation) # type: ignore
    
    print(response.choices[0].message.content)

    conversation.append({
        "role": "user",
        "content":
        f"""

    The purpose and tone of the article is:
    {purpose}
    
    Write an article on the topic of:
    {topic}
    
    Be sure that the article also discusses the following details:
    *************************
    {detail_info}
    *********************

    here is a description of the parameters: 
            - title : title of the article
            - summary: summary of the article in 2 paragraphs
            - objective: description of next action we want the reader to take after reading the article.  describe what the article is trying to achieve.
            - sections: an array of all the sections within the article, this is the headings within the article.
            
            - section name: the heading title of the section
            - section_content: provide initial version of content for the sections
            - easy_reading: alternative explaination that uses simpler words for a grade 6 reading level.  Do Not reduce the original intent of the original content.
            - informative_version: re-write the article with the intent to inform, and have the reader ask more questions. Adds some curiousity and personality to the content.
            - feedback: keep this blank for now
            - section_content_final: keep this blank for now
        """
    })

    
    # Start the chat with the initial prompt
    response = client.beta.chat.completions.parse(  #).create(
        model= os.getenv('OPENAI_MODEL', 'gpt-4o-2024-08-06'),  # Default to 'gpt-4o-2024-08-06' if not set
        messages=conversation, # type: ignore
        response_format=Article,  # new, let the response be a class ; ask for output in json_object mode.
    )

    print(response.choices[0].message.content)
    article = object  # base version must be a regular object that can be manipulated and updated as the article is processed.
    article = response.choices[0].message.parsed
    print(article.model_dump())
    return article.model_dump() # type: ignore
