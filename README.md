
# Bootcamp Respository

This repository contains exercise documents and relevant files for all the practical sessions held during the TO THE NEW bootcamp


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


## Week-2
### Introduction to Databases
  references - [ppt](https://docs.google.com/presentation/d/1XRl422b4x68SdYwfCWrWNdvI1A_bz22zufy6iRhOJN0/edit#slide=id.g7d34a8f7f9_0_123)

- basic terms & keys
 
    Database: Organized collection of data

    **Table**: Used to store/ club data same as excel sheet.

    **Row/Tuple**: is an collection of single entity attributes or group of related data.

    **Column**: feature or attricute

    Super Key: group of single or multiple keys which identifies rows in a table

    Candidate Key: A super key with no repeated attribute 

    **Primary Key**: Uniquely identify a row (entity) into table. Can not contain NULL.

    Alternate Key: Candidate keys which are not primary key

    **Normalization**: Breaking data into multiple tables to reduce redundancy and promote redundancy

- Types of sql statements

    1. Data Defination Language **DDL**: statements to define structure of the data stored
    2. Data Manipulation Language **DML**: queries used for altering the data itself
    3. Data Control Language **DCL**: control the visibility of data like granting database access and set privileges to create tables


### AWS Overview
references - [ppt](https://docs.google.com/presentation/d/1gp0q6R7vcz2m-UqJwg_fu0Wycpy7VS5B/edit) & [docs](https://aws.amazon.com/pricing/?aws-products-pricing.sort-by=item.additionalFields.productNameLowercase&aws-products-pricing.sort-order=asc&awsf.Free%20Tier%20Type=*all&awsf.tech-category=*all)


- evolution of deployment models

    1. Traditional deployment: In early days, applications were deployed directly on physical servers where each server ran a single application or a service. Applications were installed directly on the hardware without any abstraction ie each application was built as a tightly integrated unitsnand requires its own dedicated hardware.
    - challenges: not flexible, expensive, difficult to scale.        
        scaling required literally adding more physical servers and managing such amounts of hardware was time consuming, costly and labour intensive.

    2. Virtualized deployment: First architecture that introduced an abstraction layer between the hardware and OS, enabling multiple VMs to run on a single physical server. This was possible due to hypervisors(VMware, KVM etc). Now we could share resouces between multiple VMs, each of which was isolated ie had its own OS and applications and these could be easily cloned, moved and scaled in contrast to traditional methods which reduced cost and improved flexibility
    - challenges: resource overhead, slow boot times and complex management
        each VM required a full OS and managing large numbers of VMs could be challenging due to their dependencies

    3. Container deployment: introduction of containers revolutionized deployment as they are a lightweigh alternatives to VMs enabling applications to run in isolated user spaces while sharing the host OS kernel. This is possible due to container runtime(Docker, kubernetes etc). Since containers share the host OS kernel, it eliminates th need for a full OS per application while still retaining indipendence among the containers. These containers can package applications that can run consistently accross different environments, and we benefit from fast startup times promoting dynamic scaling, efficient resource usage and better orchestration because of tools like kubernetes promoting auto scaling and better management of containers
    - advantages: containers are best suited for microservices architectures, containers align with CI/CD pipelines well.
    - challenges: Containers share the host OS kernel which can introduce security risks if not properly isolated. managing containerized environments especially at scale requires expertise


- different service models

        1. Traditional: Refers to servers where you manage everything on premise

        2. Iaas: Infrastructure as a service. Here everything upto the Operating system is managed by your service provider. You are only responsible for middleware runtime data and applications on your end. eg-AWS GCP

        3. PaaS: Platform as a service model takes away even the middleware and runtime resposibility, they're provided by the SP as well. eg-Heroku, Elastic Beanstock

        4. SaaS: Software as a service model basically is a finished produt which can be used by end users. eg-Gmail, Slack