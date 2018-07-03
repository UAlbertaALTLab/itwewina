#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import os
import signal
import sys
from contextlib import contextmanager
from random import randint
from signal import SIGUSR1, SIGTERM
from time import sleep


def child():
    print(" └ child %d (session: %d)" %(os.getpid(), os.getsid(os.getpid())))
    for _ in range(4):
        pid = os.fork()
        if pid == 0:
            # Child. Simply wait for a signal, then terminate.
            print("   ├ grandchild %d (session: %d)" %(os.getpid(), os.getsid(os.getpid())))
            signal.pause()
            sys.exit()
        # Parent; continue spawning children
    sleep(randint(1, 3))
    parent = os.getppid()
    print(" - child ready; issuing SIGUSR1 to %d" %(parent,))
    os.kill(parent, SIGUSR1)
    signal.pause()


@contextmanager
def signal_handler(signalnum, handler):
    """
    Sets a signal handler temporarily.
    """
    original_handler = signal.getsignal(signalnum)
    signal.signal(signalnum, handler)
    try:
        yield
    finally:
        # *Always* reset the orignal handler
        signal.signal(signalnum, original_handler)


@contextmanager
def server():
    # Start the server.
    print("server will fork: %d (session: %d)" %(os.getpid(), os.getsid(os.getpid())))
    pid = os.fork()
    if pid == 0:
        # Child process.
        # Start a new process group.
        os.setsid()
        child()
        sys.exit()

    # Python 2 work around. Since there is non nonlocal keyword, we need to
    # mutate a variable in the closure in order for that to be reflected
    # outside of the inner function. In other words, we can't just say
    # child_ready = True inside wait_for_sigusr1, because a new variable is
    # created only in the signal handler :/
    child_ready = []

    def wait_for_sigusr1(signum, _stack_frame):
        assert signum == SIGUSR1
        print("child read!")
        child_ready.append(True)

    # Parent process
    with signal_handler(SIGUSR1, wait_for_sigusr1):
        signal.pause()
        assert os.getsid(pid) == pid
        assert child_ready

    print("%d received SIGUSR1; child %d is ready." % (os.getpid(), pid))
    try:
        # The server is ready!
        yield
    finally:
        # No matter what happens, *always* kill the child process, lest they
        # become orphaned zombies.
        print("server sending SIGTERM to progress group %d" % (pid,))
        os.killpg(pid, SIGTERM)



if __name__ == '__main__':
    with server():
        print("Check out ps/the activity monitor for the process tree!")
        raw_input("Press enter to continue.")
        raise Exception("frivillous error!")
