from CommunicationManagement import CommunicationManagement
from AlgEventHandler import AlgEventHandler
from EventManager import EventManager

class Operation:
    def __init__(self):
 # 状态监视器(对应处理端的状态，控制处理的运行)

        self.event_manager = EventManager()  # 事件管理器(事件的存入和处理管理)
        self.event_mng = EventManager()

        self.conManagement2 = CommunicationManagement(self.event_mng, "A2O", "O2A")

        self.algeventhandler = AlgEventHandler(self.event_mng, self.conManagement2)






if __name__ == '__main__':
    operation = Operation()

