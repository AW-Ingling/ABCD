Whichever version of the file is used belongs in:
C:\Program Files (x86)\PsychoPy2\Lib\site-packages\psychopy\iohub\client

The original version of iohub drops a file ".iohpd" containing the process ID for the
master process into a file in argv[0]  This has two failure modes:

1. If launched from a script in the interpreter the cwd is somewhere in the
Python modules path and unwritable.
2. The argv[0] does not exist in some conditions, that is, len[argv] == 0. 
It seems like this should never be the case acoroding to Python documentation, 
but it is.    

The solution is to always put the .iohpd file in the home directory.  

