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
    User(teamNumber=teamNumber).save()


# returns competetion
def checkCompetetion(teamNumber, compName):
    '''
    return the competetion object 
    '''

    # checking user should not be needed if its for one team only
    user = User.objects(teamNumber=teamNumber).first()
    # if not user:
    #     return 'team not exist'
    #
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
    '''
    return the scouting team object
    '''

    # checking user should not be needed if its for one team only
    user = User.objects(teamNumber=teamNumber).first()
    # if not user:
    #     return 'team not exist'
    #
    # this should definitly return a competetion
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
    '''
    record game data
    '''
    # checking user should not be needed if its for one team only
    user = User.objects(teamNumber=teamNumber).first()
    if not user:
        return 'team not exist'
    #
    checkCompetetion(teamNumber, compName)
    checkScoutTeam(teamNumber, compName, scoutTeam)
    # both competetion and scoutTeam should be in the db
    # update user object
    user = User.objects(teamNumber=teamNumber).first()
    # creat a new game
    newGame = Game(autonomouse=auto, score=score, climb=climb,
                   bonusRP=bonusRP, result=result, totalRP=totalRP)

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


def getCompetetions(teamNumber):
    user = User.objects(teamNumber=teamNumber).first()
    competetions = ''
    for comp in user.competetions:
        compName = comp.competetionName
        competetions += compName + ','
    competetions = competetions[:-1]
    return competetions


def getTeams(teamNumber, compName):
    user = User.objects(teamNumber=teamNumber).first()
    teams = ''
    for comp in user.competetions:
        if comp.competetionName == compName:
            for team in comp.teams:
                teams += str(team.scoutTeamNumber) + ','
            teams = teams[:-1]
            return teams


def getGeneralTeamInfo(teamNumber, compName, scoutTeam):
    user = User.objects(teamNumber=teamNumber).first()
    info = ''
    for comp in user.competetions:
        if comp.competetionName == compName:
            for team in comp.teams:
                if team.scoutTeamNumber == scoutTeam:
                    info += 'totalGame:' + str(team.totalGames) + ','
                    info += 'scorePerGame:' + str(team.scorePerGame) + ','
                    info += 'winCount:' + str(team.winCount) + ','
                    info += 'loseCount:' + str(team.loseCount) + ','
                    info += 'drawCount:' + str(team.drawCount) + ','
                    info += 'autonomouseCount:' + \
                        str(team.autonomouseCount) + ','
                    info += 'bonusRPCount:' + str(team.bonusRPCount) + ','
                    info += 'climbCount:' + str(team.climbCount) + ','
                    info += 'totalRP:' + str(team.totalRP) + ','
                    info = info[:-1]
                    return info


def getSpecificGameInfo(teamNumber, compName, scoutTeam, gameNum):
    user = User.objects(teamNumber=teamNumber).first()
    info = ''
    for comp in user.competetions:
        if comp.competetionName == compName:
            for team in comp.teams:
                if team.scoutTeamNumber == scoutTeam:
                    for game in team.games:
                        if game.gameNumber == gameNum:
                            info += 'autonomouse:' + \
                                str(game.autonomouse) + ','
                            info += 'score:' + str(game.score) + ','
                            info += 'bonusRP:' + str(game.bonusRP) + ','
                            info += 'climb:' + str(game.climb) + ','
                            info += 'result:' + str(game.result) + ','
                            info += 'totalRP:' + str(game.totalRP) + ','
                            info = info[:-1]
                            return info


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
