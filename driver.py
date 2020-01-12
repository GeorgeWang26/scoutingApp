import db


print('\n\nthis driver has 4 function\n\n')
print('competetions(teamNumber)     ->      all the competetions a team has attended\n')
print('teams(teamNumber, competetionName)       ->      all the teams participated in the competetion\n')
print('generalTeamInfo(teamNumber, competetionName, scoutingTeamNumber)     ->      general informations for the selected team\n')
print('detailedGameInfo(teamNumber, competetionName, scoutingTeamNumber, competetionNumber)     ->      specific game data of a team\n')
print('\n\n\nteamNumber is your own team number\n')
print('competetionName is the name of the competetions you want to check data in\n')
print('scoutingTeamNumber is the team number of the team you want to get information on\n')
print('competetionNumber is the number of competetions you want to get for a specific team\n\n')


def competetions(teamNumber):
    result = db.getCompetetions(teamNumber)
    if result == None:
        print('invalid input, check your input')
        return
    result = result.replace(',', '\n')
    print(result)


def teams(teamNumber, competetionName):
    result = db.getTeams(teamNumber, competetionName)
    if result == None:
        print('invalid input, check your input')
        return
    result = result.replace(',', '\n')
    print(result)


def generalTeamInfo(teamNumber, competetionName, scoutingTeamNumber):
    result = db.getGeneralTeamInfo(
        teamNumber, competetionName, scoutingTeamNumber)
    if result == None:
        print('invalid input, check your input')
        return
    result = result.replace(',', '\n')
    result = result.replace(':', ': ')
    print(result)


def detailedGameInfo(teamNumber, competetionName, scoutingTeamNumber, competetionNumber):
    result = db.getSpecificGameInfo(
        teamNumber, competetionName, scoutingTeamNumber, competetionNumber)
    if result == None:
        print('invalid input, check your input')
        return
    result = result.replace(',', '\n')
    result = result.replace(':', ': ')
    print(result)
