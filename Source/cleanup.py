import motorFunctions

def emptyCleanup():
  return ("Deallocating project resources")


def cleanMotors():
  motorFunctions.stop1()
  motorFunctions.stop2()
  motorFunctions.destroy()
