from loguru import logger

import numpy as np
from metabci.brainstim.paradigm import (
    READ_SYSTEM,
    paradigm,
)


'''自定义'''
import os
from  re_book_stimconfig import BACKLISTConfig, READ_BOOKConfig, REGISTER_Config
from psychopy import visual, core, event, monitors


class AlgEventHandler:
    def __init__(self, event_mng, conmanager):
        self.exchange_message_management = conmanager
        event_mng.AddEventListener('XQXQ', self.do_XQXQ)  # 向事件处理器中添加event和对应的处理函数
        event_mng.Start()

        self.page = 0
        self.book_id = 0
        self.id_result = np.arange(1, 16, 2)
        self.page_result = np.arange(21, 37, 3)

        self.stim = None
        self.result_list = []
        self.result_num = 0

    def get_paradigm(self):

        win = visual.Window(size=(1920, 1080), units='pix', color=(-1, -1, -1), pos=(0, 0),
                                    useFBO=True, allowStencil=True, fullscr=True, screen=0)
        current_directory = os.getcwd()
        cover_images = os.path.join(current_directory, 'picture_set')
        output_images = os.path.join(current_directory, 'picture_set', 'output_images')
        coverstim = os.path.join(current_directory, 'picture_set', 'cover_images')

        cur_paradigm = READ_SYSTEM(win=win)
        cur_paradigm.get_backlist(output_images)
        cur_paradigm.load_cover_co(coverstim)
        cur_paradigm.pic_stim(refresh_rate=READ_BOOKConfig.fps)

        cur_paradigm.get_booklist(output_images)
        cur_paradigm.config_pos(
            n_elements=READ_BOOKConfig.n_elements,
            rows=READ_BOOKConfig.rows,
            columns=READ_BOOKConfig.columns,
            stim_pos=READ_BOOKConfig.stim_pos,
            stim_length=READ_BOOKConfig.stim_length,
            stim_width=READ_BOOKConfig.stim_width,
        )
        cur_paradigm.config_text(symbols=READ_BOOKConfig.symbols, tex_color=READ_BOOKConfig.tex_color)
        cur_paradigm.config_color_re(
            refresh_rate=READ_BOOKConfig.fps,
            stim_time=READ_BOOKConfig.stim_time,
            stimtype="sinusoid",
            stim_color=READ_BOOKConfig.stim_color,
            stim_opacities=READ_BOOKConfig.stim_opacities,
            freqs=READ_BOOKConfig.freqs,
            phases=READ_BOOKConfig.phases,
        )
        cur_paradigm.config_index()
        cur_paradigm.config_response()

        self.stim = paradigm(VSObject=cur_paradigm,
                             win=win,
                             bg_color=REGISTER_Config.bg_color,
                             display_time=REGISTER_Config.display_time,
                             index_time=REGISTER_Config.index_time,
                             rest_time=REGISTER_Config.rest_time,
                             response_time=REGISTER_Config.response_time,
                             port_addr=REGISTER_Config.port_addr,
                             nrep=REGISTER_Config.nrep,
                             pdim="read_system",
                             lsl_source_id=REGISTER_Config.lsl_source_id,
                             online=REGISTER_Config.online)

    def get_stim(self, result):
        if result in self.id_result:
            self.book_id = np.where(self.id_result == result)[0][0]
            self.stim.re_stim(self.book_id, self.page)
        elif result in self.page_result:
            if result == 21 or result == 30:
                self.stim.wait_stim(self.book_id, self.page)
            elif result == 24:
                if self.page == 0:
                    pass
                else:
                    self.page -= 1
                self.stim.re_stim(self.book_id, self.page)
            elif result == 33:
                self.page += 1
                self.stim.re_stim(self.book_id, self.page)
            elif result == 36:
                result = self.result_list[self.result_num - 1]
                self.get_stim(result)
            else:
                self.stim.co_stim()
        else:
            pass






    def do_XQXQ(self, event):
        msg = event.message
        if msg:
            result = msg['result']
            logger.info("判决结果为："+str(result))

            self.result_list.append(result)
            self.get_stim(result)


















