import re
import regex

def extract_thought_answer(text):
    result = []
    
    # Extract first Thought and its content
    thought_match = re.search(r"Thought(?:\s*\d+)?:\s*(.*?)(?=\nAnswer(?:\s*\d+)?:|$)", text, re.DOTALL)
    if thought_match:
        thought = thought_match.group(1).replace("\n", " ").strip()
        result.append(thought)
    else:
        result.append("")  # Empty string if no Thought found
    
    # Extract first Answer and its content
    answer_match = re.search(r"Answer(?:\s*\d+)?:\s*(.*?)(?=\nThought(?:\s*\d+)?:|$)", text, re.DOTALL)
    if answer_match:
        answer = answer_match.group(1).replace("\n", " ").strip()
        result.append(answer)
    else:
        result.append("")  # Empty string if no Answer found
    
    return result

def extract_answer(input_string):
    match = re.search(r'FINISH\[(.*?)\]', input_string)
    if match:
        return match.group(1)
    else:
        return ""
    

def format_sp(supporting_facts):
    output = ""
    for idx, item in enumerate(supporting_facts):
        output += f"Supporting fact {idx+1}:\n{item['paragraph_text']}"
    return output.strip()

def clean_text(text):
    return regex.sub(r'[\s\p{P}\p{S}]+', '', text)

def extract_from_ground_answer(text):
    # new_answer_match = re.search(r'New answer:(.*?)(?=supporting fact ids:|$)', text, re.DOTALL)
    new_answer_match = re.search(r'New answer:(.*?)(?=$)', text, re.DOTALL)
    new_answer = new_answer_match.group(1).strip() if new_answer_match else None
    
    # fact_ids_match = re.search(r'Supporting fact ids:(.*?)(?=$)', text)
    # fact_ids_str = fact_ids_match.group(1).strip() if fact_ids_match else ""
    
    # fact_ids = [int(num) for num in re.findall(r'[1-9]', fact_ids_str)] if fact_ids_str else []
    # return (new_answer, fact_ids)
    return new_answer

def format_retr_docs(retr_docs):
    result = ""
    for idx, d in enumerate(retr_docs):
        result += f"Document {idx+1}: " + d['paragraph_text'] + "\n"