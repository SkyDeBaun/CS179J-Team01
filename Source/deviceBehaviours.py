import subprocess

def picture():#TODO Implement callback funcitonality
  return

def stream():#TODO Implement callback functionality
  return

def video():#TODO Implement callback functionality
  return

topicDictionary = {
  "picture" : picture,
  "stream" : stream,
  "video" : video
  #FIXME Find some way to not hardcode value names
}


#https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute
#Maybe check if k is valid input
def generateCallbackFunction(k):
  return topicDictionary[k]
