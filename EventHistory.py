# TODO : test this class
from os import path, mkdir, remove, listdir
from collections import defaultdict
from copy import deepcopy

class EventHistory:

    def __init__(self, logFrequency, eventFolderPath, masterLogFolderPath = "events_in_history", clearPastInfo = True):
        self.set_folder_paths(eventFolderPath, masterLogFolderPath)
        self.logFrequency = logFrequency
        self.logCounter = defaultdict(int)
        self.timeStamp = 0
        # make assertions here for existence

    """
    description:
    - clears contents of masterLogFolderPath

    arguments:
    - clearPastInfo := bool
    """
    def clear_info(self, clearPastInfo):
        if clearPastInfo:
            l = listdir(self.masterLogFolderPath)
            for l_ in l:
                remove(l_)

    """
    description:
    -
    """
    def set_folder_paths(self, eventFolderPath, masterLogFolderPath):
        if eventFolderPath == None:
            eventFolderPath = masterLogFolderPath + "/event_default"
        if not path.isdir(eventFolderPath): mkdir(eventFolderPath)
        assert path.isdir(eventFolderPath) and path.isdir(masterLogFolderPath), "invalid directories {} and {}".format(eventFolderPath, masterLogFolderPath)

        self.eventFolderPath = eventFolderPath
        self.masterLogFolderPath = masterLogFolderPath
        self.alignmentInfoPath = self.eventFolderPath + "/alignment_info.txt"

    """
    each element's history will be written to a separate file,
    and will contain its shame-align-receive history for each pertinent
    timestamp in GameBoard

    arguments:
    - element :=
    - destructiveLog :=
    """
    def log_element_event_history(self, element, destructiveLog = True):
        fp = self.eventFolderPath + "/element_id_{}.txt".format(element.idn)
        fi = open(fp, "a")
        # element event history will consist of 2 variables:
        ## action
        ##
        k = list(element.actionHistory.keys())

        for k_ in k:
            action = EventHistory.convert_element_history_timestamp_to_log_history(element, k_, "action", destructiveLog)
            receive = EventHistory.convert_element_history_timestamp_to_log_history(element, k_, "receive", destructiveLog)

            fi.write(action)
            fi.write(receive)

        fi.close()

    def log_element_event_history_scheduled(self, element):
        self.logCounter[element.idn] = self.logCounter[element.idn] + 1

        if self.logCounter[element.idn] == 1:
            return

        if self.logCounter[element.idn] % self.logFrequency == 0:
            self.log_element_event_history(element)

    def log_element_events(self, sequenceElements):
        for e in sequenceElements:
            self.log_element_event_history_scheduled(e)

    ##
    def log_alignments(self, sequenceElements):
        f = open(self.alignmentInfoPath, "a")
        f.write("**[{}] alignments**\n".format(self.timeStamp))
        for e in sequenceElements:
            f.write("- reference {}\tlanguage info {}/{}\n".format(e.idn, e.activeCentroidCount, e.activeDescriptorCount))
            for k, v in e.shameObeyTable.items():
                f.write("key : {}\tvalue : {}\n".format(k, v))
            f.write("\n\n")
        f.close()

    """
    description:
    -

    arguments:
    - gb := GameBoard
    """
    def log(self, gb):
        self.log_element_events(gb.elements.values())
        self.log_alignments(gb.elements.values())
        self.timeStamp += 1

    # TODO : test this
    """
    typeTimeStamp := receive|action
    """
    @staticmethod
    def convert_element_history_timestamp_to_log_history(element, timestamp,\
        typeTimeStamp, destructiveLog):

        assert typeTimeStamp in {"receive", "action"}, "invalid typeTimeStamp {}".format(typeTimeStamp)

        out = ""
        if typeTimeStamp == "receive":
            out = "RECEIVE\n"
            q = deepcopy(element.receiveHistory[timestamp])
            del element.receiveHistory[timestamp]
        else:
            out = "ACTION\n"
            q = deepcopy(element.actionHistory[timestamp])
            del element.actionHistory[timestamp]

        """
        out += str(q) + ""
        return out
        """
        out = "\n{} @ time [{}]\n".format(typeTimeStamp, timestamp)
        ks = list(q.keys())
        for k in ks:
            shame, align = round(q[k]['shame'], 2), round(q[k]['align'], 2)
            s = "\nelement {} : shame->{}, align->{}".format(k, shame, align)
            out += s
        out += "\n-------#--------------#---------#-------------#-------------#--------\n"
        return out
