import actions as act

#################################################
# [1] Microsoft Copilot, a large language model
# (after submitting my actions.py and 14_use_actions.py
# script for Copilot [1] to respond with)
#
class Agent:
    def __init__(self, name, word, program):
        self.name = name
        self.word = word  # instance of Cat3
        self.program = program
            # list of morphism commands
        self.inbox = []  # received messages
        self.outbox = []  # messages to send

    def run_step(self):
        if len(self.program) > 0:
            print(f"{self.name}\n  prog = {self.program}")
            print(f" 1. word = {self.word}")
            self.word = act.run_program(self.word, \
                    '\n'.join(self.program))
            print(f" 2. word = {self.word}")
        return True
    def send(self, recipient, tag, message):
        self.outbox.append((recipient.name, \
                tag, message))
        return True
    def receive(self, sender, tag):
        if len(sender.outbox) > 0:
            tup = sender.outbox.pop(0)
            if tup[0] == self.name and \
               tup[1] == tag:
                self.inbox.append(tup)
                return True
            else:
                sender.outbox.append(tup)
                return False
        else:
            return False
#
##############
# JGE:
#
    def __str__(self):
        s1 = f"(name: {self.name},word:{self.word},"
        s2 = f"inbox: {self.inbox},"
        s3 = f"outbox: {self.outbox})"
        s = s1 + s2 + s3
        return s
    def __repr__(self):
        return str(self)
#
#######################################################

