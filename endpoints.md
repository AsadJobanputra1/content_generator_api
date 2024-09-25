Here is the markdown documentation of the API endpoints, which you can save as a `.md` file:

---

# API Endpoints Documentation

This document provides detailed descriptions of the REST API endpoints related to article generation and manipulation, using the `Article` object structure defined earlier.

---

## Table of Contents

1. [Endpoint Overview](#endpoint-overview)
2. [Common Data Structures](#common-data-structures)
3. [Endpoints](#endpoints)
   - [Generate Article](#1-generate-article)
   - [Provide Feedback](#2-provide-feedback)
   - [Edit Article](#3-edit-article)
   - [Get Markdown Article](#4-get-markdown-article)
4. [Example Usage](#example-usage)
5. [Error Responses](#error-responses)
6. [Conclusion](#conclusion)

---

## Endpoint Overview

| Endpoint                      | Method | Description                                             |
|-------------------------------|--------|---------------------------------------------------------|
| `/server/generate_article`    | `POST` | Generates an article based on provided parameters.      |
| `/server/provide_feedback`    | `POST` | Provides feedback on an article from a persona's perspective. |
| `/server/edit_article`        | `POST` | Edits an article based on provided guidance.            |
| `/server/getmarkdown_article` | `POST` | Retrieves the article content in Markdown format.       |

---

## Common Data Structures

### Article Object

The `Article` object is a structured representation of an article that includes multiple sections.

#### JSON Structure

```json
{
  "title": "string",
  "summary": "string",
  "objective": "string",
  "description": "string",
  "sections": [
    {
      "section_name": "string",
      "section_content": "string",
      "easy_reading": "string",
      "informative_version": "string",
      "feedback": "string",
      "section_content_final": "string"
    }
    // Additional Section objects
  ]
}
```

---

## Endpoints

### 1. Generate Article

- **URL:** `/server/generate_article`
- **Method:** `POST`
- **Description:** Generates an article based on the provided parameters.

#### Request Parameters

All parameters are strings and should be included in the JSON body of the request.

- **topic**: The main subject or theme of the article.
- **target_audience**: The intended readers of the article.
- **audience_questions**: Common questions or concerns of the target audience.
- **purpose**: The goal or objective of the article (e.g., inform, persuade).
- **detail_info**: Additional details or specifics to be included.
- **length**: Desired length of the article (e.g., "short", "medium", "long").
- **style**: The writing style to be applied (e.g., "formal", "informal", "technical").

#### Request Example

```http
POST /server/generate_article HTTP/1.1
Content-Type: application/json

{
  "topic": "Advancements in Artificial Intelligence",
  "target_audience": "Software Engineers and Tech Enthusiasts",
  "audience_questions": "How is AI impacting software development?",
  "purpose": "To inform readers about the latest AI technologies",
  "detail_info": "Include recent AI frameworks and tools",
  "length": "medium",
  "style": "informative"
}
```

#### Successful Response

- **Status Code:** `200 OK`
- **Body:** An `Article` object containing the generated article.

#### Response Example

```json
{
  "title": "Advancements in Artificial Intelligence",
  "summary": "An overview of how AI is transforming software development.",
  "objective": "To inform readers about the latest AI technologies.",
  "description": "This article explores recent developments in AI and their impact on software engineering.",
  "sections": [
    {
      "section_name": "Introduction",
      "section_content": "Artificial Intelligence (AI) has rapidly evolved...",
      "easy_reading": "...",
      "informative_version": "...",
      "feedback": "",
      "section_content_final": "..."
    }
    // Additional sections
  ]
}
```

---

### 2. Provide Feedback

- **URL:** `/server/provide_feedback`
- **Method:** `POST`
- **Description:** Provides feedback on an article from the perspective of a specified persona.

#### Request Parameters

Include in the JSON body:

- **article**: The `Article` object to receive feedback on.
- **persona**: A string description of the reader persona (e.g., "Marketing Specialist").
- **job_description**: A detailed description of the persona's job role.

#### Request Example

```http
POST /server/provide_feedback HTTP/1.1
Content-Type: application/json

{
  "article": { /* Article object as defined above */ },
  "persona": "Marketing Specialist",
  "job_description": "Responsible for promoting products and understanding customer needs."
}
```

#### Successful Response

- **Status Code:** `200 OK`
- **Body:** An `Article` object with updated `feedback` fields in each section, reflecting the persona's comments.

#### Response Example

```json
{
  "title": "...",
  "summary": "...",
  "objective": "...",
  "description": "...",
  "sections": [
    {
      "section_name": "Introduction",
      "section_content": "...",
      "easy_reading": "...",
      "informative_version": "...",
      "feedback": "Consider emphasizing the benefits to the customer.",
      "section_content_final": "..."
    }
    // Additional sections with feedback
  ]
}
```

---

### 3. Edit Article

- **URL:** `/server/edit_article`
- **Method:** `POST`
- **Description:** Edits an article based on the provided guidance for each section.

#### Request Parameters

Include in the JSON body:

- **article**: The `Article` object to be edited.
- **guidance**: A string containing instructions on how to edit each section.

#### Request Example

```http
POST /server/edit_article HTTP/1.1
Content-Type: application/json

{
  "article": { /* Article object as defined above */ },
  "guidance": "For the introduction, make it more engaging. In the conclusion, include a call to action."
}
```

#### Successful Response

- **Status Code:** `200 OK`
- **Body:** An `Article` object with updated `section_content_final` fields reflecting the applied edits.

#### Response Example

```json
{
  "title": "...",
  "summary": "...",
  "objective": "...",
  "description": "...",
  "sections": [
    {
      "section_name": "Introduction",
      "section_content": "...",
      "easy_reading": "...",
      "informative_version": "...",
      "feedback": "...",
      "section_content_final": "An engaging introduction that captures the reader's attention..."
    }
    // Additional sections with edits
  ]
}
```

---

### 4. Get Markdown Article

- **URL:** `/server/getmarkdown_article`
- **Method:** `POST`
- **Description:** Retrieves the article content in Markdown format.

#### Request Parameters

Include in the JSON body:

- **article**: The `Article` object to be converted into Markdown.

#### Request Example

```http
POST /server/getmarkdown_article HTTP/1.1
Content-Type: application/json

{
  "article": { /* Article object as defined above */ }
}
```

#### Successful Response

- **Status Code:** `200 OK`
- **Body:** A JSON object containing the article content in Markdown format.

#### Response Example

```json
{
  "content": "# Advancements in Artificial Intelligence\n\n## Introduction\nAn engaging introduction that captures the reader's attention...\n\n## [Section Name]\n[Section Content]\n\n// Additional sections\n"
}
```

---

## Example Usage

### Generating an Article

1. **Request:**

   Send a `POST` request to `/server/generate_article` with the necessary parameters.

2. **Response:**

   Receive an `Article` object with the generated content.

### Providing Feedback

1. **Request:**

   Send a `POST` request to `/server/provide_feedback` with the `Article` object and persona details.

2. **Response:**

   Receive the `Article` object updated with feedback in each section.

### Editing an Article

1. **Request:**

   Send a `POST` request to `/server/edit_article` with the `Article` object and editing guidance.

2. **Response:**

   Receive the `Article` object with edits applied in the `section_content_final` fields.

### Retrieving Article in Markdown

1. **Request:**

   Send a `POST` request to `/server/getmarkdown_article` with the `Article` object.

2. **Response:**

   Receive a JSON object containing the article content formatted in Markdown.

---

## Error Responses

In case of errors, the API will respond with an error object containing details.

### Error Object Structure

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "string"
  }
}
```

### Common Error Codes

- **400 Bad Request:** Invalid or missing parameters.
- **500 Internal Server Error:** An unexpected error occurred on the server.

### Example Error Response

```json
{
    "message": "Invalid request parameters."
}
```

---

## Conclusion

This API provides endpoints for generating, editing, and retrieving articles using a structured `Article` object. By following the provided endpoint descriptions and using the examples as a guide, developers can integrate these functionalities into applications that require dynamic article creation and manipulation.

If you have any questions or need further assistance, please refer to the documentation or contact the API support team.

---

# Appendix

## Article Object JSON Representation

For reference, here's the structure of the `Article` object used in the requests and responses.

```json
{
  "title": "string",
  "summary": "string",
  "objective": "string",
  "description": "string",
  "sections": [
    {
      "section_name": "string",
      "section_content": "string",
      "easy_reading": "string",
      "informative_version": "string",
      "feedback": "string",
      "section_content_final": "string"
    }
    // Additional Section objects
  ]
}
```

---

**Notes:**

- **Content Fields:** When processing articles, ensure that the `section_content_final` field is used for the finalized content in each section.
- **Error Handling:** If any required parameters are missing or invalid, the server should respond with appropriate error messages and status codes (e.g., `400 Bad Request`).
- **Character Encoding:** All text data should be encoded using UTF-8 to support a wide range of characters and symbols.


---