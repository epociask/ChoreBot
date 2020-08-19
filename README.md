# ChoreBot (An Automated Solution for Chore Management and Allocation for Rooomate Living)
Currently uses `python3.8` with Flask Server and Twilio SMS API to create automated SMS system for chore management, allocation, and verification through text messages to be shared amongst household members 


## Getting Started 

After cloning the repository follow these steps to get your own personal SMS chore manager 

1. Put your roommates information into the ROOMMATES variable within `config.env.template` and fill in the other environmental vars 
    - Roommates should be a JSON dict like `{"NAME_0": "phone_number",.... "NAME_N": "phone_number_n"}`
