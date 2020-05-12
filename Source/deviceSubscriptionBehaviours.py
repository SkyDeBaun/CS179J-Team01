import subprocess

def picture(client, userdata, message):#TODO Implement callback funcitonality
#  print("picture topic subscribed fired beep boop beep")
#  print(message.payload) 
  return

def stream(client, userdata, message):#TODO Implement callback functionality
  return

def video(client, userdata, message):#TODO Implement callback functionality
  return

subscribedTopicDictionary = {
  "picture" : picture,
  "stream" : stream,
  "video" : video
  #FIXME Find some way to not hardcode value names
}


#https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute
#Maybe check if k is valid input
def generateCallbackFunction(k):
  return subscribedTopicDictionary[k]
