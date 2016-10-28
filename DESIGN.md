
# WOrk-log

## Planning

- The client script must accepts parameters such as public-key, hostname and etc ...
- How can send an ssh command on windows? cygwin, or new ssh 
  implementation from microsoft? at all, I assume all workstations are 
  linux.
- Observation processes must be asynchronous. for example 20 workers 
  will waiting for client's result at the same time, simultaneously.
- Because we are going to save the encryption key on the clients machine
  and everyone can access them, we should use asymmetric encryption.
  but at all, i cannot understand if, the connection is made by ssh between 
  the client & server, why data encryption was requested. at all, 
  of-course!
- The database will be created using ORM in code-first manner.
- For the configuration I prefer to use yaml instead of the xml. it's 
  so clear and readable. so my own open-source configuration 
  library will be used.
- If time available in the future. the PSExec and or winexec will be 
  tested for win client. A few years ago, I was used them for an 
  ITIL(Help-Desk) project, to executing a command on the remote machine 
  using Win-IPC, as the file & printer sharing is working. But it's very 
  un-secure.
- Using github kanban to manage project.
