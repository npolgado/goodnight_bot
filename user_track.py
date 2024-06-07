
# used to determine score, most rare is more points
GOODNIGHT_WEIGHT = 0.25
REAL_LATE_WEIGHT = 3
RARE_GOODNIGHT_WEIGHT = 1
REACTION_WEIGHT = 0.5

class User:
    def __init__(self, name, goodnights:int=0, real_late:int=0, rare_goodnights:int=0, reactions:int=0):
        self.name = name
        self.real_late = real_late # times the bot yelled at you for being up late
        self.goodnights = goodnights # times the bot has said goodnight to you
        self.rare_goodnights = rare_goodnights # times the bot has a little extra to say! 
        self.reactions = reactions # times the bot has reacted to your messages

        self.score = self.get_score()

    def get_score(self): return (GOODNIGHT_WEIGHT * self.goodnights) + (REAL_LATE_WEIGHT * self.real_late) + (RARE_GOODNIGHT_WEIGHT * self.rare_goodnights)
    def __str__(self): return f'{self.name} has {self.goodnights} goodnights, {self.real_late} real late hours, and {self.rare_goodnights} rare goodnights'
    def __repr__(self): return f'User({self.name}, {self.goodnights}, {self.real_late}, {self.rare_goodnights})'

class ActivityTracker:
    def __init__(self):
        self.users = {}

    def add_user(self, user_name, goodnights=0, real_late=0, rare_goodnights=0, reactions=0):
        if user_name in self.users:
            self.users[user_name].goodnights += goodnights
            self.users[user_name].real_late += real_late
            self.users[user_name].rare_goodnights += rare_goodnights
            self.users[user_name].reactions += reactions
            self.users[user_name].score = self.users[user_name].get_score()
        
        else:
            self.users[user_name] = User(user_name)
    
    def get_scores(self):
        return sorted(self.users.values(), key=lambda x: x.score, reverse=True)