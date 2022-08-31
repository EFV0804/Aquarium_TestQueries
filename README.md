# Prism/Aquarium API
## Description
This is the first draft of an API between the HoursTracker Prism Plugin and the Aquarium API and MeshQL queries.

So far, it is only utility functions for basic Aquarium queries. I've included some keys to run the test queries in 'useful_keys.txt'.
## Requirements
You need to add your credentials to a .env file to connect to the Aquarium data base and do queries. The .env file should look like this:
        
            AQ_USER = {email login}
            AQ_PASSWORD = {password}
            SERVER = 'https://cloud-api.fatfish.app/v1'


The script uses the dotenv module to load the variables in the .env file and use them in the code.

The Aquarium API is also required to communicate with the Aquarium data base.

To add the required modules, from a CLI pointing to the module directory:

            pip install -r requirements.txt
            
            
 ## Credit
- [MenhirFX](https://menhirfx.com/fr)
- [Aquarium API and MeshQL](https://docs.fatfish.app/dev/python/index.html)
