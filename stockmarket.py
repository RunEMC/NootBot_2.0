import json
import threading
import random

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
priceFluctuationInterval = 10

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
        self.random = random
        self.random.seed()
        self.isShutDown = False

    def IPO(self, companyName):
        company = {
            "name": companyName,
            "price": self.baseIPOPrice
        }
        self.market[companyName] = company

    def buy(self, companyName, amount, availableFunds):
        company = self.market[companyName]
        return availableFunds >= company.price * amount

    def fluctuatePrices(self, interval = priceFluctuationInterval):
        if not self.isShutDown:
            threading.Timer(interval, self.fluctuatePrices).start()
            for company in self.market:
                if self.random.random() <= 0.5:
                    self.market[company]["price"] += 1
                else:
                    self.market[company]["price"] -= 1

    def shutDown(self):
        self.isShutDown = True


            
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
        finalMessage = "########## Companies ##########\n"
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
            try:
                companyName = commands[1]
                amount = int(commands[2])
                if companyName in market:
                    # Check profile and deduct funds
                    company = market[companyName]
                    profile = profiles[msgAuthor.id]
                    sharePrice = company["price"]
                    if profile["wallet"] >= amount * sharePrice:
                        # Buy shares
                        profile["wallet"] -= amount * sharePrice
                        if companyName in profile["investments"]:
                            profile["investments"][companyName] += amount
                        else:
                            profile["investments"][companyName] = amount
                        # Update local profile and json profile
                        profiles[msgAuthor.id] = profile
                        stockMarket.setProfiles(msgAuthor.id, profile)
                        await client.send_message(msgChannel, "You have purchased " + str(amount) + " shares of " + companyName + " stocks at $" + str(sharePrice) + " per share for $" + str(amount * sharePrice) + ". (Wallet: $" + str(profile["wallet"]) + ").")
                    else:
                        await client.send_message(msgChannel, "You can't afford this $" + str(amount * sharePrice) + " purchase.\nYour wallet balance is $" + str(profile["wallet"]))
                else:
                    await client.send_message(msgChannel, "Invalid company, type !sm list for companies and !sm help for help.")
            except:
                print("An error has occured")
                await client.send_message(msgChannel, "Invalid arguments for stock market, type !sm help for help.")

    elif commands[0] == "sell":
         # Check that there are enough args, !sm sell company amt needs 3 (less the one for !sm)
        if len(commands) <= 2:
            await client.send_message(msgChannel, "Invalid arguments for stock market, type !sm help for help.")
        else:
            # Check profile and sell shares
            try:
                companyName = commands[1]
                amount = int(commands[2])
                profile = profiles[msgAuthor.id]
                if companyName in profile["investments"]:
                    company = market[companyName]
                    sharePrice = company["price"]
                    if profile["investments"][companyName] >= amount:
                        # Sell shares
                        profile["wallet"] += amount * sharePrice
                        profile["investments"][companyName] -= amount
                        # Update local profile and json profile
                        profiles[msgAuthor.id] = profile
                        stockMarket.setProfiles(msgAuthor.id, profile)
                        await client.send_message(msgChannel, "You have sold " + str(amount) + " of " + companyName + "'s shares at $" + str(sharePrice) + " per share for $" + str(sharePrice * amount) + ". (Wallet: $" + str(profile["wallet"]) + ").")
                    else:
                        await client.send_message(msgChannel, "You don't have enough stocks to sell.\nYour currently own " + str(profile["investments"][companyName]) + " of " + companyName + "'s stocks.")
                else:
                    await client.send_message(msgChannel, "Invalid company, type !sm list for companies and !sm help for help.")
            except:
                print("An error occurred")
                await client.send_message(msgChannel, "Invalid arguments for stock market, type !sm help for help.")


# Print help message for Stock market
async def printHelp(channel, client):
    helpText = "This is a simulated stock market where you can buy and sell shares of companies\n" + "The share prices will change every hour, so make sure to trade before then\n"
    commandsList = "\n                ########## Commands ##########\n" + "- !sm list: Lists all the companies in the stock market and their share price\n" + "- !sm ipo company_name: (Admin only) IPO a company to list on the stock market\n" + "- !sm buy company_name amount: Attempt to purchase a certain amount of shares in a company\n" + "- !sm sell company_name amount: Attempt to sell a certain amount of shares in a company\n"
    await client.send_message(channel, "```" + helpText + commandsList + "```")

