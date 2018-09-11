import os, sys


user_input = ''
while(True):
    user_input = input('> ')
    if (user_input == 'exit'):
        break
    
    child = os.fork()
        
    if (child < 0):
        raise Exception('Failed to create new process!')
    if (child == 0):

        # stdin / stdout redirects
        if '>' in user_input:

            user_input = list(map(str.strip, user_input.rsplit('>')))
            file_name  = user_input[1]
            user_input = user_input[0]

            os.close(1)
            sys.stdout = open(file_name, 'w')
            fd = sys.stdout.fileno()
            os.set_inheritable(fd, True)
        
        elif '<' in user_input:

            user_input = list(map(str.strip, user_input.split('<')))
            file_name  = user_input[1]
            user_input = user_input[0]

            os.close(0)
            sys.stdin = open(file_name, 'r')
            fd = sys.stdin.fileno()
            os.set_inheritable(fd, True)

            user_input = user_input + ' ' + sys.stdin.read()
            print(user_input)

        argv = user_input.split()
        if len(argv) == 0:
            exit()
        os.execvp(argv[0], argv)
    else:
        os.wait()