# Introduction
![](https://lh3.googleusercontent.com/B1D56wJ8UfDs1aizfZXuPBSB27_lLDdMZj_4ViXkAZeedmu01QzXE5_c0udcVT633HJvXR8jNNv2=s300 "mcdowell_icon")

McDowell is a discord bot that will solve all of your custom reaction needs. Ever wanted to respond with a cat picture whenever someone asked you what your pet looks like? Or respond with your Youtube playlist when someone craves a set of good songs? You can do that.

 But i get what you're thinking, what distinguishes this bot from the others that have a reaction feature implemented? That's simple, McDowell...

 1. **Allows you to manage commands in a user friendly way**. No more weird command inputs with quotes and the like.
 2. **Detects keyword in a message in a smart way**. While other bots only respond if you have the keyword *stand-alone in a message, with nothing written after it*, McDowell can detect a keyword *anywhere in your message no matter what's written next to it*. A small difference, but it can mean a lot when you just want your reaction bot to do its job, and not having to spend effort to get it to respond.
 3. **Has a random chance system**. Having your bot *always* respond could get tiring very quickly, depending on the content. That is why McDowell will only respond if it exceeds a certain percentage. In case the default doesn't percentage doesn't suit you, the chance is fully customizable, for both messages and urls!

And a whole lot more! To invite the bot to your server click [
this link.](https://discordapp.com/api/oauth2/authorize?client_id=386627978618077184&permissions=0&scope=bot)

# Under the hood

McDowell is open-source, which means you are free to take this code, make some modifications, and run it yourself. In case you want to host it yourself though, there are a few things to take care of.

 1. Create a discord bot application, and retrieve its token. This will go in the secrets.py file.
 2. Setup your PostgreSQL database (other database should work, but might require some code tweaking).  The structure of the database can be deferred from the model classes in the code. But if that's too much work, there's also a [database creation script](https://gist.github.com/MichaelVerdegaal/624a31cf72143a4463de2170d7aeca0b) available (Postgres only).
 3. Build your database url, and put it in secrets.py. 
 4. Run main.py to start the bot.

### Heroku

The bot was initially built to be hosted on Heroku. If you want to host your bot on there as well, the steps are slightly different. 

 1. Get the bot token (same as before)
 2. Install the Heroku PostgreSQL database extension. Your database url can be found in the config vars tab.
 3. Put the token in as a new config var (name = TOKEN).
 4. Setup the database structure.
 5. Link your code to a valid repository (E.G Github)
 6. Deploy it.

A few things to note afterwards. If you don't host your bot on heroku, you won't need some files, namely "Procfile" and "runtime.txt".

### Dependencies

Major:

 - Discord.py (Rewrite branch)
 - SQLALchemy

Minor:

 - psycopg2-binary (for SQLALchemy)
 - requests
 - validators
 
 # Contact and issues

If you encounter any problems or have a cool suggestion, please make a new issue on this GitHub repository, if you can't figure that out, message All#9999 on Discord.
