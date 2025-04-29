decompose_examples_hotpotqa = '''
Question: Which magazine was started first, Arthur's Magazine or First for Women?
Thought 1: First, I should ask "When Arthur's Magazine started?"
Answer 1: Arthur's Magazine was an American literary periodical published in Philadelphia, which started in **19th (1844)**.
Thought 2: Then, I should ask "When First for Women started?"
Answer 2: "First for Women" is a well-known women's magazine that covers topics such as health, beauty, fitness, food, and lifestyle. It started in **1989**.
Thought 3: Which one started first?
Answer 3: Finish[Arthur's Magazine

Question: Who was the captain of the only battleship to provide gunfire support during the Vietnam War?
Thought 1: Who was the captain of the battleship that provided gunfire support during the Vietnam War?
Answer 1: Rear Adm. J. (October 23, 1924 – November 4, 2007) was notable as the captain of the battleship USS "New Jersey" during that ship's deployment to the Vietnam War in 1968. 
Thought 2: I have got all the information. And **Rear Adm. J.** is the captain providing gunfire support during the Vietnam War?`
Answer 2: FINISH[Rear Adm. J.]

Question: How old is the female main protagonist of Catching Fire? 
Thought 1:  What is the Catching Fire?
Answer 1: Catching Fire is the second book in "The Hunger Games trilogy" written by Suzanne Collins.  It is written in the voice of **Katniss Everdeen**,
Thought 2: Katniss Everdeen is the protagonist of Catching Fire. How old is Katniss Everdeen in Catching Fire book?
Answer 2: Katniss Everdeen in Catching Fire book is **16 years old**
Thought 3: FireKatniss Everdeen, the female main protagonist of Catching, is FireKatniss Everdeen and she is **16** years old.
Answer 3: FINISH[16]

Question: What is one of the stars of The Newcomers known for?
Thought 1: Who are the stars in Newcomers?
Answer 1: **Chris Evans** is one of the stars in the Newcomers.
Thought 2: Chris Evans is one of the star in The Newcomers. What is the Chris Evans known for?
Answer 2: Chris Evans is known for **superhero roles as the Marvel Comics**
Thought 3: I have got all the information. Chris Evans is a star in Newcomers, who is known for **superhero roles as the Marvel Comics**
Answer 3: FINISH]Superhero roles as the Marvel Comics]

Question: Billy Preston is an American college basketball player for a team that competes in what?
Thought 1: Billy Preston is an American college basketball player. What does Billy Preston play for?
Answer 1: Billy Preston is an American college basketball player for the **Kansas Jayhawks**.
Thought 2: Kansas Jayhawks is an American college basketbal team. What does the Kansas Jayhawks compete for?
Answer 2: Kansas Jayhawks competes for the **Big 12 Conference**
Thought 3: I have got all the information. Billy Preston play for Kansas Jayhawks, and Kansas Jayhawks competes for the **Big 12 Conference**
Answer 3: FINISH[The Big 12 Conference]
'''.strip()
