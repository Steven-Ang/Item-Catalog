# Item Catalog
The web application is built with the Python web framework - Flask. The application supports the CRUD operations (Create, Read, Update, Delete) and uses Google OAuth provider for user authentication. Only authenticated users are allowed to perform CRUD operations.  

# Prerequisites:
### You will need to have following technologies to run this program:
* [Python 3](https://www.python.org/downloads/)
* [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)

# Installation Guide:
### Guide on Python:
1. Visit this [link](https://www.python.org/downloads/), find the latest version of Python 3 and download it.
2. Once it's finished, click on it.
3. Follow the instructions provided by the wizard (Before installing, make sure Python is inside the environment variable).
4. To check if Python is successfully installed into your computer, open up your terminal and type the following `python --version`. If it's successful, it will displays the version of the Python you're using.

### Guide on VM (Virtual Box):
1. Visit this [link](https://www.virtualbox.org/wiki/Downloads), find the host that is compatible with your operating system and download it.
2. Once it's finished, click on it.
3. Follow the instructions provided by the wizard.
4. Opening the software is not required, vagrant will do the work for it.

### Guide on Vagrant:
1. Visit this [link](https://www.vagrantup.com/downloads.html), find the package that is proper for your operating system and download it.
2. Once it's finished, click on it.
3. Follow the instructions provided by the wizard.
4. To check if it's successfully installed into your computer, open your terminal and type the following `vagrant --version`.
5. The rest of it will be cover in the **How To Run The Program** section.

# JSON Endpoints:
* **"/albums/JSON"** - Shows the data for all of the album
* **"/albums/<int:album_id>/JSON"** - Shows the data of the album associated with their ID

# How To Run The Program:
* If you haven't already, download all of the required technologies needed for this program from the **Installation Guide**.
* Download this repository or clone it by using the following command: `git clone https://github.com/Steven-Ang/Item-Catalog`
* Visit this [repository](https://github.com/udacity/fullstack-nanodegree-vm), download the folder or clone it by using the following command: `git clone https://github.com/udacity/fullstack-nanodegree-vm`
* Clone or download the folder from this repository, and move it to **catalog** folder from **FSND-Virtual-Machine**.
* Use the `vagrant up` inside the **vagrant folder**. Once it's finished, run `vagrant ssh` and `cd /vagrant`.
* Change directory to the **catalog** folder (make sure the folder from this repository is inside it) and run these three following commands in chronological order `python db_setup.py`, `python db_data.py` and finally to run the main program `python application.py`
* Feel free to play around with the application as much as you like!
