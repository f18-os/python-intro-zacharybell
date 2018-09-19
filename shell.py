#! /usr/bin/env python3

import os, sys, webbrowser


def execute_cmd_sq(cmd_sq):

    if '|' in cmd_sq:
        
        p1, p2 = map(str.strip, cmd_sq.split('|', 1))

        # get fds for pipe
        pr, pw = os.pipe()
        os.set_inheritable(pr, True)
        os.set_inheritable(pw, True)
        
        # create fork for execution
        rc = os.fork()

        if rc < 0:
            raise Exception('fork failed')
        
        # child handles execution
        elif rc == 0:
            
            # set stdout to pw
            os.dup2(pw, 1)
            
            os.close(pw)
            os.close(pr)

            # separate program from flags, ect.
            p1 = p1.split()
            os.execvp(p1[0], p1)
        
        # parent reassigns input and continues
        else:
            
            # wait for child to finish
            os.wait()

            # set stdin to pr
            os.dup2(pr, 0)

            os.close(pw)
            os.close(pr)

            execute_cmd_sq(p2)

    elif '<' in cmd_sq:
        
        # p2 is the file that is used for input into p1
        p1, p2 = map(str.strip, cmd_sq.rsplit('<', 1))

        os.close(0)
        sys.stdin = open(p2, 'r')
        os.set_inheritable(sys.stdin.fileno(), True)

        execute_cmd_sq(p1)

    elif '>' in cmd_sq:

        # p2 is the file that is used for output from p1
        p1, p2 = map(str.strip, cmd_sq.rsplit('>', 1))

        os.close(1)
        sys.stdout = open(p2, 'w')
        os.set_inheritable(sys.stdout.fileno(), True)

        execute_cmd_sq(p1)

    # command seq with no pipes or redirection
    elif cmd_sq:

        cmd_sq = cmd_sq.split()
        os.execvp(cmd_sq[0], cmd_sq)

    else:
        return webbrowser.open('https://www.warnerbros.com/archive/spacejam/movie/jam.htm')


raw = ''
while(True):
    
    raw = input('$ ')
    
    if raw == 'exit':
        break

    rc = os.fork()

    if rc < 0:
        sys.exit(1)
    elif rc == 0:
        execute_cmd_sq(raw)
    else:
        os.wait()
    