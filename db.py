import json
from mongoengine import connect, EmbeddedDocument, Document, IntField, BooleanField, EmbeddedDocumentListField, StringField

connect("scoutingDB")


class Game(EmbeddedDocument):
    autonomouse = BooleanField(required=True)
    score = IntField(required=True)
    bonusRP = BooleanField(required=True)
    climb = BooleanField(required=True)
    result = IntField(required=True)
    totalRP = IntField(required=True)
    gameNumber = IntField(default=0)


class Team(EmbeddedDocument):
    games = EmbeddedDocumentListField(Game)
    scoutTeamNumber = IntField(required=True)
    # update below
    totalGames = IntField(default=0)
    totalScore = IntField(default=0)
    scorePerGame = IntField(default=0)
    #
    winCount = IntField(default=0)
    loseCount = IntField(default=0)
    drawCount = IntField(default=0)
    #
    autonomouseCount = IntField(default=0)
    bonusRPCount = IntField(default=0)
    climbCount = IntField(default=0)
    #
    totalRP = IntField(default=0)


class Competetion(EmbeddedDocument):
    competetionName = StringField(required=True)
    teams = EmbeddedDocumentListField(Team)


class User(Document):
    teamNumber = IntField(required=True, unique=True)
    competetions = EmbeddedDocumentListField(Competetion)


def addUser(teamNumber):
    """add user(team) into db
    
    Arguments:
        teamNumber {int} -- your team number
    
    Returns:
        'done' or 'user already exist'
    """

    user = User.objects(teamNumber = teamNumber).first()
    if user:
        return 'user already exist'

    User(teamNumber=teamNumber).save()
    return 'done'


# returns competetion
def checkCompetetion(teamNumber, compName):
    """check if competition exist, if not then create one
    
    Arguments:
        teamNumber {int} -- your team number
        compName {string} -- competition name
    
    Returns:
        competition object -- the competition found/created
    """
    
    # checking user should not be needed if its for one team only
    user = User.objects(teamNumber=teamNumber).first()
    if not user:
        return 'team not exist'
    
    for comp in user.competetions:
        if comp.competetionName == compName:
            # has competetion already
            return comp
    # dont have competetion, need to create a new one
    newCompetetion = Competetion(competetionName=compName)
    user.competetions.append(newCompetetion)
    user.save()
    return newCompetetion


def checkScoutTeam(teamNumber, compName, scoutTeam):
    """check if team being scouted exist, if no then create one
    
    Arguments:
        teamNumber {int} -- your team number
        compName {string} -- competetion name
        scoutTeam {int} -- team being scouted
    
    Returns:
        team object -- the team found/created
    """

    # checking user should not be needed if its for one team only
    user = User.objects(teamNumber=teamNumber).first()
    if not user:
        return 'team not exist'
    
    # this should definitly return a competetion, because is called after checkCompetetion()
    for comp in user.competetions:
        if comp.competetionName == compName:
            for team in comp.teams:
                if team.scoutTeamNumber == scoutTeam:
                    # has team already
                    return team
            # dont have scoutTeam, need to create a new one
            newTeam = Team(scoutTeamNumber=scoutTeam)
            comp.teams.append(newTeam)
            user.save()
            return newTeam


def recordGame(teamNumber, compName, scoutTeam, auto, score, bonusRP, climb, result, totalRP):
    """store game result in db
    
    Arguments:
        teamNumber {int} -- your team number
        compName {string} -- the competetion name
        scoutTeam {int} -- team being scouted
        auto {boolean} -- did autonomous
        score {int} -- total score in game
        bonusRP {boolean} -- get bonus RP 
        climb {boolean} -- climbing
        result {int} -- 0 lose  1 draw  2 win
        totalRP {int} -- total RP earned
    
    Returns:
        'done' -- finished
        OR 
        ''(empty string) -- something wrong
    """    
    
    # competetion name not case sensitive 
    compName = compName.lower()
    
    # checking user should not be needed if its for one team only
    user = User.objects(teamNumber=teamNumber).first()
    if not user:
        return 'team not exist'
    
    checkCompetetion(teamNumber, compName)
    checkScoutTeam(teamNumber, compName, scoutTeam)
    # both competetion and scoutTeam should be in the db
    # update user object
    user = User.objects(teamNumber=teamNumber).first()
    
    # creat a new game
    newGame = Game(autonomouse=auto, score=score, climb=climb, bonusRP=bonusRP, result=result, totalRP=totalRP)

    for each in user.competetions:
        if each.competetionName == compName:
            for team in each.teams:
                if team.scoutTeamNumber == scoutTeam:
                    # should get in here for sure

                    team.totalGames += 1
                    team.totalScore += score
                    team.scorePerGame = int(team.totalScore / team.totalGames)

                    if result == 2:
                        team.winCount += 1
                    elif result == 1:
                        team.drawCount += 1
                    elif result == 0:
                        team.loseCount += 1

                    team.autonomouseCount += auto
                    team.bonusRPCount += bonusRP
                    team.climbCount += climb

                    team.totalRP += totalRP

                    newGame.gameNumber = team.totalGames
                    team.games.append(newGame)

                    user.save()
                    return 'done'

# user name (team number) shouldn't need to be checked here, since they can alreay log in 
def getCompetetions(teamNumber):
    user = User.objects(teamNumber=teamNumber).first()
    competetions = ''
    for comp in user.competetions:
        compName = comp.competetionName
        competetions += compName + ','
    competetions = competetions[:-1]
    return competetions


def getTeams(teamNumber, compName):
    compName = compName.lower()
    user = User.objects(teamNumber=teamNumber).first()
    teams = ''
    for comp in user.competetions:
        if comp.competetionName == compName:
            for team in comp.teams:
                teams += str(team.scoutTeamNumber) + ','
            teams = teams[:-1]
            break
    return teams


def getGeneralTeamInfo(teamNumber, compName, scoutTeam):
    compName = compName.lower()
    user = User.objects(teamNumber=teamNumber).first()
    teamInfo = ''
    for comp in user.competetions:
        if comp.competetionName == compName:
            for team in comp.teams:
                if team.scoutTeamNumber == scoutTeam:
                    teamInfo += 'totalGame:' + str(team.totalGames) + ','
                    teamInfo += 'scorePerGame:' + str(team.scorePerGame) + ','
                    teamInfo += 'winCount:' + str(team.winCount) + ','
                    teamInfo += 'loseCount:' + str(team.loseCount) + ','
                    teamInfo += 'drawCount:' + str(team.drawCount) + ','
                    teamInfo += 'autonomouseCount:' + str(team.autonomouseCount) + ','
                    teamInfo += 'bonusRPCount:' + str(team.bonusRPCount) + ','
                    teamInfo += 'climbCount:' + str(team.climbCount) + ','
                    teamInfo += 'totalRP:' + str(team.totalRP) + ','
                    teamInfo = teamInfo[:-1]
                    break
    return teamInfo


def getSpecificGameInfo(teamNumber, compName, scoutTeam, gameNum):
    compName = compName.lower()
    user = User.objects(teamNumber=teamNumber).first()
    gameInfo = ''
    for comp in user.competetions:
        if comp.competetionName == compName:
            for team in comp.teams:
                if team.scoutTeamNumber == scoutTeam:
                    for game in team.games:
                        if game.gameNumber == gameNum:
                            gameInfo += 'autonomouse:' + str(game.autonomouse) + ','
                            gameInfo += 'score:' + str(game.score) + ','
                            gameInfo += 'bonusRP:' + str(game.bonusRP) + ','
                            gameInfo += 'climb:' + str(game.climb) + ','
                            gameInfo += 'result:' + str(game.result) + ','
                            gameInfo += 'totalRP:' + str(game.totalRP) + ','
                            gameInfo = gameInfo[:-1]
                            break
    return gameInfo


if __name__ == '__main__':
    User.drop_collection()
    print(User.objects())
    addUser(7476)

    recordGame(7476, 'carleton', 1111, True, 50, True, True, 2, 4)
    recordGame(7476, 'carleton', 1111, False, 13, False, False, 1, 1)
    recordGame(7476, 'carleton', 22, False, 70, True, False, 0, 1)
    recordGame(7476, 'carleton', 2706, True, 31, False, True, 2, 3)
    recordGame(7476, 'northbay', 921, True, 50, True, True, 2, 4)
    recordGame(7476, 'northbay', 641, False, 13, False, False, 1, 1)
    recordGame(7476, 'northbay', 1310, False, 70, True, False, 0, 1)
    recordGame(7476, 'northbay', 1310, True, 31, False, True, 2, 3)

    # print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4))

    print(getCompetetions(7476))
    print(getTeams(7476, 'carleton'))
    print(getGeneralTeamInfo(7476, 'carleton', 1111))
    print(getSpecificGameInfo(7476, 'carleton', 1111, 2))


# teamNumber, compName, scoutTeam, auto, score, bonusRP, climb, result, totalRP
#   7476,     'carleton', 1111,    True,   50,    True,   True,   2,       4
# 'teamNumber: 7476, compName: Carleton, scoutTeam: 5024, auto: true, score: 100, bonusRP: true, climb: true, result: 2, totalRP:4'
