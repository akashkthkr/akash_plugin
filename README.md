# AKASH Plugin
* Akash Kant 
* ASU ID: 1222368576
Reverse Engineering tool for gdb using python exploit development assistance PEDA(use is extensive)



# Installation
- clone the repo git clone git@github.com:akashkthkr/akash_plugin.git  ~/
- echo "source ~/akash_plugin/akash.py" >> ~/.gdbinit
- Now it would be added to Home folder and gdbinit with source py code


# Features 
This will list al the string in like strncmp, memcmp as these are generally used by angr-management or ghida base address to run it in angr via python code

# Prerequiste

* Python 3  -- latest python version
* Gdb -- latest gdb debugger
* sample file to debug on gdb in this case the test binary

# Execution

- Run gcc test.c -o test
- The run gdb with inital load of the files.


