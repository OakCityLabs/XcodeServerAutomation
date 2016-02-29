This directory should contain the ssh key pair so that the build server can access the git repository.

Files:
 
  * id_rsa
  * id_rsa.pub

You can create an appropriate pair with no passphrase using the command:

```ssh-keygen -t rsa -f id_rsa -N ""```