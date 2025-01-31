
# Bootcamp Respository

This repository contains exercise documents and relevant files for all the sessions held during the TO THE NEW bootcamp


## Authors

- Employee name - [Deepanshu Mishra](https://newersworld.tothenew.com/#/unifiedEmployeeView/8210)
- Employee ID - 8210


# Common Sessions
Common sessions module includes total 9 sessions held from 22 Jan - 31 Jan, 2025 
## Week-1
### Introduction to Linux
references - [notion](https://hexagonal-seahorse-af5.notion.site/Liniix-notes-fddedad1e8014f76831223624dbe8764) & [ppt](https://docs.google.com/presentation/d/1WGUNJtDjp_oM6dISAPbGM526l43Yl_d7/edit#slide=id.p1)
- what is linux?
    
    Linux is a kernel (responsible for communicating applications with hardware ie memory, cpu etc) which when combined with a GNU (GNU not unix) makes an operating system. It is so popular mainly because of its open source nature and portability, This means we can run a linux based os on any hardware by making some changes to the base architecture only and since it has such an active Open Source community there's actively updates and patches being released, more and more OS options are available and troubleshooting becomes easy

- linux architecture

    Linux architecture on base level has
        
        -->hardware
            -->kernel - responsible for interacting with the hardware
                -->shell - line based ui that works with a kernel using commands
                    -->applications - end applications that require hardware attention


- EVERYTHING IS A FILE!!

    The Linux file system follows the File System Standard (FSSTND) proposed in 1994. Each Linux system contains a set of standard files and directories, such as (ppt41):

        Root Directory ( / ): The top-level directory.

        /bin: Contains essential user binaries like bash, cat, cp, etc.

        /boot: Contains files essential for booting, including the kernel.

        /home: Contains users' home directories.

        /dev: Contains special device files for hardware (e.g., /dev/fd0 for floppy disk).

        /etc: Holds configuration files, e.g., /etc/passwd stores login information.

        /var: Stores files that change as the system runs, such as logs.

        /lib: Holds essential shared libraries needed for system operation.

        /mnt: Used for temporarily mounting file systems.

        /root: Home directory of the system administrator.

        /sbin: Contains system binaries.

        /tmp: Holds temporary files.

        /usr: Contains read-only data, such as manuals and shared files.


### Introduction to Version Control
references - [ppt](https://docs.google.com/presentation/d/1Uh76MArjF7CPdQNImZZujoH4iYEA6I5k/)

- what is version control?

    A system that helps manage changes to files, code, or any digital assets over time. It allows multiple people to work on a project simultaneously, tracks every modification made, and provides tools to revert to earlier versions if needed. Version control systems (VCS) are commonly used in software development, but they can also be applied to other collaborative work like documentation, design, or research projects.

- central and distributed VCS

    Centralized Version Control Systems (CVCS) store all project versions on a central server, requiring constant connectivity and posing a single point of failure risk. In contrast, Distributed Version Control Systems (DVCS) allow each user to maintain a complete local copy of the repository, enabling offline work and faster operations. DVCS also reduces data loss risk, simplifies conflict resolution, and provides full project history locally, while CVCS relies on server capacity and network speed.

- stages in git

        Modified: The file has been altered but these changes haven't been recorded in the repository yet.
        Staged: The modified file has been marked to be included in the next commit.
        Committed: The changes have been saved to the local repository.
