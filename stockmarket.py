
# Companies
class Company():

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def __init__(self, name, price):
        self.name = name
        self.price = price


# Stock markeet for trades
class StockMarket():

    def __init__(self):
        print("New stock market created")
        self.baseIPOPrice = 10
        self.market = {}

    def IPO(self, companyName):
        company = Company(companyName, 10)
        self.market[companyName] = company

    def getCompanies(self):
        return self.market

    def buy(self, companyName, amount, availableFunds):
        company = self.market[companyName]
        return availableFunds >= company.price * amount
            
# Interacts with the stockmarket based on command
async def processSMCommands(stockMarket, commands, message, client):
    msgContents = message.content
    msgChannel = message.channel
    msgAuthor = message.author
    
    if len(commands) <= 0:
        await client.send_message(msgChannel, "Invalid arguments for stock market")
    
    elif commands[0] == "list":
        # Get the companies
        market = stockMarket.getCompanies()
        # Setup the print message
        finalMessage = "########## Companies ##########\n"
        for company in market:
            finalMessage += market[company].getName() + ": $" + str(market[company].getPrice()) + "\n"
        # Send message
        await client.send_message(msgChannel, "```" + finalMessage + "```")

    elif commands[0] == "ipo":

        if len(commands) <= 1:
            await client.send_message(msgChannel, "Invalid arguments for stock market")
        else:
            stockMarket.IPO(commands[1])
            await client.send_message(msgChannel, "New stock created: " + commands[1])
