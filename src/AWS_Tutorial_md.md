# AWS & MongoDB Setup Walkthrough

## Launch EC2 & Connect to it
1. Go to AWS and create an instance using the "Amazon Linux 2 AMI (HVM), SSD Volume Type" AMI

1. Open the port on your new instance by going to<br>
   Security Groups -> Inbound -> Edit -> Add Rule<br>
   Type: "Custom TCP Rule" Port Range: "27017" Source: "Anywhere"


1. Add connection information to your SSH config file at `~/.ssh/config`<br>
All of this except the connection name, which you can pick, comes from the "Connect" dialog on AWS<br>
Note: the hostname dns WILL CHANGE every time you stop and restart your instance!
    ```
    Host <connection name>
        Hostname ec2-##-##-##-##.us-west-2.compute.amazonaws.com
        User <user>
        IdentityFile ~/.ssh/<keyfile>.pem
    ```
    
1. Connect!
    ```
    ssh <connection name>
    ```

1. Update the pre-installed packages.
    ```
    sudo yum update
    ```

## Setup Mongo
1. Install MongoDB on your EC2
    https://docs.mongodb.com/manual/tutorial/install-mongodb-on-amazon/<br>
    Follow the installation instructions for "Amazon Linux (2013.03+)"<br>
    once installed run these commands:
    ```
    sudo chkconfig mongod on
    sudo service mongod start
    ```

1. Create a database by inserting something, anything, into it. If nothing is inserted, database is not created.
    ```
    mongo

    use <database_name>
    db.meta.insert({"Description": "Lorem ipsum, dolor sit amet"})
    ```

1. Create Users. If you skip this step, anyone who finds the EC2's ip address will have full access to your MongoDB server!
    ```py
    # create an admin user for full access
    use admin
    db.createUser({user: "root", pwd: "<password>", roles: ["root"]})

    use <database_name>
    db.createUser(
        {
            user: "<userName>",
            pwd: "<password>"
            roles: [ "readWrite" ]
        }
    )
    ```

1. Unbind IP & Turn on authentication
    ```
    sudo nano /etc/mongod.conf
    ```
    after the line "#security:" insert this:
    ```
    security:
       authorization: 'enabled'
    ```
    Change the 'net' section so it looks like this:
    ```
    net:
      port: 27017
      bindIpAll: true
    ```
    save, then run
    ```
    sudo service mongod restart
    ```

1. Now after launching mongo from the terminal, you have to sign in as follows:
    ```py
    db.auth( <username>, passwordPrompt() )
    // Or
    db.auth( <username>, <password> )
    ```

1. Test connection from python (on any machine)
    ```py
    from pymongo import MongoClient

    connection_string = "mongodb://<username>:<password>@<aws connection url>:27017/<database-name>"
    # example "mongodb://guest:pass@ec2-54-69-159-110.us-west-2.compute.amazonaws.com:27017/ufo_sightings"

    # or if you're more security minded and don't want passwords in your repo!
    from getpass import getpass
    connection_string = f"mongodb://{getpass(prompt="User:")}:{getpass.getpass()}@<aws connection url>:27017/<database-name>"

    client = MongoClient(connection_string)
    db = client.<database-name>
    db.list_collection_names()
    ```

## Frictionless S3, & Github Setup for EC2 instances
### Copied from a file you probably didn't notice in the AWS assignment
Here's what to do:
1. Create an EC2 instance with permission to write to s3 (without ever having to copy your AWS credentials to the instance!)
 
    -  Go to AWS Console
    -  Go to IAM
    -  Choose Roles
    -  Create Role
    -  AWS Service -> EC2, click Next: Permissions
    -  Search box -> type S3 -> check AmazonS3FullAccess, Next: Review
    -  Create Role
    -  Now, create a new EC2 instance (or choose an existing one) and assign it the IAM role that you just created. It will appear on a dropdown list.
    -  SSH into your EC2 instance and use `aws s3 cp <origin> <destination> to copy a file from EC2 to s3! see (https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html)
2. Create a new github repository with source code for your project. Just like normal.
3. Clone github repository onto your EC2 instance to keep your code and compure resources synced. 
    - You can go straight ahead and `git clone https://github.com/username/reponame` to your EC2 instance and your done.  
    - To remove the friction of supplying your username/password every time you push/pull, run the following commands **on your remote machine**:
        - Create an SSH key: `ssh-keygen -b 4096`
        - Tell SSH to use it. (this assumes that there's no existing SSH config on the instance) `echo "IdentityFile ~/.ssh/id_rsa" > ~/.ssh/config`
        - Then copy and paste the public key as a new authorized SSH key on GitHub `cat ~/.ssh/id_rsa.pub`
        - Then `git clone git@github.com:username/reponame` just works.
4. Write code on your local machine (or your remote instance!), and keep all machines synced with frequent add/commit/push/pull.  This is the beauty of version control!
5. That's it!