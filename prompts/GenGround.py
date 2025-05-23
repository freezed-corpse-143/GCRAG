decompose_instructions = '''
Please answer the question by following these steps:
1. Break down the main question into smaller, specific sub-questions
2. For each sub-question:
   - First provide a "Thought:" that clearly states what you're investigating
   - Then provide an "Answer:" with factual information and key details in bold
3. Continue until you can conclusively answer the original question
4. When you can conclusively answer the original question, end with "Answer: FINISH[final answer]". The final answer should be concise and directly address the question without any additional explanation.
5. If you don't have enough document to answer the question, output "No enough information" instead of "FINISH".
6. If the question includes candidate answers, the final answer should be one of the candidate answers.
7. If you can conclusively answer the original question, clarify the type of final answer(Yes/No, time, place, person's name, number, etc), which is corresponding to your final answer.

Rules to follow:
- **Be specific** in Thoughts: Clearly name entities and what you're checking
- **Bold key facts** in Answers: Highlight the most important information
- **No pronouns**: Always use proper names instead of "he/she/they"
- **Be decisive**: Provide the best answer you can even if uncertain
- **Use original vocabulary**: Try to use the words from the question in your thoughts, avoiding new terms.

Example Format:reason
Question: [original question]
Thought 1: [first sub-question]
Answer 1: [answer with **key facts**]
Thought 2: [next sub-question]
Answer 2: [answer with **key facts**]
...
Thought: Question impolies/includes ...(information about final answer)...
Answer: FINISH[final answer]
'''.strip()

decompose_prompt = f"{decompose_instructions}" + '''

Here are some examples of how to answer step-by-step:
{examples}

Now answer the following question using the same format:
Question: {question}
{thoughts_and_answers}
'''.strip()

ground_instructions = '''
You will be provided with documents (labeled Document 1, Document 2, etc.), a question, and an old answer. Your task is to:
1. Extract the corresponding sentences to verify and edit the old answer using only information from the provided documents.
2. If you edit the old answer, please attach the extracted sentences to the new answer without newline/line break.
3. If not document is help, directly output old answer as the new new answer and attach nothing.

Example format:
Input:
Question: What is topic A about?
Document 1: "Text about topic A is about music"
Document 2: "Text about topic B..."
Document 3: "Text about topic C..."
...
Old Answer: Topic A is about computer.
New answer: Music. The relevant sentences: Document 1,...
'''.strip()

ground_prompt = f"{ground_instructions}" + '''

Here are some examples:
{examples}

Input:
Question: {question}
{retrieved_documents}
Thought: {thought}
Old answer: {answer}
'''.strip()

ground_single_instructions = '''
You will be provided with a document, a question, and an thought. Your task is to:
1. Determine whether the document content is helpful for answering the thought
2. Respond only with "True" if the document is helpful, or "False" if not
3. Do not provide any additional explanation or text.

Example format:
Input:
Question: Are Topic A and Topic C about the same?
Thought: What is topic A about?
Document : "Text about topic A is about music"
You response:
True
'''.strip()

ground_single_prompt = f"{ground_single_instructions}" + '''

Here are some examples:
{examples}

Input:
Question: {question}
Thought: {thought}
Document: {document}
Your response:
'''.strip()

answer_format_instructions = '''
You will be provided with a question and an old answer. Your task is to analyze the old answer and generate a new, concise answer that directly responds to the question. The new answer should:
1. If the question is a yes/no question, answer only "YES" or "NO."
2. If the question requires an entity (e.g., time, person, place), extract the most relevant one as answer without additional explanatory or descriptive information.
2. Be as brief as possible
3. End with "FINISH[answer]" where "answer" is your response
4. If the question is a multiple-choice question (the question includes candidate answers), select one answer from the candidate answers provided in the question.

Format your response exactly as shown in the examples.
'''.strip()

answer_format_examples = '''
Question: Nobody Loves You was written by John Lennon and released on what album that was issued by Apple Records, and was written, recorded, and released during his 18 month separation from Yoko Ono?
Old answer: The album issued by Apple Records, and written, recorded, and released during John Lennon's 18 month separation from Yoko Ono is Walls and Bridges. Nobody Loves You was written by John Lennon on Walls and Bridges album. So the answer is: Walls and Bridges.
New answer: FINISH[Walls and Bridges]

Question: What is known as the Kingdom and has National Route 13 stretching towards its border?
Old answer: Cambodia is officially known as the Kingdom of Cambodia. National Route 13 streches towards border to Cambodia. So the answer is: Cambodia.
New answer: FINISH[Cambodia]

Question: Jeremy Theobald and Christopher Nolan share what profession?
Old answer: Jeremy Theobald is an actor and producer. Christopher Nolan is a director, producer, and screenwriter. Therefore, they both share the profession of being a producer. So the answer is: producer.
New answer: FINISH[producer]
'''.strip()

answer_format_prompt = f"{answer_format_instructions}\n\n" + f"Here are some examples:\n{answer_format_examples}\n\n" + '''
Question: {question}
Old answer: {answer}
New answer:
'''.strip()

decompose_examples_prompt = '''
# Comparison Question
Question: Who was born first, Albert Einstein or Abraham Lincoln?
Thought 1: When was Albert Einstein born?
Answer 1: Albert Einstein was born on March 14, 1879.
Thought 2: When was Abraham Lincoln born?
Answer 2: Abraham Lincoln was born on February 12, 1809.
Thought 3: Question includes candidate answers: Albert Einstein (born in 1879), Abraham Lincoln (born in 1809). Who was born first?
Answer 3: FINISH[Abraham Lincoln]

# Inference Question
Question: Who is the paternal grandmother of Abraham Lincoln?
Thought 1: Who is the monther of Abraham Lincoln?
Answer 1: Abraham Lincoln's mother is Nancy Hanks Lincoln.
Thouhgt 2: Who is the father of Nancy Hanks Lincoln?
Answer 2: Nancy Hanks Lincoln'father is James Hanks.
Thought 3: Question implies that the final answer is a person's name. Abraham Lincoln'mother is Nancy Hanks Lincoln. Nancy Hanks Lincoln'father is James Hanks. Who is the maternal grandfather of Abraham Lincoln?
Answer 3: FINISH[James Hanks]

# Compositional Question
Question: Who is the founder of the company that distributed La La Land film?
Thought 1: Which company distributed "La La Land"?
Answer 1: "La La Land" was distributed by Summit Entertainment.
Thought 2: Who is the founder of Summit Entertainment?
Answer 2: Summit Entertainment was founded by Patrick Wachsberger and Bob Yari.
Thought 3: Question implies that the final answer is a person's name. Who is the founder of the company that distributed La La Land film?
Answer 3: FINISH[Patrick Wachsberger, Bob Yari]

# Bridge - comparison question
Question: Which movie has the director born first, La La Land or Tenet?
Thought 1: Who is the director of La La Land?
Answer 1: The director of "La La Land" is Damien Chazelle.
Thought 2: When was Damien Chazelle born?
Answer 2: Damien Chazelle was born on January 19, 1985.
Thought 3: Who is the director of Tenet?
Answer 3: The director of "Tenet" is Christopher Nolan.
Thought 4: When was Christopher Nolan born?
Answer 4: Christopher Nolan was born on July 30, 1970.
Thought 5: Compare the birth dates of Damien Chazelle and Christopher Nolan to determine who was born first.
Answer 5: FChristopher Nolan.
Thought 5: Question includes candidate answers: La La Land, Tenet. Above all, which movie has the director born first, La La Land or Tenet?
Answer 5: FINISH[Tenet]

# Comparison Question
Question: Are Tabisheh and Qarah Takan, Razavi Khorasan located in the same country?  
Thought 1: Where is Tabisheh located?  
Answer 1: Tabisheh is a village in Zu ol Faqr Rural District, Sarshiv District, Saqqez County, Kurdistan Province, Iran.  
Thought 2: Where is Qarah Takan located?  
Answer 2: Qarah Takan is a village in Yam Rural District, Meshkan District, Khoshab County, Razavi Khorasan Province, Iran. 
Thought 4: Question includes candidate answers: yes, no. Are Tabisheh and Qarah Takan in the same country?  
Answer 4: FINISH[yes]

# Comparison Question
Question: Do Archie Palmer and Umar Cheema have the same nationality?
Thought 1: What is Archie Palmer's nationality?
Answer 1: Archie Palmer was an American educator and academic administrator, as stated in the supporting fact. Therefore, his nationality is American.
Thought 2: What is Umar Cheema's nationality?
Answer 2: Umar Cheema is an investigative reporter for the Pakistani newspaper "The News" and has been involved in events and organizations primarily based in Pakistan, such as the Chevening Scholarship and the Daniel Pearl Journalism Fellowship. This suggests his nationality is Pakistani.
Thought 3: Question includes candidate answers: yes, no. Do Archie Palmer (American) and Umar Cheema (Pakistani) share the same nationality?
Answer 3: FINISH[no]
'''.strip()


ground_examples_prompt = '''
Input:
Question: The Wild Wacky Wonderful World of Winter had a co-star in which actress from the sitcom "Alice"?
Document 1: Elizabeth "Beth" Howland (May 28, 1941 – December 31, 2015) was an American actress. She worked on stage and television and was best known for playing Vera Gorman in the sitcom "Alice", inspired by the Martin Scorsese film "Alice Doesn't Live Here Anymore" (1974).
Document 2: The 2010 Emory Healthcare 500 was a NASCAR Sprint Cup Series stock car race that was held on September 5, 2010 at Atlanta Motor Speedway in Hampton, Georgia. Contested over 325 laps, it was the twenty-fifth race of the 2010 Sprint Cup Series season. The race was won by Tony Stewart, for the Stewart Haas Racing team. Carl Edwards finished second, and Jimmie Johnson, who started seventh, clinched third.
Document 3: George Stanley McGovern (July 19, 1922 – October 21, 2012) was an American historian, author, U.S. Representative, U.S. Senator, and the Democratic Party presidential nominee in the 1972 presidential election.
Thought: Who played a notable role in the sitcom "Alice"?
Old answer: Linda Lavin played Vera Gorman in the sitcom "Alice".
New answer: Elizabeth "Beth" Howland. The relevant sentences: Elizabeth "Beth" Howland (May 28, 1941 – December 31, 2015) was an American actress. She worked on stage and television and was best known for playing Vera Gorman in the sitcom "Alice", inspired by the Martin Scorsese film "Alice Doesn't Live Here Anymore" (1974).

Input:
Question: What team defeated the Philadelphia Phillies in 4 games, and plays in the Yankee Stadium?
Document 1: "Snow White" is a 19th-century German fairy tale which is today known widely across the Western world. The Brothers Grimm published it in 1812 in the first edition of their collection "Grimms' Fairy Tales". It was titled in German: Sneewittchen (in modern orthography "Schneewittchen") and numbered as Tale 53. The name "Sneewittchen" was Low German and in the first version it was translated with "Schneeweißchen". The Grimms completed their final revision of the story in 1854.
Document 2: Yankee Stadium was a stadium located in the Bronx, a borough of New York City. It was the home ballpark of the New York Yankees, one of the city's Major League Baseball (MLB) franchises, from 1923 to 1973 and then from 1976 to 2008. The stadium hosted 6,581 Yankees regular season home games during its 85-year history. It was also the former home of the New York Giants football team from 1956 through the first part of the 1973–74 football season. The stadium's nickname, "The House That Ruth Built", is derived from Babe Ruth, the baseball superstar whose prime years coincided with the stadium's opening and the beginning of the Yankees' winning history. It has also been known as "The Big Ballpark in The Bronx", "The Stadium", and "The Cathedral of Baseball".
Document 3: The 1950 New York Yankees season was the 48th season for the team in New York and its 50th overall as a franchise. The team finished with a record of 98–56, winning their 17th pennant, finishing 3 games ahead of the Detroit Tigers. In the World Series, they defeated the Philadelphia Phillies in 4 games. New York was managed by Casey Stengel. The Yankees played at Yankee Stadium.
Document 4: Group Captain Geoffrey Leonard Cheshire, Baron Cheshire (7 September 1917 – 31 July 1992) was a highly decorated World War II Royal Air Force pilot and philanthropist.
Thought : Which team defeated the Philadelphia Phillies in 4 games in the World Series?
Old answer: The 1950 Brooklyn Dodgers defeated the Philadelphia Phillies in 4 games in the World Series.
New answer: The 1950 New York Yankees. The relevant sentences: The 1950 New York Yankees season was the 48th season for the team in New York and its 50th overall as a franchise. The team finished with a record of 98–56, winning their 17th pennant, finishing 3 games ahead of the Detroit Tigers. In the World Series, they defeated the Philadelphia Phillies in 4 games. New York was managed by Casey Stengel. The Yankees played at Yankee Stadium.

Input:
Question: In what year did the American professional stock car racing driver that finished third in the September 5, 2010 Atlanta Motor Speedway was born?
Document 1: The 2010 Emory Healthcare 500 was a NASCAR Sprint Cup Series stock car race that was held on September 5, 2010 at Atlanta Motor Speedway in Hampton, Georgia. Contested over 325 laps, it was the twenty-fifth race of the 2010 Sprint Cup Series season. The race was won by Tony Stewart, for the Stewart Haas Racing team. Carl Edwards finished second, and Jimmie Johnson, who started seventh, clinched third.
Document 2: Jimmie Kenneth Johnson (born September 17, 1975) is an American professional stock car racing driver and a seven-time champion in the Monster Energy NASCAR Cup Series. He currently drives the No. 48 Chevrolet SS for Hendrick Motorsports.
Thought: Who was the driver that finished third in the September 5, 2010 Atlanta Motor Speedway race?
Old answer: the driver who finished third in the 2010 Emory Healthcare 500 at Atlanta Motor Speedway was Dale Earnhardt Jr.
New answer: Jimmie Johnson. The relevant sentences: The 2010 Emory Healthcare 500 was a NASCAR Sprint Cup Series stock car race that was held on September 5, 2010 at Atlanta Motor Speedway in Hampton, Georgia. Contested over 325 laps, it was the twenty-fifth race of the 2010 Sprint Cup Series season. The race was won by Tony Stewart, for the Stewart Haas Racing team. Carl Edwards finished second, and Jimmie Johnson, who started seventh, clinched third.
'''.strip()

ground_single_examples = '''
Input:
Question: When was the city where Howdy Holmes was born founded?
Thought: Where was Howdy Holmes born?
Document: Howard "Howdy" S. Holmes (born December 14, 1947, Ann Arbor, Michigan), is a former driver in the CART Championship Car series. He began racing in the early 1970s and was based in Stockbridge, Michigan, about northeast of Chelsea, Michigan where his family owned a milling company.
Your response:
True

Input:
Question: How many states are there in the country that Ghee is from?
Thought: How many states are there in the country that Ghee is from?
Document: Avalau is an islet within the atoll of Funafuti, Tuvalu. Charles Hedley described Avalau in 1896 "this islet is said to possess a spring of fresh water".
Your response:
False

Input:
Question: What is the date of death of Quentin Metsys The Younger's father?
Thought: Who is Quentin Metsys The Younger's father?
Document: Quentin Metsys the Younger (Quinten or Massys; c. 1543 – 1589) was a Flemish Renaissance painter, one of several of his countrymen active as artists of the Tudor court in the reign of Elizabeth I of England. He was the son of Flemish painter Jan Massys, Matsys, or Metsys and the grandson and namesake of Quentin Massys or Metsys. The younger Quentin was born in Antwerp, where he joined the Guild of St. Luke in 1574; by c. 1581 he was living in London, likely having fled religious persecution in Antwerp as his father and uncle had done. He left England for Frankfurt in 1588 and died there the next year. He is best known for the "Sieve Portrait" of Elizabeth I, in which she is depicted as Tuccia, a Vestal Virgin who proved her chastity by carrying water from the Tiber River to the Temple of Vesta without spilling a drop. Elizabeth is surrounded by symbols of empire, including a column and a globe, iconography that would appear again and again in her portraiture of the 1580s and 1590s, most notably in the "Armada Portrait" of 1588.
Your response:
True

Input:
Question: What is the place of birth of the composer of film Kaayamkulam Kochunniyude Makan?
Thought: Who is the composer of the film Kaayamkulam Kochunniyude Makan?
Document: Bipradash Barua( born 1940) is a Bangladeshi novelist. He was awarded Bangla Academy Literary Award in 1991 and Ekushey Padak in 2014.
Your response:
False
'''


