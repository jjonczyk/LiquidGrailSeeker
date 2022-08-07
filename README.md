# LiquidGrailSeeker

**Author:             Jakub Jonczyk  
Project made:       17.10.2020**  
Code updated:       7.08.2022  
Repository created: 25.08.2021  

---------------------------------

This app searches for best fresh craft beer releases and saves you a list to review. You can customize it a little bit!

### Requirements:
- Untappd account: `https://untappd.com/login` + your personal `client_id` and `client_secret` (please request Untappd for an API key)
- SendGrid account: `https://signup.sendgrid.com/` + SendGrid API key created + Sender Identity verified

### Prepare to use my app:
1. clone my repo 
2. install everything from `[GIT_ROOT]/requirements.txt` (if using pip, try: `pip install -r requirements.txt` in your venv)    
3. save your username to `[GIT_ROOT]/authentication/username.txt`    
4. save your `client_id` to `[GIT_ROOT]/authentication/client_id.txt`    
5. save your `client_secret` to `[GIT_ROOT]/authentication/client_secret.txt`    

### Usage:
The base command is `python grail_seeker.py` (launch it in your GIT root directory).    
It will run the app with the default config:    
`country='poland', options='newest', rating=3.80, logger='today'`.    
However, you can change those arguments on your own:
- `--country` [**poland**/global]
- `--options` [**newest**/top_rated] - sorting options
- `--min_rating` [**3.80**] - Minimal rating in float (out of 5.00) of your wanted feed, above 3.75 you shouldn't be dissapointed
- `--logger` [**today**] - default is the current date in the dd-mm-yyyy format, but you can specify any name you want

**BOLD** - defaults

Please, run `python grail_seeker.py --help` to read about some available options.

The daily feed data will be saved in the `[GIT_ROOT]/data/[country]/` directory with a specified `logger` in its name.

### Credits
My program builds the daily feed based on the Untappd data.    
However, I only use it as a research tool and don't ccreate my own database.   
    
![Optional Text](../main/assets/pbu_80_grey.png)
