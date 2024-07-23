import os
import glob
import json
from openai import OpenAI, APIError
from dotenv import load_dotenv

load_dotenv()

def get_all_md_files(root_dir):
    return glob.glob(os.path.join(root_dir, '**', '*.md'), recursive=True)

def concatenate_md_files(md_files, output_file, lines_per_file):
    combined_content = ""
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as infile:
                for i in range(lines_per_file):
                    line = infile.readline()
                    if not line:
                        break
                    combined_content += line
                    outfile.write(line)
                combined_content += "\n\n"
                outfile.write('\n\n')
    return combined_content

def clean_response_content(content):
    """ Clean the response content to extract valid JSON part. """
    try:
        start_index = content.index('{')
        end_index = content.rindex('}') + 1
        json_content = content[start_index:end_index]
        return json.loads(json_content)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error cleaning response content: {e}")
        return None

def generate_questions_from_content(content, api_key, num_questions, model):
    client = OpenAI(api_key=api_key)
    all_questions = []
    used_questions = set()
    next_q_number = 1

    def call_api_for_questions(content, remaining_questions):
        nonlocal next_q_number

        prompt = f"""
Here is the entirety of my course, acknowledge it: {content}
Okay, now based exclusively off of what was covered, nothing outside of what has been EXPLICITLY covered IN THE COURSE, I need multiple choice questions. Give this to me in a JSON file that has a "questions": JS array that has JSON objects inside of it, like so: [{{"q_number":1, "q_text":"lorem ipsum", "q_choices": [{{"choice_letter":"A", "choice_text":"this is a choice", "choice_correct":true}},{{"choice_letter":"B", "choice_text":"this is a choice", "choice_correct":false}}] }}]...

Make sure there are 4 possible responses (A,B,C,D) for each question. I need the next {remaining_questions} multiple choice questions pertaining to what is covered in this course, starting with question number {next_q_number}.
"""
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                model=model,
            )
            message_content = response.choices[0].message.content
            print("API Response Content:\n", message_content)

            cleaned_data = clean_response_content(message_content)
            if not cleaned_data:
                print("Failed to clean the response content. Skipping this batch of questions.")
                return []

            questions_chunk = cleaned_data["questions"]
            filtered_questions = []
            for question in questions_chunk:
                q_text = question["q_text"]
                if q_text not in used_questions:
                    used_questions.add(q_text)
                    question["q_number"] = next_q_number
                    next_q_number += 1
                    filtered_questions.append(question)

            return filtered_questions

        except APIError as e:
            print(f"APIError: {e}")
            if e.status_code == 429:
                print("Rate limit exceeded or insufficient quota. Please check your plan and billing details.")
            else:
                print("An error occurred while generating questions.")
            return []
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print("Response content was not valid JSON. Here is the response content:")
            print(message_content)
            return []

    while len(all_questions) < num_questions:
        remaining_questions = num_questions - len(all_questions)
        new_questions = call_api_for_questions(content, min(10, remaining_questions))
        if not new_questions:
            break  # Exit if no new questions are returned
        all_questions.extend(new_questions)

    return {"questions": all_questions}

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")  # Use the API key from the .env file

    current_directory = os.getcwd()
    md_files = get_all_md_files(current_directory)
    output_file = os.path.join(current_directory, 'combined.md')

    lines_per_file = int(input("How many lines would you like to read from each Markdown file? "))
    combined_content = concatenate_md_files(md_files, output_file, lines_per_file)
    print(f"Combined {len(md_files)} Markdown files into {output_file}")

    num_questions = int(input("How many questions would you like to generate (in increments of 10)? "))

    questions_dict = generate_questions_from_content(combined_content, api_key, num_questions, 'gpt-4o-mini')
    if questions_dict:
        with open('exam_questions.json', 'w', encoding='utf-8') as json_file:
            json.dump(questions_dict, json_file, ensure_ascii=False, indent=4)
        print("Generated Questions have been saved to exam_questions.json")
