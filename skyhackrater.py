category_weights = {
    "gameplay": 2.0,
    "story": 1.75,
    "sound": 1.5,
    "visuals": 1.25,
    "ui":0.75
}

class Question:
    def __init__(self, question:str, type:list[str], category:str, inverse=False, exclude_if_wip=False, 
                 only_wip=False, numeric=False, bonus=False, num_units=1.0) -> None:

        self.question = question
        if type == ["all"]:
            self.type = ["story", "mixed", "difficulty"]
        else:
            self.type = type
        self.category = category
        self.inverse = inverse
        self.exclude_if_wip = exclude_if_wip
        self.only_wip = only_wip
        self.numeric = numeric # numeric is implied bonus, ignores bonus flag
        self.bonus = bonus
        self.num_units = num_units

    def check(self) -> bool:
        """
        Checks if the question is valid.
        
        :return: True if valid
        :rtype: bool
        """
        for item in self.type:
            if item not in ["story", "mixed", "difficulty"]:
                print(f"ERR: {item} is an invalid type.")
                return False

        if self.category not in ["gameplay", "story", "visuals", "sound", "ui"]:
            print(f"ERR: {self.category} is an invalid category.")
            return False
        
        if self.question == "":
            print("Question Empty")
            return False
        
        if self.exclude_if_wip and self.only_wip:
            print("WIP exclusion and inclusion cannot be the same.")
            return False
        
        return True


    def ask(self, hack_type:str, wip:bool) -> bool:
        """
        Should this question be asked?
        
        :param hack_type: the hack's typ
        :type hack_type: str
        :param wip: is the hack a work in progress?
        :type wip: bool
        :return: True if valid to ask
        :rtype: boolF
        """
        if self.exclude_if_wip:
            if wip:
                return False
            
        if self.only_wip:
            if not wip:
                return False
        
        if hack_type not in self.type:
            return False
        
        return True
    
    def __str__(self) -> str:
        return self.question
    

questions:list[Question] = [
    Question("Is the creator actively involved/patching bugs?",
             ["all"],
             "gameplay"),

    Question("Are there frequent crashes or soft-locks?",
             ["all"],
             "gameplay",
             inverse=True,
             exclude_if_wip=True),  # Skip for WIPs (bugs are expected)

    Question("Are there noticeable graphical glitches?",
             ["all"],
             "visuals",
             inverse=True,
             exclude_if_wip=True),  # Skip for WIPs (visuals usually polished last)

    Question("Can you choose who you & your partner are?",
             ["all"],
             "gameplay",
             bonus=True),

    Question("Does the MC's dialog break immersion (if insertion story).",
             ["story", "mixed"],
             "story",
             inverse=True),

    Question("Is the dungeon \"Talk\" command updated?",
             ["story", "mixed"],
             "story"),

    Question("Is the overworld \"Talk\" command updated?",
             ["story", "mixed"],
             "story"),

    Question("Do characters' personalities evolve well overtime?",
             ["story", "mixed"],
             "story"),

    Question("Is the character dynamic enjoyable?",
             ["all"],
             "story"
             ),

    Question("Is the humor well timed?",
             ["story", "mixed"],
             "story"),

    Question("Did you like the humor?",
             ["story", "mixed"],
             "story"),

    Question("Does the story handle darker/mature themes with appropriate weight?",
             ["story", "mixed"],
             "story"),

    Question("Are side characters given personality beyond just quest-giving?",
             ["story", "mixed"],
             "story"),

    Question("Does the plot avoid feeling like padding or filler?",
             ["story", "mixed"],
             "story"),

    Question("Does the hack capture the charm of PMD?",
             ["story", "mixed"],
             "story"),

    Question("Does the title screen change based on progression?",
             ["story", "mixed"],
             "visuals",
             bonus=True),

    Question("Does Treasure Town have dynamic weather?",
             ["story", "mixed"],
             "visuals",
             bonus=True),

    Question("Are there custom portraits?",
             ["story", "mixed"],
             "visuals",
             bonus=True),

    Question("Do the portraits follow the PMD style?",
             ["story", "mixed"],
             "visuals",
             bonus=True),

    Question("Is the existing OST well used?",
             ["all"],
             "sound"),

    Question("How many custom songs are there?",
             ["all"],
             "sound",
             numeric=True),

    Question("Do custom songs loop properly?",
             ["all"],
             "sound"),

    Question("Is the Sky Jukebox available?",
             ["all"],
             "sound",
             bonus=True),

    Question("Does the Sky Jukebox contain custom music?",
             ["all"],
             "sound",
             bonus=True),

    Question("Are custom songs balanced well? (not too loud, not too quiet)",
             ["all"],
             "sound"),

    Question("Are there custom animations?",
             ["all"],
             "visuals",
             bonus=True),

    Question("Do custom animations follow the same PMD style?",
             ["all"],
             "visuals"),

    Question("Is the difficulty curve fair?",
             ["mixed", "difficulty"],
             "gameplay"),

    Question("Does the hack introduce new items?",
             ["all"],
             "gameplay",
             bonus=True),

    Question("Does the hack introduce new moves?",
             ["all"],
             "gameplay",
             bonus=True),

    Question("Are there scripted rooms in dungeons with clever puzzles? (Find an item to progress, etc).",
             ["all"],
             "gameplay",
             bonus=True),


    Question("Is gameplay/story balanced well?",
             ["mixed"],
             "gameplay"),

    # I personally prefer it, increases score if yes, doesn't decrease score if no
    Question("Does this hack retain the old move system?",
             ["all"],
             "gameplay",
             bonus=True),

    Question("Can you manually control teammates?",
             ["all"],
             "gameplay",
             bonus=True),

    Question("Do you get all tactics from the start?",
             ["all"],
             "gameplay",
             bonus=True),

    Question("Are there grinding segments if you get stuck? (Dungeons before bosses count)",
             ["all"],
             "gameplay"),
    
    Question("Can you skip cutscenes?",
             ["all"],
             "gameplay",
             bonus=True),

    Question("Are boss fights balanced (not just HP sponges)?",
             ["all"],
             "gameplay"),

    Question("Do Special Episodes world-build meaningfully?",
             ["story", "mixed"],
             "story"),
    
    Question("How many special episodes are there? (If difficulty hack, include if they are modified.)",
             ["story", "mixed", "difficulty"],
             "story",
             numeric=True),

    Question("Is the post game engaging/flows well with the main story?",
             ["story", "mixed"],
             "gameplay"),

    Question("Are there Easter Eggs or hidden interactions?",
             ["all"],
             "gameplay"),

    Question("Are there additional ways to spend Poké on other things apart from dungeon items?",
             ["all"],
             "gameplay"),

    Question("Is the Adventure Log updated to reflect the main and special stories?",
             ["story", "mixed"],
             "ui"),

    Question("Are there text formatting errors?",
             ["all"],
             "ui",
             exclude_if_wip=True,
             inverse=True),

    Question("Are there noticable spelling & grammar errors?",
             ["all"],
             "ui",
             exclude_if_wip=True,
             inverse=True),

    Question("Are there enough save points?",
             ["all"],
             "gameplay"),

    Question("How long is the story (in hours)?",
             ["all"],
             "story",
             numeric=True,
             num_units=0.5),

    Question("Was the game engaging?",
             ["all"],
             "gameplay"),

    Question("Does the story feel unique (not just EoS with a fresh coat of paint)?",
             ["story", "mixed"],
             "story"),
    
    Question("Did the hack flow well story-wise?",
             ["story", "mixed"],
             "story"),
    
    Question("Would you want to replay this hack?",
             ["all"],
             "gameplay"
             ),

    Question("Would you recommend this hack to someone else?",
             ["all"],
             "gameplay"
             )
]

# check if questions valid
ex:bool = False

for q in questions:
    if not q.check():
        print(f"Question [{q}] is invalid!")
        ex = True

if ex:
    exit(1)

# prompt user to select game type

hack_type:str = "mixed"
wip:bool = True

while True:

    print("\n--- PMD Sky Hack Rating Tool ---")
    print(f"Current Hack Type: {hack_type} | WIP?: {wip}")
    print("[1] Change Type")
    print("[2] Change WIP Status")
    print("[3] Start!")

    inp:str = input("Make a selection: ")

    if inp == "3": break
    elif inp == "1":
        print("\n--- Change Type ---")
        print("[1] Story")
        print("[2] Mixed (Base)")
        print("[3] Difficulty")
        print("[4] Back")
        inp = input("Make a selection: ")
        if inp == "1":
            hack_type = "story"
        elif inp == "2":
            hack_type = "mixed"
        elif inp == "3": 
            hack_type = "difficulty"
        else: continue
    elif inp == "2":
        print("\n--- Change WIP Status ---")
        print("[1] WIP")
        print("[2] Finished")
        print("[3] Back")
        inp = input("Make a selection: ")
        if inp == "1":
            wip = True
        elif inp == "2":
            wip = False
        else: continue



# calculate max score

max_score_nobono:float = 0

bonus_score:float = 0

for q in questions:

    if not q.ask(hack_type, wip): continue

    weight:float = category_weights[q.category]

    if q.numeric:
        bonus_score += ((5.0*q.num_units)*weight)
        continue
    if q.bonus:
        bonus_score += weight
        continue
    max_score_nobono += weight

old_max = max_score_nobono
# ask questions

score_earned:float = 0
bonus_earned:float = 0

for q in questions:

    if not q.ask(hack_type, wip): continue

    print("-----------------------")

    weight:float = category_weights[q.category]

    if q.numeric:
        try:
            ans = float(input(f"{q} (Enter number): "))*q.num_units
            bonus_earned += (min(ans, 5) * weight)
            continue
        except:
            bonus_earned += 0
            continue

    if q.bonus:
        ans = input(f"{q} (y/n/na): ").lower()
        if ans != "na" and ans != "":
            if q.inverse:
                if ans == "n":
                    bonus_earned += weight
            else:
                if ans == "y":
                    bonus_earned += weight
            continue
        else:
            bonus_score -= weight
            continue


    ans = input(f"{q} (y/n/na): ").lower()

    if ans != "na" and ans != "":
        if q.inverse:
            if ans == "n":
                score_earned += weight
        else:
            if ans == "y":
                score_earned += weight
        continue
    else:
        max_score_nobono -= weight

if max_score_nobono > 0:
    # grades
    score = (score_earned / max_score_nobono)*100
    if score >= 100: grade = "EX+"
    elif score >= 98: grade = "EX"
    elif score >= 95: grade = "SS"
    elif score >= 92: grade = "S"
    elif score >= 85: grade = "A"
    elif score >= 75: grade = "B"
    elif score >= 60: grade = "C"
    elif score >= 50: grade = "D"
    else: grade = "F"

    modifier = ""
    if (old_max / max_score_nobono) < 0.7:modifier = "?"
    elif bonus_score > 0:
        b_ratio = bonus_earned / bonus_score
        if b_ratio >= 0.7: modifier = "+"
        elif b_ratio <= 0.3: modifier = "-"


    final_rank = f"{grade}{modifier}"

    print("-----------------------")
    print(f"Final Score: {score_earned:.2f} / {max_score_nobono:.2f} ({score:.2f}%)")
    print(f"Bonus Score: {bonus_earned} / {bonus_score} ({(bonus_earned / bonus_score)*100:.2f}%)")
    print("-----------------------")
    print(f"Rank: {final_rank}")
else:
    print("All questions answered as N/A... cannot get grade")