decompose_examples_hotpotqa = '''
Input:
Question: Which magazine was started first, Arthur's Magazine or First for Women?
New one thought/answer pair:
Thought 1: First, When Arthur's Magazine started? What year did Arthur's Magazine begin publication? 
Answer 1: Arthur's Magazine was an American literary periodical published in Philadelphia, which started in **19th (1844)**.

Input:
Question: Who was the captain of the only battleship to provide gunfire support during the Vietnam War?
Thought 1: Who was the captain of the battleship that provided gunfire support during the Vietnam War?
Answer 1: Rear Adm. J. (October 23, 1924 – November 4, 2007) was notable as the captain of the battleship USS "New Jersey" during that ship's deployment to the Vietnam War in 1968. 
New one thought/answer pair:
Thought 2: I have got all the information. And **Rear Adm. J.** is the captain providing gunfire support during the Vietnam War?`
Answer 2: FINISH[Rear Adm. J.]

Input:
Question: What is one of the stars of The Newcomers known for?
Thought 1: Who are the stars in Newcomers? Who are the notable actors featured in The Newcomers?
Answer 1: **Chris Evans** is one of the stars in the Newcomers.
Thought 2: Chris Evans is one of the star in The Newcomers. What is the Chris Evans known for? What are his most famous roles?
Answer 2: Chris Evans is known for **superhero roles as the Marvel Comics**
New one thought/answer pair:
Thought 3: I have got all the information. Chris Evans is a star in Newcomers, who is known for **superhero roles as the Marvel Comics**
Answer 3: FINISH]Superhero roles as the Marvel Comics]

Input:
Question: Billy Preston is an American college basketball player for a team that competes in what? Which team does Billy Preston represent?
Thought 1: Billy Preston is an American college basketball player. What does Billy Preston play for?
Answer 1: Billy Preston is an American college basketball player for the **Kansas Jayhawks**.
Thought 2: Kansas Jayhawks is an American college basketbal team. What does the Kansas Jayhawks compete for? What conference do they play in?
Answer 2: Kansas Jayhawks competes for the **Big 12 Conference**
New one thought/answer pair:
Thought 3: I have got all the information. Billy Preston play for Kansas Jayhawks, and Kansas Jayhawks competes for the **Big 12 Conference**
Answer 3: FINISH[The Big 12 Conference]
'''.strip()

decompose_examples_2wikimultihopqa = '''
Input:
Question: What is the place of birth of the composer of film Kaayamkulam Kochunniyude Makan?
New one thought/answer pair:
Thought 1: Who is the composer of the film Kaayamkulam Kochunniyude Makan? Who composed the music for Kaayamkulam Kochunniyude Makan?
Answer 1: The composer of the film Kaayamkulam Kochunniyude Makan is M. K. Arjunan.

Input:
Question: Are Bipradash Barua and Henk Wijngaard from the same country?
Thought 1: What is the nationality of Bipradash Barua? Which country Bipradash Barua is from? Where does Bipradash Barua come from?
Answer 1: Bipradash Barua is a Bangladeshi novelist.
New one thought/answer pair:
Thought 2: What is the nationality of Henk Wijngaard? Which country Henk Wijngaard is from?  Where does Henk Wijngaard come from?
Answer 2: Henk Wijngaard is a Dutch country singer.

Input:
Question: Are Gavlimak and Berušica located in the same country?
Thought 1: Where is Gavlimak located? What is the geographical location of Gavlimak?
Answer 1: Gavlimak is a village in Chehel Shahid Rural District, in the Central District of Ramsar County, Mazandaran Province, Iran.
Thought 2: Where is Berušica located? Which country Berušica is found in?
Answer 2: Berušica is a village in the municipality of Trebinje, Republika Srpska, Bosnia and Herzegovina.
New one thought/answer pair:
Thought 3: Are Iran and Bosnia and Herzegovina the same country?
Answer 3: No, Iran and Bosnia and Herzegovina are two different countries.

Input:
Question: What is the place of birth of the director of film The Seven Madmen?
Thought 1: Who is the director of the film "The Seven Madmen"? Who directed The Seven Madmen?
Answer 1: The director of "The Seven Madmen" is Leopoldo Torre Nilsson.
Thought 2: Where was Leopoldo Torre Nilsson born? What is Leopoldo Torre Nilsson's birthplace?
Answer 2: Leopoldo Torre Nilsson was born in Buenos Aires, as mentioned in the supporting fact that he died in his native Buenos Aires in 1978.
New one thought/answer pair:
Thought 4: What is the final answer to the question about the place of birth of the director of "The Seven Madmen"?
Answer 4: FINISH[Buenos Aires]

Input:
Question: Are the directors of films The Super Cops and Dick Tracy (1990 Film) both from the same country?
Thought 1: Who is the director of The Super Cops? Who directed The Super Cops?
Answer 1: The director of The Super Cops is Gordon Parks.
Thought 2: What is the nationality of Gordon Parks? What country did Gordon Parks come from?
Answer 2: Gordon Parks was an American photographer, musician, writer, and film director.
Thought 3: Who is the director of Dick Tracy (1990 Film)? Who directed the 1990 movie Dick Tracy?
Answer 3: The director of Dick Tracy (1990 Film) is Warren Beatty.
Thought 4: What is the nationality of Warren Beatty? Where is Warren Beatty from?
Answer 4: Warren Beatty is an American actor and filmmaker.
New one thought/answer pair:
Thought 5: Are both directors from the same country? Do both directors share the same nationality?
Answer 5: FINISH[yes]
'''.strip()

decompose_examples_musique = """
Input:
Question: Where is the headquarters of located of the 48th Highlanders of the country which released the performer of As Seen Through Windows?
New one thought/answer pair:
Thought 1: What country released the performer of "As Seen Through Windows"? From what country does the musician who performed 'As Seen Through Windows' originate?
Answer 1: The performer of "As Seen Through Windows" is Bell Orchestre, a band from Montreal, Quebec, Canada. Therefore, the country is Canada.

Input:
Question: Who is the spouse of the director of The Yellow Ticket?
Thought 1: Who is the director of The Yellow Ticket? Who helmed the film The Yellow Ticket?
Answer 1: The director of The Yellow Ticket is Raoul Walsh, as mentioned in the supporting fact about the film.
New one thought/answer pair:
Thought 2: Who is the spouse of Raoul Walsh? Who was Raoul Walsh married to?
Answer 2: According to the supporting fact about the film "Betrayed," Raoul Walsh worked with Miriam Cooper, who is his spouse. This is inferred from the context of their collaboration and historical records.

Input:
Question: Where is the district in which Latrigg is located in the UK?
Thought 1: What is the county where Latrigg is located? In which county can Latrigg be found?
Answer 1: Latrigg is located entirely within the county of Cumbria.
Thought 2: Is Latrigg part of a larger district or national park? Does Latrigg belong to a broader protected area or administrative region?
Answer 2: The first supporting fact also states that all the land in England higher than 3,000 feet (910 m) above sea level lies within the National Park, which includes the Lake District. Latrigg is part of the Lake District, as it is one of the fells there.
New one thought/answer pair:
Thought 3: What is the final answer to the question?
Answer 3: FINISH[county of Cumbria]

Input:
Question: What county shares a border with the county where Bill Short was born?
Thought 1: Where was Bill Short born? What is Bill Short's birthplace?
Answer 1: Bill Short was born in Kingston, New York.
Thought 2: Which county is Kingston, New York located in? In what county can Kingston, New York, be found?
Answer 2: Kingston is a town in Ulster County, New York.
Thought 3: Which county shares a border with Ulster County, New York? What neighboring county borders Ulster County, New York?
Answer 3: The supporting fact mentions that the hamlet of Chichester, New York, is right next to the borderline between Ulster County and Greene County, indicating that Greene County shares a border with Ulster County.
New one thought/answer pair:
hought 4: What county shares a border with the county where Bill Short was born?
Answer 4: FINISH[Greene County]
""".strip()

ground_examples_hotpotqa = '''
Input:
Question: Eleanor McGovern was the wife of the Senator who was the presidential nominee in what year?
Document 1: Jim Bright is an Australian organisational psychologist and Professor of Career Education and Development at Australian Catholic University (ACU) National. He authored the Chaos Theory of Careers with Robert Pryor.
Document 2: Wade Watts (23 September 1919 – 13 December 1998) was an African American gospel preacher and civil rights activist from Oklahoma. He served as the state president of the Oklahoma chapter of the NAACP for sixteen years, challenging the Ku Klux Klan through Christian love doctrine. He worked with Thurgood Marshall and developed a friendship with Martin Luther King during the American civil rights movement, and has been cited as a mentor by the current leader of the NAACP in Oklahoma, Miller Newman, and his nephew, former congressman, J. C. Watts.
Document 3: India is a federal union comprising twenty-nine states and seven union territories, for a total of 36 state and union territories. The states and union territories are further subdivided into districts and further into smaller administrative divisions.
Thought : Who was the Senator that Eleanor McGovern was married to?
Old Answer: Eleanor McGovern was married to George Stanley McGovern, who served as a U.S. Senator from South Dakota from 1955–1977.
New answer and supporting fact ids:
New answer: Eleanor McGovern was married to George Stanley McGovern, who served as a U.S. Senator from South Dakota from 1955–1977. No document is relevant to thought and old answer.
Supporting fact ids: 

Input:
Question: The Wild Wacky Wonderful World of Winter had a co-star in which actress from the sitcom "Alice"?
Document 1: Elizabeth "Beth" Howland (May 28, 1941 – December 31, 2015) was an American actress. She worked on stage and television and was best known for playing Vera Gorman in the sitcom "Alice", inspired by the Martin Scorsese film "Alice Doesn't Live Here Anymore" (1974).
Document 2: The 2010 Emory Healthcare 500 was a NASCAR Sprint Cup Series stock car race that was held on September 5, 2010 at Atlanta Motor Speedway in Hampton, Georgia. Contested over 325 laps, it was the twenty-fifth race of the 2010 Sprint Cup Series season. The race was won by Tony Stewart, for the Stewart Haas Racing team. Carl Edwards finished second, and Jimmie Johnson, who started seventh, clinched third.
Document 3: George Stanley McGovern (July 19, 1922 – October 21, 2012) was an American historian, author, U.S. Representative, U.S. Senator, and the Democratic Party presidential nominee in the 1972 presidential election.
Thought: Who played a notable role in the sitcom "Alice"?
Old answer: Linda Lavin played Vera Gorman in the sitcom "Alice".
New answer and supporting fact ids:
New answer: Elizabeth "Beth" Howland played Vera Gorman in the sitcom "Alice", according to the supporting fact.
Supporting fact ids: 1

Input:
Question: What team defeated the Philadelphia Phillies in 4 games, and plays in the Yankee Stadium?
Document 1: "Snow White" is a 19th-century German fairy tale which is today known widely across the Western world. The Brothers Grimm published it in 1812 in the first edition of their collection "Grimms' Fairy Tales". It was titled in German: Sneewittchen (in modern orthography "Schneewittchen") and numbered as Tale 53. The name "Sneewittchen" was Low German and in the first version it was translated with "Schneeweißchen". The Grimms completed their final revision of the story in 1854.
Document 2: Yankee Stadium was a stadium located in the Bronx, a borough of New York City. It was the home ballpark of the New York Yankees, one of the city's Major League Baseball (MLB) franchises, from 1923 to 1973 and then from 1976 to 2008. The stadium hosted 6,581 Yankees regular season home games during its 85-year history. It was also the former home of the New York Giants football team from 1956 through the first part of the 1973–74 football season. The stadium's nickname, "The House That Ruth Built", is derived from Babe Ruth, the baseball superstar whose prime years coincided with the stadium's opening and the beginning of the Yankees' winning history. It has also been known as "The Big Ballpark in The Bronx", "The Stadium", and "The Cathedral of Baseball".
Document 3: The 1950 New York Yankees season was the 48th season for the team in New York and its 50th overall as a franchise. The team finished with a record of 98–56, winning their 17th pennant, finishing 3 games ahead of the Detroit Tigers. In the World Series, they defeated the Philadelphia Phillies in 4 games. New York was managed by Casey Stengel. The Yankees played at Yankee Stadium.
Document 4: Group Captain Geoffrey Leonard Cheshire, Baron Cheshire (7 September 1917 – 31 July 1992) was a highly decorated World War II Royal Air Force pilot and philanthropist.
Thought : Which team defeated the Philadelphia Phillies in 4 games in the World Series?
Old answer: The 1950 Brooklyn Dodgers defeated the Philadelphia Phillies in 4 games in the World Series.
New answer and supporting fact ids:
New answer: The 1950 New York Yankees defeated the Philadelphia Phillies in 4 games in the World Series, as mentioned in the supporting fact.
Supporting fact ids: 2, 3
'''.strip()

ground_examples_2wikimultihopqa = '''
Input:
Question: What is the place of birth of the composer of film Kaayamkulam Kochunniyude Makan?
Document 1: Bipradash Barua( born 1940) is a Bangladeshi novelist. He was awarded Bangla Academy Literary Award in 1991 and Ekushey Padak in 2014.
Document 2: Berušica is a village in the municipality of Trebinje, Republika Srpska, Bosnia and Herzegovina.
Document 3: The Seven Madmen (also known as The Revolution of the Seven Madmen) is a 1973 Argentine drama film directed by Leopoldo Torre Nilsson and starring Alfredo Alcón, Norma Aleandro and Héctor Alterio. It was based on the novels "Los siete locosThe Seven Madmen") and "Los lanzallamasThe Flamethowers"), by Roberto Arlt. The film was entered into the 23rd Berlin International Film Festival, where it won the Silver Bear Award.
Thought: Who is the composer of the film Kaayamkulam Kochunniyude Makan?
Old answer: The composer of the film Kaayamkulam Kochunniyude Makan is Ilaiyaraaja.
New answer and supporting fact ids:
New answer: The composer of the film Kaayamkulam Kochunniyude Makan is Ilaiyaraaja. No document is relevant to thought and old answer.
Supporting fact ids: 

Input:
Question: What is the date of death of Quentin Metsys The Younger's father?
Document 1: Erle C. Kenton (August 1, 1896 – January 28, 1980) was an American film director. He directed 131 films between 1916 and 1957. He was born in Norborne, Missouri and died in Glendale, California from Parkinson's disease. Kenton and Edward Ludwig were the principal directors of the 1958-1960 CBS television series, "The Texan", starring Rory Calhoun as Bill Longley, a "Robin Hood of the West", who drifts through the region helping persons in need.
Document 2: Peter Németh( born 14 September 1972) is a retired Slovak football player of Hungarian ethnic origin. Németh played for several top Slovak clubs during his career, including Inter Bratislava and MŠK Žilina. He also spent one season playing for Czech team Baník Ostrava. Since 2001 he played mostly in Germany. Németh was also a regular for the Slovakia national football team.
Document 3: Quentin Metsys the Younger (Quinten or Massys; c. 1543 – 1589) was a Flemish Renaissance painter, one of several of his countrymen active as artists of the Tudor court in the reign of Elizabeth I of England. He was the son of Flemish painter Jan Massys, Matsys, or Metsys and the grandson and namesake of Quentin Massys or Metsys. The younger Quentin was born in Antwerp, where he joined the Guild of St. Luke in 1574; by c. 1581 he was living in London, likely having fled religious persecution in Antwerp as his father and uncle had done. He left England for Frankfurt in 1588 and died there the next year. He is best known for the "Sieve Portrait" of Elizabeth I, in which she is depicted as Tuccia, a Vestal Virgin who proved her chastity by carrying water from the Tiber River to the Temple of Vesta without spilling a drop. Elizabeth is surrounded by symbols of empire, including a column and a globe, iconography that would appear again and again in her portraiture of the 1580s and 1590s, most notably in the "Armada Portrait" of 1588.
Thought: Who is Quentin Metsys The Younger's father?
Old answer: Quentin Metsys The Younger's father is Pieter Bruegel the Elder, a famous Dutch painter.
New answer and supporting fact ids:
New answer: Jan Massijs or Jan Matsys died on 8 October 1575, according to the supporting fact "Dcument 3".
Supporting fact ids: 3

Input:
Question: Where was the husband of Susan Buffett born?
Document 1: Warren Edward Buffett (born August 30, 1930) is an American business magnate, investor, and philanthropist, who is the chairman and CEO of Berkshire Hathaway. He is considered one of the most successful investors in the world and has a net worth of US$88.9 billion as of December 2019, making him the fourth-wealthiest person in the world. Buffett was born in Omaha, Nebraska. He developed an interest in business and investing in his youth, eventually entering the Wharton School of the University of Pennsylvania in 1947 before transferring and graduating from the University of Nebraska at the age of 19. He went on to graduate from Columbia Business School, where he molded his investment philosophy around the concept of value investing that was pioneered by Benjamin Graham. He attended New York Institute of Finance to focus his economics background and soon after began various business partnerships, including one with Graham. He created Buffett Partnership, Ltd in 1956 and his firm eventually acquired a textile manufacturing firm called Berkshire Hathaway, assuming its name to create a diversified holding company. In 1978, Charlie Munger joined Buffett and became vice chairman of the company. Buffett has been the chairman and largest shareholder of Berkshire Hathaway since 1970. He has been referred to as the "Oracle" or "Sage" of Omaha by global media outlets. He is noted for his adherence to value investing and for his personal frugality despite his immense wealth. Research published at the University of Oxford characterizes Buffett's investment methodology as falling within "founder centrism" – defined by a deference to managers with a founder's mindset, an ethical disposition towards the shareholder collective, and an intense focus on exponential value creation. Essentially, Buffett's concentrated investments shelter managers from the short-term pressures of the market. Buffett is a notable philanthropist, having pledged to give away 99 percent of his fortune to philanthropic causes, primarily via the Bill & Melinda Gates Foundation. He founded The Giving Pledge in 2009 with Bill Gates, whereby billionaires pledge to give away at least half of their fortunes. He endorsed Democratic candidate Hillary Clinton in the 2016 U.S. presidential election and will judge current U.S. President Donald Trump by his results on national safety, economic growth and economic participation when deciding if he will vote for him in the 2020 U.S. presidential election.
Document 2: Muskurahat is a 1992 Hindi-language Indian feature film directed by Priyadarshan, starring Jay Mehta, Revathi, Amrish Puri, Anil Dhawan, Sharat Saxena, Annu Kapoor and Jagdeep. The film is the remake of Priyadarshan's own Malayalam blockbuster "Kilukkam" starring Mohanlal and Revathi, and was initially supposed to have Aamir Khan and Pooja Bhatt in the lead.
Document 3: Band -e Lal Mohammad is a village in Nosratabad Rural District, in the Central District of Zahedan County, Sistan and Baluchestan Province, Iran. At the 2006 census, its population was 25, in 5 families.
Document 4: Susan Thompson Buffett (June 15, 1932 – July 29, 2004) was an American activist for the causes of civil rights, abortion rights and birth control, and the first wife of investor Warren Buffett. She was a director of Berkshire Hathaway, owning 2.2 percent (worth US$3 billion in 2004) of the company at the time of her death, and was the 153rd richest person in the world. She was president of the Buffett Foundation, which has contributed millions of dollars to educational groups, medical research, family planning groups and other charities.
Thought: Where was the husband of Susan Buffett born?
Old answer: Warren Buffett was born in New York City, New York, as stated in the supporting fact about his life and career.
New answer and supporting fact ids:
New answer: Warren Buffett was born in Omaha, Nebraska, as stated in the supporting fact about his life and career, according to supporing facts.
Supporting fact ids: 1, 4
'''.strip()

ground_examples_musique = '''
Input:
Question: Who founded the publisher of Journal of Bisexuality?
Document 1: As Seen Through Windows is the second album by Canadian band Bell Orchestre. It was recorded at Soma Electric Studios in Chicago, IL.
Document 2: Betrayed (1917) is a silent drama film directed and written by Raoul Walsh, starring Hobart Bosworth, Miriam Cooper, and Monte Blue, and released by Fox Film Corporation. It is not known if the film currently survives, which suggests that it is a lost film.
Document 3: It is located entirely within the county of Cumbria, and all the land in England higher than 3,000 feet (910 m) above sea level lies within the National Park, including Scafell Pike, the highest mountain in England. It also contains the deepest and longest bodies of water in England, respectively Wast Water and Windermere.
Thought: Who is the publisher of the Journal of Bisexuality?
Old answer: The Journal of Bisexuality is published by the Oxford University Press.
New answer and supporting fact ids:
New answer: The Journal of Bisexuality is published by the Oxford University Press. No document is relevant to thought and old answer.
Supporting fact ids: 

Input:
Question: When was the city where Howdy Holmes was born founded?
Document 1: Andrzej Strug, real name Tadeusz (or Stefan) Gałecki (sources vary; 28 November 1871/1873 in Lublin – 9 December 1937 in Warsaw) was a Polish socialist politician, publicist and activist for Poland's independence. He was also a freemason and declined the offer to join the prestigious Polish Academy of Literature, upset by official criticism of the movement.
Document 2: Howard "Howdy" S. Holmes (born December 14, 1947, Ann Arbor, Michigan), is a former driver in the CART Championship Car series. He began racing in the early 1970s and was based in Stockbridge, Michigan, about northeast of Chelsea, Michigan where his family owned a milling company.
Document 3: Being 1,000 miles (1,609 km) from any large body of water (with the exception of Lake Superior), temperatures and precipitation in North Dakota can vary widely. North Dakota is far enough north to experience − 60 ° F (− 51 ° C) temperatures and blizzards during the winter months, but far enough south to experience 121 ° F (49 ° C) temperatures and tornado outbreaks in the summer. The 181 ° F degree (100 ° C) variation between North Dakota's highest and lowest temperature is the 3rd largest variation of any U.S. State, and the largest of any non-mountainous state.
Thought: Where was Howdy Holmes born?
Old answer: Howdy Holmes was born in Detroit, Michigan.
New answer and supporting fact ids:
New answer: Howdy Holmes was born in Ann Arbor, Michigan, according to the supporting fact.
Supporing fact ids: 2

Input:
Question: How many states are there in the country that Ghee is from?
Document 1: Ghee (Sanskrit: Ghṛta), is a class of clarified butter that originated in ancient India. It is commonly used in Middle Eastern cuisine, cuisine of the Indian subcontinent, Southeast Asian cuisine, traditional medicine, and religious rituals.
Document 2: The Government of India (ISO: Bhārat Sarkār), often abbreviated as GoI, is the union government created by the constitution of India as the legislative, executive and judicial authority of the union of 29 states and seven union territories of a constitutionally democratic republic. It is located in New Delhi, the capital of India.
Document 3: Avalau is an islet within the atoll of Funafuti, Tuvalu. Charles Hedley described Avalau in 1896 "this islet is said to possess a spring of fresh water".
Thought: How many states are there in the country that Ghee is from?
Old answer: The Government of India is the authority over 25 states and five union territories.
New answer and supporting fact ids:
New answer: Ghee originated in ancient India. The Government of India is the authority over 29 states and seven union territories.
Supporing fact ids: 1,2
'''.strip()

decompose_examples = {
    "hotpotqa": decompose_examples_hotpotqa,
    "2wikimultihopqa": decompose_examples_2wikimultihopqa,
    "musique": decompose_examples_musique
}

ground_examples = {
    "hotpotqa": ground_examples_hotpotqa,
    "2wikimultihopqa": ground_examples_2wikimultihopqa,
    "musique": ground_examples_musique,
}