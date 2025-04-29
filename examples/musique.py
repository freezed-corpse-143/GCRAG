decompose_examples_musique = """
Question: Where do Greyhound buses leave from in the city where Arna Selznick's employer is headquartered?
Thought: Who is the employer of Arna Selznick?
Answer: The employer of Arna Selznick is Nelvana since he directed Nelvana's 1985 animated film The Care Bears Movie.
Thought: Nelvana is an animation studio and entertainment company. Where is the headquarters of Nelvana?
Answer: The headquarters of Nelvana is in Toronto.
Thought: Where do Greyhound buses leave from Toronto?
Answer: Greyhound buses leave from **Toronto Coach Terminal**
Thought: the employer of Arna Selznick is Nelvana. Nelvana's headquartered is in Toronto. Greyhound leave from **Toronto Coach Terminal**
Answer: FINISH[Toronto Coach Terminal]

Question: Which county does Lloyd Dane's birthplace belong to?
Thought: What is the Lloyd Dane's birthplace?
Answer: Lloyd Dane's birthplace is Eldon.
Thought: Eldon is a city. Which country does Eldon belong to?
Answer: Eldon belongs to Miller County.
Thought: Lloyd Dane's birthplace is Eldon. Eldon belongs to Miller County.
Answer: FINISH[Miller County]

Question: Who wrote \"Turn Me On\" by the performer of \"Happy Pills\"?
Thought: Happy Pills is an song from American. Who is the performer of "Happy Pills"?
Answer: the performer of Happy Pills is Norah Jones.
Thought: Turn Me On is a song. Who wrote "Turn Me On" performed by Norah Jones?
Answer: **John D. Loudermilk** wrote: "Turn Me On".
Thought: The performer of "Happy Pills" is **Norah Jones**. **John D. Loudermilk** wrote the `Turn Me On` by Norah Jones.
Answer: FINISH[John D. Loudermil]

Question: Who did the screenwriter for Good Will Hunting play in Dazed and Confused?
Thought: Who is the screenwriter of Good Will Hunting?
Answer: the screenwriter of Good Will Hunting is Ben Affleck.
Thought: who did Ben Affleck play in "Dazed and Confused"?
Answer: Ben Affleck plays Fred O'Bannion in "Dazed and Confused"
Thought: **Ben Affleck** is the screenwriter of Good Will Hunting. Ben Affleck plays **Fred O'Bannion** in `Dazed and Confused`.
Answer: FINISH[Fred O'Bannion]
""".strip()