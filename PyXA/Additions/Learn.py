""".. versionadded:: 0.1.1

A collection of classes for interfacing with built-in ML/AI features in macOS.
"""

from typing import Union

import Foundation
import LatentSemanticMapping

from PyXA import XABase


class XALSM():
    def __init__(self, dataset: Union[dict[str, list[str]], None] = None, from_file: bool = False):
        """Initializes a Latent Semantic Mapping environment.

        :param dataset: The initial dataset, specified as a dictionary where keys are categories and values are list of corresponding texts, defaults to None. Cannot be None if from_file is False.
        :type dataset: Union[dict[str, list[str]], None], optional
        :param from_file: Whether the LSM is being loaded from a file, defaults to False. Cannot be False is dataset is None.
        :type from_file: bool, optional
        :raises ValueError: Either you must provide a dataset, or you must load an existing map from an external file

        :Example 1: Classify emails based on subject line

        >>> import PyXA
        >>> lsm = PyXA.XALSM({
        >>>     # 1
        >>>     "spam": ["Deals", "Holiday playbook", "Spend and save. You know the drill.", "Don't miss these holiday deals!", "GOOD NEWS", "you will never have an opportunity of this kind again", "Your Long Overdue Compensation Funds; Totally", "US $25,000,000.00", "goog day", "GOOD DAY, I am Mike Paul I have a", "enron methanol; meter # : 988291 this is a follow up to the note i gave you on monday , 4...", "hpl nom for january 9, see attached file : hplnol 09. xls", "neon retreat ho ho ho, we're around to that most wonderful time of the year", "photoshop, windows, office cheap, main trending abasements, darer prudently fortuitous", "re: indian springs this deal is to book the teco pvr revenue. it is my understanding that...", "noms / actual flow for 2 / we agree", "nominations for oct 21 - 23"],
        >>> 
        >>>     # 2
        >>>     "kayak": ["Price Alert: Airfare holding steady for your trip", "Prices going down for your Boston to Dublin flight", "Price Increase: Boston to Dublin airfare up $184", "Flight Alert: #37 decrease on your flight to Dublin.", "Flight Alert: It's time to book your flight to Dublin", "Price Alert: Airfare holding steady for your Bangor, ME to...", "Ready to explore the world again?"],
        >>> 
        >>>     # 3
        >>>     "lenovo": ["Doorbuster deals up to 70% off", "Visionary, On-Demand Content. Lenovo Tech World '22 is starting", "Up to 70% off deals 9 AM", "TGIF! Here's up to 70% off to jumpstart your weekend", "Top picks to refresh your workspace", "This only happens twice a year", "Think about saving on a Think PC", "Deep deals on Summer Clearance", "Save up to 67% + earn rewards", "Unlock up to 61% off Think PCs", "Giveaway alert!", "Annual Sale Sneak Peak Unlocked!"],
        >>> 
        >>>     # 4
        >>>     "linkedin": ["Here is the latest post trending amongst your coworkers", "Stephen, add Sean Brown to your network", "Share thoughts on LinkedIn", "Top companies are hiring", "Linkedin is better on the app", "Here is the latest post trending amongst your coworkers", "Stephen, add Ronald McDonald to your network", "James Smith shared a post for the first time in a while", "Here is the latest post trending amongst your coworkers", "You appeared in 13 searches this week", "you're on a roll with your career!", "You appeared in 16 searches this week", "18 people notices you", "You appeared in 10 searches this week", "Stephen, add Joe Shmoe to your network", "Your network is talking: The Center for Oceanic Research...", "thanks for being a valued member"]
        >>> })
        >>> print(lsm.categorize_query("New! Weekend-only deals"))
        >>> print(lsm.categorize_query("Stephen, redeem these three (3) unlocked courses"))
        >>> print(lsm.categorize_query("Round Trip From San Francisco to Atlanta"))
        [(3, 0.9418474435806274)]
        [(4, 0.9366401433944702)]
        [(2, 0.9944692850112915)]

        :Example 2: Use the Mail module to automate dataset construction

        >>> import PyXA
        >>> app = PyXA.Application("Mail")
        >>> junk_subject_lines = app.accounts()[0].mailboxes().by_name("Junk").messages().subject()
        >>> other_subject_lines = app.accounts()[0].mailboxes().by_name("INBOX").messages().subject()
        >>> 
        >>> dataset = {
        >>>     "junk": junk_subject_lines,
        >>>     "other": other_subject_lines
        >>> }
        >>> lsm = PyXA.XALSM(dataset)
        >>> 
        >>> query = "Amazon Web Services Billing Statement Available"
        >>> category = list(dataset.keys())[lsm.categorize_query(query)[0][0] - 1]
        >>> print(query, "- category:", category)
        >>> 
        >>> query = "Complete registration form asap receive your rewards"
        >>> category = list(dataset.keys())[lsm.categorize_query(query)[0][0] - 1]
        >>> print(query, "- category:", category)
        Amazon Web Services Billing Statement Available - category: other
        Complete registration form asap receive your rewards - category: junk

        .. versionadded:: 0.1.0
        """
        self.__categories = {}
        if dataset is None and not from_file:
            raise ValueError("You must either load a map from an external file or provide an initial dataset.")
        elif dataset is None:
            # Map will be loaded from external file -- empty dataset is temporary
            self.__dataset = {}
        else:
            # Create new map
            self.__dataset = dataset

            self.map = LatentSemanticMapping.LSMMapCreate(None, 0)
            LatentSemanticMapping.LSMMapStartTraining(self.map)
            LatentSemanticMapping.LSMMapSetProperties(self.map, {
                LatentSemanticMapping.kLSMSweepCutoffKey: 0,
                # LatentSemanticMapping.kLSMPrecisionKey: LatentSemanticMapping.kLSMPrecisionDouble,
                LatentSemanticMapping.kLSMAlgorithmKey: LatentSemanticMapping.kLSMAlgorithmSparse,
            })

            for category in dataset:
                self.__add_category(category)

            LatentSemanticMapping.LSMMapCompile(self.map)

    def __add_category(self, category: str) -> int:
        loc = Foundation.CFLocaleGetSystem()
        category_ref = LatentSemanticMapping.LSMMapAddCategory(self.map)
        self.__categories[category] = category_ref
        self.__categories[category_ref] = category_ref
        text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
        LatentSemanticMapping.LSMTextAddWords(text_ref, " ".join(self.__dataset[category]), loc, LatentSemanticMapping.kLSMTextPreserveAcronyms)
        LatentSemanticMapping.LSMMapAddText(self.map, text_ref, category_ref)
        return category_ref

    def save(self, file_path: Union[XABase.XAPath, str]) -> bool:
        """Saves the map to an external file.

        :param file_path: The path to save the map at
        :type file_path: Union[XABase.XAPath, str]
        :return: True if the map was saved successfully
        :rtype: bool

        :Example: Create a Reddit post classifier for gaming vs. productivity posts

        >>> import PyXA
        >>> lsm = PyXA.XALSM({
        >>>     # 1
        >>>     "gaming": ["If you could vote on the 2017 Mob Vote again, which mob would you choose this time and why?", "Take your time, you got this", "My parents (late 70s) got me a ps5 controller for Christmas. I do not own a playstation 5...", "I got off the horse by accident right before a cutscene in red dead", "boy gamer", "Minesweeper 99 x 99, 1500 mines. Took me about 2.5 hours to finish, nerve-wracking. No one might care, but just wanted to share this.", "The perfect cosplay doesn’t ex...", "'Play until we lose'", "Can we please boycott Star Wars battlefront 2", "EA removed the refund button on their webpage, and now you have to call them and wait to get a refund.", "Train Simulator is so immersive!", "Been gaming with this dude for 15 years. Since Rainbow Six Vegas on 360. I have some good gaming memories with him. He tried but couldn’t get one. Little did he know I was able to get him one. Looking forward to playing another generation with him.", "EA will no longer have exclusive rights of the Star Wars games", "A ziplining contraption I created with 1000+ command blocks", "The steepest walkable staircase possible in 1.16", "I made a texture pack that gives mobs different facial expressions. Should I keep going?"],
        >>> 
        >>>     # 2
        >>>     "productivity": ["Looking for an alarm app that plays a really small alarm, doesn’t need to be switched off and doesn’t repeat.", "I want to build a second brain but I'm lost and don't know where to start.", "noise cancelling earplugs", "I have so much to do but I don't know where to start", "How to handle stressful work calls", "time tracking app/platform", "We just need to find ways to cope and keep moving forward.", "Ikigai - A Reason for Being", "Minimalist Productivity Tip: create two users on your computer ➞ One for normal use and leisure ➞ One for business/work only. I have nothing except the essentials logged in on my work user. Not even Messages or YouTube. It completely revolutionized my productivity 💸", "Trick yourself into productivity the same way you trick yourself into procrastination", "I spent 40 hours sifting through research papers to fix my mental clarity, focus, and productivity - I ended up going down a rabbit hole and figuring out it was all tied to sleep, even though I felt I sleep well - here's what I found.", "The Cycle of Procrastination. Always a good reminder", "'Most people underestimate what they can do in a year, and overestimate what they can do in a day' - When you work on getting 1% better each day you won't even recognize yourself in a year."],
        >>> })
        >>> lsm.save("/Users/steven/Downloads/gaming-productivity.map")

        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, str):
            file_path = XABase.XAPath(file_path)

        status = LatentSemanticMapping.LSMMapWriteToURL(self.map, file_path.xa_elem, 0)
        if status == 0:
            return True
        return False

    def load(file_path: Union[XABase.XAPath, str]) -> 'XALSM':
        """Loads a map from an external file.

        :param file_path: The file path for load the map from
        :type file_path: Union[XABase.XAPath, str]
        :return: The populated LSM object
        :rtype: XALSM

        :Example: Using the gaming vs. productivity Reddit post map

        >>> import PyXA
        >>> lsm = PyXA.XALSM.load("/Users/steven/Downloads/gaming-productivity.map")
        >>> print(lsm.categorize_query("Hidden survival base on our server"))
        >>> print(lsm.categorize_query("Your memory is FAR more powerful than you think… school just never taught us to use it properly."))
        [(1, 0.7313863635063171)]
        [(2, 0.9422407150268555)]

        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, str):
            file_path = XABase.XAPath(file_path)

        new_lsm = XALSM(from_file=True)
        new_lsm.map = LatentSemanticMapping.LSMMapCreateFromURL(None, file_path.xa_elem, LatentSemanticMapping.kLSMMapLoadMutable)
        new_lsm.__dataset = {i: [] for i in range(LatentSemanticMapping.LSMMapGetCategoryCount(new_lsm.map))}
        new_lsm.__categories = {i: i for i in range(LatentSemanticMapping.LSMMapGetCategoryCount(new_lsm.map))}
        LatentSemanticMapping.LSMMapCompile(new_lsm.map)
        return new_lsm

    def add_category(self, name: str, initial_data: Union[list[str], None] = None) -> int:
        """Adds a new category to the map, optionally filling the category with initial text data.

        :param name: The name of the category
        :type name: str
        :param initial_data: _description_
        :type initial_data: list[str]
        :return: The ID of the new category
        :rtype: int

        :Example: Add a category for cleaning-related Reddit posts to the previous example

        >>> import PyXA
        >>> lsm = PyXA.XALSM.load("/Users/steven/Downloads/gaming-productivity.map")
        >>> lsm.add_category("cleaning", ["Curtains stained from eyelet reaction at dry cleaner", "How do I get these stains out of my pink denim overalls? from a black denim jacket that was drying next to them", "Cleaned my depression room after months 🥵", "Tip: 30 minute soak in Vinegar", "Regular floor squeegee pulled a surprising amount of pet hair out of my carpet!", "Before and after…", "It actually WORKS", "CLR is actually magic. (With some elbow grease)", "It was 100% worth it to scrape out my old moldy caulk and replace it. $5 dollars and a bit of time to make my shower look so much cleaner!", "Thanks to the person who recommended the Clorox Foamer. Before and after pics", "TIL you can dissolve inkstains with milk.", "Fixing cat scratch marks to couch using felting needle: Before and After", "Turns out BKF isn't a meme! Really satisfied with this stuff"])
        >>> print(lsm.categorize_query("Hidden survival base on our server"))
        >>> print(lsm.categorize_query("Your memory is FAR more powerful than you think… school just never taught us to use it properly."))
        >>> print(lsm.categorize_query("A carpet rake will change your life."))
        [(1, 0.7474805116653442)]
        [(2, 0.7167008519172668)]
        [(3, 0.797333300113678)]

        .. versionadded:: 0.1.0
        """
        LatentSemanticMapping.LSMMapStartTraining(self.map)

        if initial_data is None:
            initial_data = []

        if name in self.__dataset:
            raise ValueError("The category name must be unique.")

        self.__dataset[name] = initial_data
        category_ref = self.__add_category(name)
        LatentSemanticMapping.LSMMapCompile(self.map)
        return category_ref

    def add_data(self, data: dict[Union[int, str], list[str]]) -> list[int]:
        """Adds the provided data, organized by category, to the active map.

        :param data: A dictionary specifying new or existing categories along with data to input into them
        :type data: dict[Union[int, str], list[str]]
        :return: A list of newly created category IDs
        :rtype: int

        :Example: Classify text by language

        >>> import PyXA
        >>> lsm = PyXA.XALSM({})
        >>> lsm.add_data({
        >>>     # 1
        >>>     "english": ["brilliance outer jacket artist flat mosquito recover restrict official gas ratio publish domestic realize pure offset obstacle thigh favorite demonstration revive nest reader slide pudding symptom ballot auction characteristic complete Mars ridge student explosion dive emphasis the buy perfect motif penny a errand to fur far spirit random integration of with"],
        >>> 
        >>>     # 2
        >>>     "italian": ["da piazza proposta di legge legare nazionale a volte la salute bar farti farmi il pane aggiunta valore artista chiamata settentrionale scuro buio classe signori investitore in grado di fidanzato tagliare arriva successo altrimenti speciale esattamente definizione sorriso chiamo madre pulire esperto rurale vedo malattia era amici libertà l'account immaginare lingua soldi più perché"],
        >>> })
        >>> print(lsm.categorize_query("Here's to the crazy ones"))
        >>> print(lsm.categorize_query("Potete parlarmi in italiano"))
        [(1, 1.0)]
        [(2, 1.0)]

        .. versionadded:: 0.1.0
        """
        category_refs = []
        LatentSemanticMapping.LSMMapStartTraining(self.map)
        for category in data:
            if category not in self.__dataset:
                self.__dataset[category] = data[category]
                category_refs.append(self.__add_category(category))
            else:
                loc = Foundation.CFLocaleGetSystem()
                text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
                LatentSemanticMapping.LSMTextAddWords(text_ref, " ".join(data[category]), loc, LatentSemanticMapping.kLSMTextPreserveAcronyms)
                LatentSemanticMapping.LSMMapAddText(self.map, text_ref, self.__categories[category])
        LatentSemanticMapping.LSMMapCompile(self.map)
        return category_refs

    def add_text(self, text: str, category: Union[int, str], weight: float = 1):
        """Adds the given text to the specified category, applying an optional weight.

        :param text: The text to add to the dataset
        :type text: str
        :param category: The category to add the text to
        :type category: Union[int, str]
        :param weight: The weight to assign to the text entry, defaults to 1
        :type weight: float, optional
        :raises ValueError: The specified category must be a valid category name or ID

        :Example:

        >>> import PyXA
        >>> lsm = PyXA.XALSM({"colors": [], "numbers": ["One", "Two", "Three"]})
        >>> lsm.add_text("red orange yellow green blue purple", "colors")
        >>> lsm.add_text("white black grey gray brown pink", 1)
        >>> print(lsm.categorize_query("pink"))

        .. versionadded:: 0.1.0
        """
        LatentSemanticMapping.LSMMapStartTraining(self.map)
        if category not in self.__dataset and category not in self.__categories:
            raise ValueError(f"Invalid category: {category}")
            
        loc = Foundation.CFLocaleGetSystem()
        text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
        LatentSemanticMapping.LSMTextAddWords(text_ref, text, loc, LatentSemanticMapping.kLSMTextPreserveAcronyms)
        LatentSemanticMapping.LSMMapAddTextWithWeight(self.map, text_ref, self.__categories[category], weight)
        LatentSemanticMapping.LSMMapCompile(self.map)

    def categorize_query(self, query: str, num_results: int = 1) -> list[tuple[int, float]]:
        """Categorizes the query based on the current weights in the map.

        :param query: The query to categorize
        :type query: str
        :param num_results: The number of categorizations to show, defaults to 1
        :type num_results: int, optional
        :return: A list of tuples identifying categories and their associated score. A higher score indicates better fit. If not matching categorization is found, the list will be empty.
        :rtype: list[tuple[int, float]]

        :Example:

        >>> import PyXA
        >>> dataset = {
        >>>     # 1
        >>>     "color": ["red", "orange", "yellow", "green", "emerald", "blue", "purple", "white", "black", "brown", "pink", "grey", "gray"],
        >>> 
        >>>     # 2
        >>>     "number": ["One Two Three Four Five Six Seven Eight Nine Ten"]
        >>> }
        >>> lsm = PyXA.XALSM(dataset)
        >>> queries = ["emerald green three", "one hundred five", "One o' clock", "sky blue", "ninety nine", "purple pink"]
        >>> 
        >>> for query in queries:
        >>>     category = "Unknown"
        >>>     categorization_tuple = lsm.categorize_query(query)
        >>>     if len(categorization_tuple) > 0:
        >>>         category = list(dataset.keys())[categorization_tuple[0][0] - 1]
        >>>     print(query, "is a", category)
        emerald green three is a color
        one hundred five is a number
        One o' clock is a number
        sky blue is a color
        ninety nine is a number
        purple pink is a color

        .. versionadded:: 0.1.0
        """
        loc = Foundation.CFLocaleGetSystem()
        text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
        LatentSemanticMapping.LSMTextAddWords(text_ref, query, loc, 0)
        rows = LatentSemanticMapping.LSMResultCreate(None, self.map, text_ref, 10, LatentSemanticMapping.kLSMTextPreserveAcronyms)

        categorization = []
        num_results = min(num_results, LatentSemanticMapping.LSMResultGetCount(rows))
        for i in range(0, num_results):
            category_num = LatentSemanticMapping.LSMResultGetCategory(rows, i)
            score = LatentSemanticMapping.LSMResultGetScore(rows, i)
            categorization.append((category_num, score))
        return categorization
