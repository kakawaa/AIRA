import openai
import re
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_embeddings(text):
    """Generate test case embeddings using OpenAI."""
    response = openai.embeddings.create(input=[text], model="text-embedding-ada-002").data[0].embedding
    
    return response

import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_chatgpt_suggestions_with_context(query_text, existing_cases):
    """Generate additional test cases using OpenAI ChatGPT."""
    existing_cases_text = "\n".join(
        f"- Test Case ID: {case['test_case_id']}\n"
        f"  Test Description: {case['test_description']}\n"
        f"  Pre-requisite: {case['pre_requisite']}\n"
        f"  Test Steps: {case['test_steps']}\n"
        f"  Expected Result: {case['expected_result']}\n"
        for case in existing_cases
    )

    # ChatGPT prompt
    messages = [
        {"role": "system", "content": "You are a test case generation assistant for an e-commerce platform. Your job is to generate precise, unique, and structured test cases based on input queries."},
        {"role": "user", "content": f"""
        The user has submitted the following feature query:
        "{query_text}"
        
        The following test cases already exist:
        {existing_cases_text}
        
        Your tasks:
        1. Analyze the above existing test cases carefully and ensure there is no overlap or duplication.
        2. Generate 5 completely new and unique test cases. Each test case must strictly follow this format:
        
        - Test Case ID: [Unique ID]
        - Test Description: [A brief description of the test case]
        - Pre-requisite: [Conditions required before the test]
        - Test Steps:
            1. [Step 1]
            2. [Step 2]
            ...
        - Expected Result: [The expected outcome of the test]
        
        3. Based on both the existing and new test cases, provide a Test Focus. This should summarize the most critical areas of testing, considering the feature query, existing coverage, and the newly generated test cases. Highlight gaps, priorities, and areas requiring special attention.

        Ensure that the new test cases are distinct, innovative, and address gaps not covered in the existing test cases.
        Your output must strictly follow this format and avoid inconsistencies:
        
        New Test Cases:
        - Test Case ID: ...
        - Test Description: ...
        - Pre-requisite: ...
        - Test Steps:
            1. ...
            2. ...
        - Expected Result: ...
        
        Test Focus:
        ...
        """}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1000,
            temperature=0.3
        )
        generated_text = response.choices[0].message.content.strip()

        print(f"Output from chatGPT: {generated_text}")

        # Separate New Test Cases and Focused Test Summary
        if "Test Focus:" in generated_text:
            new_test_cases_text, summary = generated_text.split("Test Focus:", 1)
        else:
            new_test_cases_text, summary = generated_text, "No summary available."

        new_test_cases = parse_generated_test_cases(new_test_cases_text)
        return new_test_cases, summary.strip()
    except Exception as e:
        print(f"Error generating ChatGPT suggestions: {e}")
        return [], "No summary available."


import re

def parse_generated_test_cases(generated_text):
    """
    Parse structured or semi-structured text from ChatGPT response into a list of test case dictionaries,
    and prefix AI-generated test case IDs with 'AI_'.

    Args:
        generated_text (str): Text containing generated test cases.

    Returns:
        list: Parsed list of test case dictionaries with 'AI_' prefix for test case IDs.
    """
    test_cases = []
    blocks = re.split(r"- Test Case ID:", generated_text)  # Split by Test Case ID markers

    for block in blocks[1:]:  # Skip the first part (it doesn't contain a test case)
        lines = block.strip().splitlines()
        current_case = {}
        steps = []

        for i, line in enumerate(lines):
            line = line.strip()

            if i == 0:  # First line is always the Test Case ID
                current_case["test_case_id"] = f"AI_{line}"

            elif line.startswith("- Test Description:"):
                current_case["test_description"] = line.split(":", 1)[1].strip()

            elif line.startswith("- Pre-requisite:"):
                current_case["pre_requisite"] = line.split(":", 1)[1].strip()

            elif line.startswith("- Test Steps:"):
                # Collect steps until "Expected Result" or end of block
                for step_line in lines[i + 1 :]:
                    step_line = step_line.strip()
                    if step_line.startswith("- Expected Result:"):
                        break
                    steps.append(step_line)
                current_case["test_steps"] = " ".join(steps).strip()

            elif line.startswith("- Expected Result:"):
                current_case["expected_result"] = line.split(":", 1)[1].strip()

        # Ensure all required fields are present
        if "test_case_id" in current_case:
            current_case["test_steps"] = current_case.get("test_steps", "Steps not provided.")
            current_case["expected_result"] = current_case.get("expected_result", "Expected result not provided.")
            test_cases.append(current_case)

    return test_cases