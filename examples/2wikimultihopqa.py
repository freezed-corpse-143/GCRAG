decompose_examples_2wikimultihopqa = '''
Question: Are North Marion High School (Oregon) and Seoul High School both located in the same country?
Thought: Which country is North Marion High School (Oregon) located in?
Answer: North Marion High School (Oregon) is located in **United States**.
Thought: Which country is Seoul High School located in?
Answer: Seoul High School is located in **South Korea**.
Thought: Seoul High School is located in South Korea while North Marion High School (Oregon) is located in the United States. They are not in the same country.
Answer: FINISH[No]

Question: Does Jon Wertheim have the same nationality as Jon L. Mills
Thought: what is Jon Wertheim's nationality?
Answer: Jon Wertheim's country of citizenship is American.
Thought: what is Jon L. Mills's nationality?
Answer: Jon L. Mills's nationality is American
Thought: Both Jon Wertheim and Jon L. Mills are American.
Answer: FINISH[yes]

Question: Which film came out first, Blind Shaft or The Mask Of Fu Manchu?
Thought: When was the film Blind Shaft released?
Answer: Blind Shaft was released in **2003**
Thought: When was the film The Mask Of Fu Manchu released?
Answer: The Mask of Fu Manchu was released in **1932**, which is earlier than Blind Shaft.
Thought: The film Mask Of Fu Manchu came out in 1932 while The film Blind Shaft came out in 2003. The Mask of Fu Manchu came out first.
Answer: FINISH[The Mask of Fu Manchu]

Question: When did John V, Prince Of Anhalt-Zerbst's father die?
Thought: Who is the father of John V, Prince Of Anhalt-Zerbst?
Answer:  **Ernest I, Prince of Anhalt-Dessau** is the father of John V, Prince Of Anhalt-Zerbst.
Thought: when did John V, Prince Of Anhalt-Zerbst die?
Answer: Ernest I, Prince of Anhalt-Dessau died in **1516**.
Thought: Ernest I, Prince of Anhalt-Dessau is the father of John V, Prince Of Anhalt-Zerbst, and he died in 1516
Answer: FINISH[1516]

Question: Where was the director of the film Ronnie Rocket born?
Thought: Who is the director of the film Ronnie Rocket?
Answer: **David Lynch** is the director of Ronnie Rocket
Thought: David Lynch is the director. Where was David Lynch born?
Answer: **Missoula, Montana** is the birthplace of David Lynch.
Thought: David Lynch is the director of Ronnie Rocket. He was born in Missoula, Montana.
Answer: FINISH[Missoula, Montana]
'''.strip()