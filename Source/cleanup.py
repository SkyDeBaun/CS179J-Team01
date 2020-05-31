import motorFunctions

def emptyCleanup():
  print("Deallocating project resources")
  exit(0)


def cleanMotors():
  motorFunctions.stop1()
  motorFunctions.stop2()
  motorFunctions.destroy()