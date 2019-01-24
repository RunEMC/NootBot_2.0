import json

# Company json format
'''
{
    "company_name": {
        "name": "company_name",
        "price": 10
    },
    ...
}

'''

# Stock markeet for trades
class StockMarket():

    def __init__(self):
        print("New stock market created")
        self.baseIPOPrice = 10
        with open("data/stockmarket/market.json") as infile:
            self.market = json.load(infile)

    def IPO(self, companyName):
        company = {
            "name": companyName,
            "price": 10
        }
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
            finalMessage += market[company]["name"] + ": $" + str(market[company]["price"]) + "\n"
        # Send message
        await client.send_message(msgChannel, "```" + finalMessage + "```")

    elif commands[0] == "ipo":

        if len(commands) <= 1:
            await client.send_message(msgChannel, "Invalid arguments for stock market")
        else:
            stockMarket.IPO(commands[1])
            # Write data to file
            with open("data/stockmarket/market.json", "w+") as outfile:
                json.dump(stockMarket.getCompanies(), outfile)
            await client.send_message(msgChannel, "New stock created: " + commands[1])
