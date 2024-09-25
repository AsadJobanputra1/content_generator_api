# prompt: create an openai client and start a thread.  initial prompt should be: 'you are a sales director, specializing in creating persuasive proposals'

import openai, json, os 
from content_generator import Article
from pydantic import ValidationError
from flask import Flask, abort
from pydantic import BaseModel, ConfigDict


def getmarkdown_article(article):
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

    # construct the article
    content = f"# {article.title } <br/>"
    content += f"\n# Summary: {article.summary } \n"
    for s in article.sections:
        content += f"\n# {s.section_name} \n"
        content += f"{s.section_content_final} \n\n"

    print(json.dumps({"content": f"```markdown\n{content}\n```"}))
    return {"content":f"```markdown\n{content}\n```"} # type: ignore
