#!/usr/bin/env python

import rospy
import smach
import random
import smach_ros

##-----------------------------------------------------------------------------------
##Example 2

class ConcurrenceState(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["positiv", "negativ"])
    
    def execute(self, ud):
        rnumber = random.randint(-50,50)
        rospy.loginfo("Random : %d"%(rnumber))
        rospy.sleep(1.0)
        if(rnumber > 0):
           return "positiv"
        else:
           return "negativ"   

def SimpleConcurrence():
    FooBar_cc = smach.Concurrence(outcomes = ["positiv","negativ"],
                                  default_outcome = "positiv",
                                  outcome_map = {"positiv" : {'Foo':"positiv",'Bar':"positiv"},
                                                 "negativ" : {'Foo':"negativ",'Bar':"negativ"}})
    with FooBar_cc:
        FooBar_cc.add('Foo',ConcurrenceState())
        FooBar_cc.add('Bar',ConcurrenceState())
    
    return FooBar_cc

##-----------------------------------------------------------------------------------
##Example 1

class Ping(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["ping"], output_keys = ['ping'])
    
    def execute(self, ud):
        rospy.sleep(3.0)
        rospy.loginfo("Pinging...")
        ud.ping = True
        return "ping"
    
class Pong(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["pong"], input_keys = ['ping'])
    
    def execute(self, ud):
        while 'ping' not in ud:
            rospy.loginfo('... Waiting for ping....')
            rospy.sleep(0.5)
        rospy.loginfo('Ping received')
        return "pong"
        
def SynchroConcurrence():
    Synchro_cc = smach.Concurrence(outcomes = ["succeeded","aborted"],
                                   default_outcome='aborted',
                                   outcome_map = {"succeeded" : {'Ping':"ping",'Pong':"pong"}})
                                   
    with Synchro_cc:
        Synchro_cc.add('Ping',Ping())
        Synchro_cc.add('Pong',Pong())
        
    return Synchro_cc


    
    
    

    
                                                                  
    
                                                                  