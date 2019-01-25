import json

'''
# Company json format
{
    "company_name": {
        "name": "company_name",
        "price": 10
    }, ...
}

# Profiles json format
{
    "user-id": {
        "name": "RunEMC",
        "id": 1234567890,
        "wallet": 1000,
        "investments": {
            "companyA": 10, ...
        }
    }, ...
}
'''

# Global path variables
dirPath = "data/"
marketFile = "market.json"
proFile = "profiles.json"

# Global default variables
startingMoney = 500
companyStartPrice = 10

# Stock markeet for trades
class StockMarket():

    def getCompanies(self):
        return self.market

    def getProfiles(self):
        return self.profiles

    def setProfiles(self, id, profile):
        global dirPath
        global proFile
        self.profiles[id] = profile
        # Write profiles for persistence
        with open(dirPath + proFile, "w+") as outfile:
            json.dump(self.profiles, outfile, indent=4)

    def __init__(self):
        global dirPath
        global marketFile
        global proFile
        global companyStartPrice
        # print("New stock market created")
        self.baseIPOPrice = companyStartPrice
        with open(dirPath + marketFile) as infile:
            self.market = json.load(infile)
        with open(dirPath + proFile) as infile:
            self.profiles = json.load(infile)

    def IPO(self, companyName):
        company = {
            "name": companyName,
            "price": self.baseIPOPrice
        }
        self.market[companyName] = company

    def buy(self, companyName, amount, availableFunds):
        company = self.market[companyName]
        return availableFunds >= company.price * amount
            
# Interacts with the stockmarket based on command
async def processSMCommands(stockMarket, commands, message, client):
    msgContents = message.content
    msgChannel = message.channel
    msgAuthor = message.author

    # Get stockmarket info
    market = stockMarket.getCompanies()
    profiles = stockMarket.getProfiles()
    
    # Create a new profile for the author if they don't exist
    if msgAuthor.id not in profiles:
        global startingMoney
        profile = {
            "name": msgAuthor.name,
            "id": msgAuthor.id,
            "wallet": startingMoney,
            "investments": {}
        }
        stockMarket.setProfiles(msgAuthor.id, profile)

    # Error check and parse command
    if len(commands) <= 0:
        await client.send_message(msgChannel, "Invalid arguments for stock market, type !sm help for help.")
    
    elif commands[0] == "help":
        await printHelp(msgChannel, client)

    elif commands[0] == "list":
        # Setup the print message
        finalMessage = "                ########## Companies ##########\n"
        for company in market:
            finalMessage += market[company]["name"] + ": $" + str(market[company]["price"]) + "\n"
        # Send message
        await client.send_message(msgChannel, "```" + finalMessage + "```")

    elif commands[0] == "ipo":
        if len(commands) <= 1:
            await client.send_message(msgChannel, "Invalid arguments for stock market, type !sm help for help.")
        else:
            stockMarket.IPO(commands[1])
            # Write data to file
            with open("data/stockmarket/market.json", "w+") as outfile:
                json.dump(market, outfile, indent=4)
            await client.send_message(msgChannel, "New stock created: " + commands[1])

    elif commands[0] == "buy":
        # Check that there are enough args, !sm buy company amt needs 3 (less the one for !sm)
        if len(commands) <= 2:
            await client.send_message(msgChannel, "Invalid arguments for stock market, type !sm help for help.")
        else:
            company = commands[1]
            amount = commands[2]
            if company in market:
                # Check profile and deduct funds
                pass
            else:
                await client.send_message(msgChannel, "Invalid company, type !sm list for companies and !sm help for help.")

            

# Print help message for Stock market
async def printHelp(channel, client):
    helpText = "This is a simulated stock market where you can buy and sell shares of companies\n" + "The share price will change every 24 hours at 12:00am EST, so make sure to trade before then\n"
    commandsList = "\n                ########## Commands ##########\n" + "- !sm list: Lists all the companies in the stock market and their share price\n" + "- !sm ipo company_name: (Admin only) IPO a company to list on the stock market\n" + "- !sm buy company_name amount: Attempt to purchase a certain amount of shares in a company\n" + "- !sm sell company_name amount: Attempt to sell a certain amount of shares in a company\n"
    await client.send_message(channel, "```" + helpText + commandsList + "```")