from datetime import datetime
from datetime import timedelta
from datetime import date
from functions import *

######### Seting Up Time Span to train data #########

timeFormat = '%Y-%m-%d %H:%M:%S'
trainFromLastDate, trainUntilToday = False, False

# leave these open if trainFromLastDate and trainUntilToday are true
start = datetime.strptime('2021-06-14 23:59:45', timeFormat)
end = datetime.strptime('2021-06-16 23:59:45', timeFormat)

# get last or today as date if setted up
if trainUntilToday:
    end = datetime.strptime(date.today().strftime(timeFormat), timeFormat)

if trainFromLastDate:
    with open('lastTrainingDateTime.txt') as f:
        start = datetime.strptime(f.readlines()[0], timeFormat)

####### Seting Up Time intervals for Evaluation #######

# time for prediction to be done in minutes
timePredict = 30
# total hours influencing the prediction
totalTime = 3
# time between evaluations in minutes
everyTime = 30
# feature every x minutes (less than one hour please)
minutesBetween = 10

######### Iterating over data and training AI #########
numberOfFeatures = int(totalTime / (minutesBetween / 60))

dir = []
# get list of json files, make sure only raw data is available in working directory
for directories in os.listdir():
    if len(directories.split('.')) == 2 and directories.split('.')[1] == 'json':
        dir += [directories]

for day in dir:
    timeOfFile = datetime.strptime(day.split('.')[0], '%Y-%m-%d')
    if start <= timeOfFile <= end:
        # read .json data file created by scraping if between time intervall and remove timezone for every tweet
        tweets_df = pd.read_json(day, lines=True)
        tweets_df['date'] = tweets_df['date'].apply(removeTz)

        # start everyday at 3 pm and end everyday at 23 am
        startingTime = datetime.strptime(day.split('.')[0] + ' 03:00:00', timeFormat).replace(tzinfo=None)
        endingTime = datetime.strptime(day.split('.')[0] + ' 23:00:00', timeFormat).replace(tzinfo=None)
        while startingTime <= endingTime:
            counter, results, tempTime = 0, [], startingTime
            # iterate over all features and build data
            while counter < numberOfFeatures:
                lastTime  = tempTime
                tempTime = tempTime - timedelta(minutes =  minutesBetween)
                
                # create time interval for picking tweets
                temp = tweets_df[tempTime <= tweets_df.date]
                temp = temp[tweets_df.date <= lastTime]
                
                # use textbob for creating data and evaluate them
                temp["Auswertung"] = temp["content"].apply(cleanTwt).apply(getPolarity).apply(getSentiment)
                results += getResults(temp) #[p,t,n,sum]

                #TODO: score average for POS, NEU, NEG and add it to results
                counter += 1
            startingTime = startingTime + timedelta(minutes = everyTime)
            print(results)