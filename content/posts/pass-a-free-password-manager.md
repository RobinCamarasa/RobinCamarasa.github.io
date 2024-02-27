---
title: "A Free Password Manager"
date: 2022-09-03T08:22:00+02:00
draft: false
short: How I Learned to Stop Worrying and Love <a href="https://www.passwordstore.org/">pass</a>
tags: [cli, linux, security]
img: /lock.png
---

For all those years, my friends and colleagues used to make fun of people's digital security: "People are stupid. They use 12345678 as their main password." I was smiling and nodding, but deep down, I knew that having a [pawned mail address](https://haveibeenpwned.com/) and the same weak password on dozens of websites would not make me a poster boy for personal data security. I felt guilty about it, but I never really had the motivation to dive into it. However, one day, a colleague gave me the push I needed. We were at the coffee machine, and he explained to me that the Dutch government might create a law that makes employees responsible for the safety of their passwords. Losing my personal data really sucked, but losing my job and potentially being sued was too much of a risk. I had to do something and find a decent password manager!

## Wish list

Being specific about the programs and web services I use, I knew that I could not take the first password manager I found on Google and be done with it. I had to make sure that it could integrate nicely into my workflow and habits; otherwise, I would never use it. So I came up with a wish list.

As I try to integrate myself into my new country, the Netherlands, I am starting to become more and more frugal. So first, it **should not cost me a single penny**. Jokes aside, it is difficult from the customer's point of view to see the difference between a good and a bad password manager as the whole encryption is usually done on the back-end, keeping the user in the dark. This leads me to my second wish: I want to have **full control over the cryptography**; two reasons for that: I want to learn how cryptography works, and I want to trust the encryption. My third wish is **seamless terminal integration**, to get rid of hard-coded passwords in my shell scripts. Finally, I want a password manager that **works offline and syncs on all my devices**.

After searching on the internet, I settled on [pass](https://www.passwordstore.org/), the UNIX standard password manager that fulfilled all my requirements. Now, I just had to make it happen. So I gathered my courage, a cup of tea, and a [bar of chocolate](https://tonyschocolonely.com/us/en) and started configuring.

## Overview of the solution

Pass follows the UNIX philosophy, and as a consequence, it is designed to interact with other free software to offer as much flexibility as possible. My pipeline requires the following features:

- **Encryption and decryption of passwords**, handled by [gnupg](https://www.gnupg.org/)
- **Synchronization of the password database**, handled by [git](https://git-scm.com/)
- **A Command Line Interface**, handled by [pass](https://www.passwordstore.org/) itself
- **A Graphical User Interface**, shell script based on [dmenu](https://tools.suckless.org/dmenu/) integrated in [pass](https://www.passwordstore.org/)
- **A Terminal User Interface**, A handcrafted one-liner based on [fzf](https://github.com/junegunn/fzf)

## How I set it up on my Linux machine

- First, create the encryption keys. This can easily be achieved through a [gnupg](https://www.gnupg.org/) interactive prompt as follows:
```bash
gpg --full-generate-key
```
- Then, install [pass](https://www.passwordstore.org/) (the method depends on your distribution). Once installed, you can initialize it as follows:
```bash
pass init EMAIL-ADDRESS-GPG-KEY
```
- This initialization will create a `~/.password-store/` directory that will contain your encrypted passwords at the following location: `~/.password-store/PASSWORD-NAME.gpg`.

- Set up your remote repository on [GitHub](https://github.com/), [GitLab](https://gitlab.com/), or any remote location of your choice and link your local repository to your remote repository:
```bash
pass git init; pass git remote add origin REPO-URL
```
- Add your first password (or generate it):
```bash
pass edit -c PASSWORD-NAME # create password
pass generate -c PASSWORD-NAME # generate password
```

- Synchronize your local and your remote repositories:
```bash
pass git push -u origin main # or master if you did not make the switch
```
- You can now easily manage your encrypted passwords with version control as a bonus!

## Setting up on your Android device

**My setup might not be the easiest as it involves using the terminal on your phone; an android application is also available**: [Android-Password-Store](https://github.com/android-password-store/Android-Password-Store#readme)

This part of the installation assumes that you have already set up a Linux PC reachable via [ssh](https://en.wikipedia.org/wiki/Secure_Shell) that is on the same network as the Android device you want to set up.

- **On the Linux** PC, export your gpg key:
```bash
gpg --export-secret-keys --armor EMAIL-ADDRESS-GPG-KEY > ~/key.asc
```
- **On the android device**, install [termux](https://github.com/termux/termux-app#github), [termux-api](https://github.com/termux/termux-api) (advised to do it via f-droid as the version on the play store is not supported anymore). Then open the [termux](https://github.com/termux/termux-app#github) app and install the following packages:
```bash
pkg install gnupg pass fzf git openssh
```
- **On the android device**, clone the repository:
```bash
git clone REPO-URL ~/.password-store
```
- Copy the gpg key you exported from the **Linux PC** to the **android device**, import it, and finally delete it from the **android device**. This can be achieved with the following command line **on the android device**:
```bash
scp USERNAME@COMPUTER-IP:~/key.asc ./; gpg --import ~/key.asc; rm ~/key.asc
```
- Add a Terminal User Interface to copy your password to your **android device** clipboard easily:
```bash
echo "alias tpass=\"pass -c \\\$(find ~/.password-store/ -name '*.gpg' | sed -e 's:^.*password-store/\\\\(.*\\\\).gpg\\\$:\\\\1:g' | fzf)\"" >> ~/.bash_aliases; source ~/.bash_aliases
```
- **On the Linux PC**, delete the exported gpg key:
```bash
rm ~/key.asc
```
- You are all set to use passwords on your **android device**.

## Additional notes

- [pass](https://www.passwordstore.org/) also offers migration plans if you already have a password manager. (Check those migration plans on [pass website](https://www.passwordstore.org/))
- The community has implemented many compatible clients for all kinds of use cases (A list of those clients is available on the [pass website](https://www.passwordstore.org/))
