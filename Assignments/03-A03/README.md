## Assignment 3 - Create your own server.
#### Due: 02-13-2023 (Monday @ 2:30 p.m.)

-----


### 1. [Github Developr Pack](https://education.github.com/pack)

Sign for the Github Student Developer Pack to try an receive free digital ocean credits to pay for your server.

### 2. [Sign up @ Digital Ocean](https://cloud.digitalocean.com/registrations/new) for Digital Ocean.

Create an account at DO if you don't have one.

### 3. Create a Droplet

Choose the cheapest version of Ubuntu 22~. If you want to pay extra for more memory etc., its up to you. I linked to a few tutorials below.

Use the tutorial below to get started: 
- https://docs.digitalocean.com/products/droplets/how-to/create/

- https://www.digitalocean.com/community/tutorials/how-to-set-up-an-ubuntu-20-04-server-on-a-digitalocean-droplet

- https://www.youtube.com/watch?v=kzThZOZj1S4


### 4. IP Address & Password

- The IP address that is assigned to your "droplet", is your only connection to your server.
- The root password was chosen when you create your droplet.
- You need both IP address & password to access your new server.

### 5. Accessing Your Server

- Open some type of "terminal" (like [putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) or [gitbash](https://git-scm.com/downloads) or [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)) and log into your server using:
    - The IP address given to you
    - The password you picked
- Changing your password:
    - Run the following command (note: the dollar `$` sign just implies "command line", don't use it in the command):
    - `$ passwd`
    - Follow the prompts.

#### 6. Basic necessary packages:

```bash
# update the package repositories
$ sudo apt-get update

# actually update any out of data packages
$ sudo apt-get upgrade

# install git a distributed version control system  
$ apt install git
$ apt install python3.10-venv

```

#### 6. Testing Your Server

For a later assignment...
