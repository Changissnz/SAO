# TODO : test this class 
from os import path

from collections import defaultdict


class EventHistory:

    def __init__(self, logFrequency, eventFolderPath, masterLogFolderPath = "events_in_history"):
        assert path.isdir(eventFolderPath) and path.isdir(masterLogFolderPath), "invalid directories {} and {}".format(eventFolderPath, masterLogFolderPath)
        self.logFrequency = logFrequency
        self.logCounter = defaultdict(int)

        self.eventFolderPath = eventFolderPath
        self.masterLogFolderPath = masterLogFolderPath
        # make assertions here for existence

    """
    each element's history will be written to a separate file,
    and will contain its shame-align-receive history for each pertinent
    timestamp in GameBoard
    """
    def log_element_event_history(self, element):
        fp = self.masterLogFolderPath + "/element_id_{}.txt".format(element.idn)
        fi = open(fp, "a")
        # element event history will consist of 2 variables:
        ## action
        ##
        k = element.actionHistory.keys()
        for k_ in k:
            action = EventHistory.convert_element_history_timestamp_to_log_history(element, k_, "action")
            receive = EventHistory.convert_element_history_timestamp_to_log_history(element, k_, "receive")
            fi.write(action)
            fi.write(receive)

    def log_element_event_history_scheduled(self, element):
        self.logCounter[element.idn] = self.logCounter[element.idn] + 1

        if self.logCounter[element.idn] == 1:
            return

        if self.logCounter[element.idn] % self.logFrequency == 0:
            self.log_element_event_history(element)

    """
    typeTimeStamp := receive|action
    """
    @staticmethod
    def convert_element_history_timestamp_to_log_history(element, timestamp,\
        typeTimeStamp):

        assert typeTimeStamp in {"receive", "action"}, "invalid typeTimeStamp {}".format(typeTimeStamp)

        if typeTimeStamp == "receive":
            q = element.receiveHistory[timestamp]
        else:
            q = element.actionHistory[timestamp]


        out = "{} @ time [{}]\n".format(typeTimeStamp, timestamp)
        for k, v in q.items():
            shame, align = round(v['shame'], 2), round(v['align'], 2)
            s = "\nelement {} : shame->{}, align->{}".format(k, shame, align)
            out += s
        out += "\n-------#--------------#---------#-------------#-------------#--------\n"
        return out
