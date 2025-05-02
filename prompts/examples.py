decompose_examples_hotpotqa_1 = '''
Question: Which magazine was started first, Arthur's Magazine or First for Women?
Thought 1: First, When Arthur's Magazine started?
Answer 1: Arthur's Magazine was an American literary periodical published in Philadelphia, which started in **19th (1844)**.
Thought 2: Then, When First for Women started?
Answer 2: "First for Women" is a well-known women's magazine that covers topics such as health, beauty, fitness, food, and lifestyle. It started in **1989**.
Thought 3: Which one started first?
Answer 3: Finish[Arthur's Magazine]

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

decompose_examples_hotpotqa = '''
Prompt:
Question: Which magazine was started first, Arthur's Magazine or First for Women?
Your response:
Thought 1: First, When Arthur's Magazine started?
Answer 1: Arthur's Magazine was an American literary periodical published in Philadelphia, which started in **19th (1844)**.

Prompt:
Question: Who was the captain of the only battleship to provide gunfire support during the Vietnam War?
Thought 1: Who was the captain of the battleship that provided gunfire support during the Vietnam War?
Answer 1: Rear Adm. J. (October 23, 1924 – November 4, 2007) was notable as the captain of the battleship USS "New Jersey" during that ship's deployment to the Vietnam War in 1968. 
Your response:
Thought 2: I have got all the information. And **Rear Adm. J.** is the captain providing gunfire support during the Vietnam War?`
Answer 2: FINISH[Rear Adm. J.]

Prompt:
Question: How old is the female main protagonist of Catching Fire? 
Thought 1:  What is the Catching Fire?
Answer 1: Catching Fire is the second book in "The Hunger Games trilogy" written by Suzanne Collins.  It is written in the voice of **Katniss Everdeen**,
Thought 2: Katniss Everdeen is the protagonist of Catching Fire. How old is Katniss Everdeen in Catching Fire book?
Answer 2: Katniss Everdeen in Catching Fire book is **16 years old**
Your response:
Thought 3: FireKatniss Everdeen, the female main protagonist of Catching, is FireKatniss Everdeen and she is **16** years old.
Answer 3: FINISH[16]

Prompt:
Question: What is one of the stars of The Newcomers known for?
Thought 1: Who are the stars in Newcomers?
Answer 1: **Chris Evans** is one of the stars in the Newcomers.
Thought 2: Chris Evans is one of the star in The Newcomers. What is the Chris Evans known for?
Answer 2: Chris Evans is known for **superhero roles as the Marvel Comics**
Your response:
Thought 3: I have got all the information. Chris Evans is a star in Newcomers, who is known for **superhero roles as the Marvel Comics**
Answer 3: FINISH]Superhero roles as the Marvel Comics]

Prompt:
Question: Billy Preston is an American college basketball player for a team that competes in what?
Thought 1: Billy Preston is an American college basketball player. What does Billy Preston play for?
Answer 1: Billy Preston is an American college basketball player for the **Kansas Jayhawks**.
Thought 2: Kansas Jayhawks is an American college basketbal team. What does the Kansas Jayhawks compete for?
Answer 2: Kansas Jayhawks competes for the **Big 12 Conference**
Your response:
Thought 3: I have got all the information. Billy Preston play for Kansas Jayhawks, and Kansas Jayhawks competes for the **Big 12 Conference**
Answer 3: FINISH[The Big 12 Conference]
'''.strip()

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

ground_examples_hotpotqa = '''
Document 1: "Mother" is a song by English musician John Lennon, first released on his 1970 album "John Lennon/Plastic Ono Band". An edited version of the song was issued as a single in the United States on Apple Records, on 28 December 1970. The single runs about 1:41 shorter than the album due to a lack of the tolling bells intro and a quicker fadeout. The B-side features "Why" by Yoko Ono. The song peaked in the US at number 19 on the "Cashbox" Top 100 and number 43 on the "Billboard" Hot 100.
Document 2: "Nobody Loves You (When You're Down and Out)" is a song written by John Lennon released on his 1974 album "Walls and Bridges". The song is included on the 1986 compilation "Menlove Ave.", the 1990 boxset "Lennon", the 1998 boxset "John Lennon Anthology", the 2005 two-disc compilation "", and the 2010 boxset "Gimme Some Truth".
Document 3: Happiness Ltd. is the third studio album, and second major release since signing with Sire Records by Hot Hot Heat. The album was released on September 11, 2007. It is their first album without original member Dante DeCaro.
Question: Nobody Loves You was written by John Lennon and released on what album that was issued by Apple Records, and was written, recorded, and released during his 18 month separation from Yoko Ono?
Candidate Answer: The album issued by Apple Records, and written, recorded, and released during John Lennon's 18 month separation from Yoko Ono is Walls and Bridges. Nobody Loves You was written by John Lennon on Walls and Bridges album.
{ "answer": "Walls and Bridges", "citation": ["2"] }

Document 1: National Route 129 is a national highway of Japan connecting Hiratsuka, Kanagawa and Sagamihara, Kanagawa in Japan, with a total length of 31.7 km (19.7 mi). It junctions with the following routes: Japan National Route 16 in Sagamihara, Route 412 (Japan) and Japan National Route 246 in Atsugi, Kanagawa, and Japan National Route 1 and Japan National Route 134 in Hiratsuka, Kanagawa. Asides from the route running north to south, it also spans along some major highways: Harataima, Kenoatsugi and Ebina, Kanagawa IC in Keno Expressway, Atsugi, Kanagawa IC in Tōmei Expressway, Atsuginishi in Odawara-Atsugi Road road and Samukawaminami in Shin-Shōnan Bypass.
Document 2: National Route 13 (Vietnamese: "Quốc lộ 13") is a highway in southern Vietnam stretching from the northeastern outskirts of Ho Chi Minh City, the commercial centre of the country, towards the border to Cambodia. The highway starts around Thủ Đức on the northern outskirts of Ho Chi Minh City, once the site of the military academy of the Army of the Republic of Vietnam, and travels north through the provinces of Bình Dương and Bình Phước. The highway passes through the districts of Thuận An, Thủ Dầu Một town, Bến Cát, Chơn Thành, Đồng Phú, Bình Long, and Lộc Ninh.
Document 3: Cambodia (; Khmer: កម្ពុជា, or Kampuchea), officially known as the Kingdom of Cambodia (Khmer: ព្រះរាជាណាចក្រកម្ពុជា, "Preăh Réachéanachâk Kâmpŭchéa"), is a country located in the southern portion of the Indochina Peninsula in Southeast Asia. It is 181035 km2 in area, bordered by Thailand to the northwest, Laos to the northeast, Vietnam to the east, and the Gulf of Thailand to the southwest.
Question: What is known as the Kingdom and has National Route 13 stretching towards its border?
Candidate Answer: Cambodia is officially known as the Kingdom of Cambodia. National Route 13 stretches towards border to Cambodia.
{ "answer": "Cambodia", "citation": ["2", "3"] }

Document 1: A community of practice (CoP) is a group of people who share a craft or a profession. The concept was first proposed by cognitive anthropologist Jean Lave and educational theorist Etienne Wenger in their 1991 book "Situated Learning". Wenger then significantly expanded on the concept in his 1998 book "Communities of Practice".
Document 2: Route 413 is a highway in Missouri running between Route 13 in Springfield and Route 13 in Reeds Spring. It is an older alignment of Route 13 which was later rerouted. Except for two sections (in Springfield between Route 13 and U.S. Route 60 and about a mile between US 60 and Route 265 southwest of Billings), the road is runs concurrent with other designations for its entire length.
Document 3: Downhill is a British comedy film directed by James Rouse and written by Torben Betts about four old friends who reunite to walk the Coast to Coast Walk. It stars Richard Lumsden, Karl Theobald, Jeremy Swift and Ned Dennehy. It was produced by Benji Howell and is noted for its "innovative" release strategy.
Question: Jeremy Theobald and Christopher Nolan share what profession?
Candidate Answer: Jeremy Theobald is an actor and producer. Christopher Nolan is a director, producer, and screenwriter.
{ "answer": "Jeremy Theobald is an actor and producer. Christopher Nolan is a director, producer, and screenwriter.", "citation": [] }
'''.strip()



decompose_examples = {
    "hotpotqa": decompose_examples_hotpotqa,
    "2wikimultihopqa": decompose_examples_2wikimultihopqa,
    "musique": decompose_examples_musique
}

ground_examples = {
    "hotpotqa": ground_examples_hotpotqa,
    "2wikimultihopqa": ground_examples_hotpotqa,
    "musique": ground_examples_hotpotqa,
}