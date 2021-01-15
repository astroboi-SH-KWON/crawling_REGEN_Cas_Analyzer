import time

from astroboi_bio_tools.ToolLogicPrep import ToolLogicPreps
class LogicPreps(ToolLogicPreps):
    def __init__(self, web_drv, target_url):
        super(LogicPreps, self).__init__()
        self.web_drv = web_drv
        self.target_url = target_url

    def go_to_url(self, url):
        self.web_drv.get(url)

    def input_data_by_id(self, el_id, data):
        self.web_drv.find_element_by_id(el_id).send_keys(data)

    def click_by_id(self, el_id):
        self.web_drv.find_element_by_id(el_id).click()

    """
    get_by_xpath : 
    :param
        ml_path : xml path
        flag : True -> multi elements
    """

    def get_by_xpath(self, ml_path, flag=True):
        try:
            if flag:
                return self.web_drv.find_elements_by_xpath(ml_path)
            return self.web_drv.find_element_by_xpath(ml_path)
        except:
            print("is still processing")
            time.sleep(1)
            self.get_by_xpath(ml_path, flag)

    def scroll_down(self):
        self.web_drv.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def get_data_by_id(self, el_id):
        try:
            return self.web_drv.find_element_by_id(el_id)
        except:
            print("is still processing")
            time.sleep(1)
            self.get_data_by_id(el_id)
