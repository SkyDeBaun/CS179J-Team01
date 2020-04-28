import boto3
from boto3.dynamodb.conditions import Key, Attr

def printRow(table, entryNumber):
	# test that we can retrieve valid row in table by the row's primary key (entryNumber)
	response = table.query(
        KeyConditionExpression = Key("entryNumber").eq(entryNumber)
	)

	print(response["Items"])

def insertRow(table, columns, Primary_Column_Name, entryNumber, temperature, humidity):
	# test that we can insert a new row into table with a given primary key (entryNumber)

	response = table.put_item(
    		Item = {
        		Primary_Column_Name: entryNumber,
        		columns[0]: temperature,
        		columns[1]: humidity
		}
        )

def printAllRows(table):
	# print all table entries to test we inserted rows correctly
	# get all rows with a primary key (entryNumber) greater than or equal to 0 (so all of them)

	response = table.scan(
    		FilterExpression = Attr("entryNumber").gte(0)
	)

	for row in response["Items"]:
		print(row)

def deleteRow(table, Primary_Column_Name, entryNumber):
	# delete a row by primary key (entryNumber)
	response = table.delete_item(
		Key = {
			Primary_Column_Name: entryNumber
		}
	)

if __name__ == "__main__":
	# entryNumber is my primary key!
	# setup fields
	__TableName__ = "tempHumidityData"
	Primary_Column_Name = "entryNumber"
	columns = ["temperature", "humidity"]

	# resource and table
	DB = boto3.resource("dynamodb")
	table = DB.Table(__TableName__)

	# test insert row with entryNumber of 1
	entryNumber = 1
	testTemperature = 90
	testHumidity = 100
	insertRow(table, columns, Primary_Column_Name, entryNumber, testTemperature, testHumidity)

	# print that specific row to verify it was inserted into DynamoDB
	print("Table after inserting first row:")
	printRow(table, entryNumber)

	#insert second row
	entryNumber = 2
	testTemperature = 5
	testHumidity = 10
	insertRow(table, columns, Primary_Column_Name, entryNumber, testTemperature, testHumidity)
	print("Table after inserting second row:")
	printAllRows(table)

	# now delete row with entryNumber = 1 to verify we can delete rows
	entryNumber = 1
	deleteRow(table, Primary_Column_Name, entryNumber)

	# print all rows to verify row was deleted (should only see the row with entryNumber = 2)
	print("Table after deleting first row:")
	printAllRows(table)



