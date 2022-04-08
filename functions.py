import os
import re
import pandas as pd
from textblob import TextBlob

# funtion to remove timezone
def removeTz(twt):
    return twt.replace(tzinfo=None)

# Create a  function to clean the tweets
def cleanTwt(twt):
    twt = re.sub("#bitcoin", "bitcoin", twt) #removes the hashtah from bitcoin
    twt = re.sub("#Bitcoin", "bitcoin", twt) #removes the hashtag from Bitcoin
    twt = re.sub("#[A-Za-z0-9]+", "", twt)   # removes any strings with a #
    twt = re.sub("\\n", "", twt) # removes the "\n" string
    twt = re.sub("https?:\/\/\S+", "", twt) #removes any hyperlinks
    return twt

# create a function to get the polarity
def getPolarity(twt):
    return TextBlob(twt).sentiment.polarity
    
# create a function to get the text sentiment
def getSentiment(score):
    if score<0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"

def getResults(df):
    # in case of no values in dataframe to skip error
    try:
        p = df["Auswertung"].value_counts().Positive
    except:
        p = 0
    try:
        t = df["Auswertung"].value_counts().Neutral
    except:
        t = 0
    try:
        n = df["Auswertung"].value_counts().Negative
    except:
        n = 0    
    sum = p + t + n
    return [p,t,n,sum]