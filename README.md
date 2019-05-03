# CSDMS clinic

This repository houses materials used at the 2019 CSDMS annual meeting, in a clinic called "Developing and teaching interactive sedimentology and stratigraphy computer activities".

## Abstract

In this clinic, we will first demonstrate existing interactive computer-based activities used for teaching concepts in sedimentology and stratigraphy.
This will be followed by a hands-on session for creating different modules based on the participants’ teaching and research interests.
Active learning strategies improve student exam performance, engagement, attitudes, thinking, writing, self-reported participation and interest, and help students become better acquainted with one another (Prince, 2004).
Specifically, computer-based active learning is an attractive educational approach for post-secondary educators, because developing these activities takes advantage of existing knowledge and skills the educator is likely to already have.

The demonstration portion of the clinic will focus on the existing rivers2stratigraphy (https://github.com/sededu/rivers2stratigraphy) activity, which illustrates basin-scale development of fluvial stratigraphy through adjustments in system kinematics including sandy channel migration and subsidence rates.
The activity allows users to change these system properties, so as to drive changing depositional patterns.
The module utilizes a rules based model, which produces realistic channel patterns, but simplifies the simulation to run efficiently, in real-time.
The clinic will couple rivers2stratigraphy to a conventional laboratory activity which interprets an outcrop photograph of fluvial stratigraphy, and discuss logistics of using the module in the classroom.

For the second part of the clinic, familiarity with Python will be beneficial (but is not required); we will utilize existing graphical user interface (GUI) frameworks in developing new activities, aimed to provide a user-friendly means for students to interact with model codes while engaging in geological learning. 
Participants should plan to have Python installed on their personal computers prior to the workshop, and a sample module will be emailed beforehand to let participants begin exploring the syllabus.

Prince, M. (2004). Does Active Learning Work? A Review of the Research. Journal of Engineering Education, 93(3), 223-231. doi: 10.1002/j.2168-9830.2004.tb00809.x.


## Installing and running the modules

This modules depends on Python 3, `tkinter`, and the Python packages `numpy`, `scipy`, `matplotlib`, and `shapely`. 

### Installing Python 3

If you are new to Python, it is recommended that you install Anaconda, which is an open source distribution of Python which includes many basic scientific libraries, some of which are used in the module. 
Anaconda can be downloaded at https://www.anaconda.com/download/ for Windows, macOS, and Linux. 
If you do not have storage space on your machine for Anaconda or wish to install a smaller version of Python for another reason, see below on options for Miniconda or vanilla Python.

1. Visit the website for Anaconda https://www.anaconda.com/download/ and select the installer for your operating system.
__Be sure to select the Python 3.x installation.__
2. Start the installer.
3. If prompted, select to "install just for me", unless you know what you are doing.
4. When prompted to add Anaconda to the path during installation, select _yes_ if you __know__ you do not have any other Python installed on your computer; otherwise select _no_.

See below for detailed instructions on installing `rivers2stratigraphy` for your operating system.

