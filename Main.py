from selenium import webdriver
import time
import os
# from Bio import SeqIO
import multiprocessing as mp
# import numpy as np
import platform

import Util
# import Logic
import LogicPrep
#################### st env ####################
WORK_DIR = os.getcwd() + "/"
PROJECT_NAME = WORK_DIR.split("/")[-2]
SYSTEM_NM = platform.system()

if SYSTEM_NM == 'Linux':
    # REAL
    pass
else:
    # DEV
    WORK_DIR = "D:/000_WORK/JangHyeWon_LeeMinYung/20200703/WORK_DIR/"

IN = 'input/'
OU = 'output/'
FASTQ = 'FASTQ/'

os.makedirs(WORK_DIR + IN, exist_ok=True)
os.makedirs(WORK_DIR + OU, exist_ok=True)

TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.8)

WEB_DRV_PATH = "C:/Users/terry/chromedriver.exe"
TARGET_URL = "http://www.rgenome.net/cas-analyzer/#!"


#################### en env ####################


def main():
    util = Util.Utils()

    trgt_fastq_dir = 'test_253_2_S7_L001_R1_001/'
    sources = util.get_files_from_dir(WORK_DIR + FASTQ + trgt_fastq_dir + '*.fastq')

    ref_seq = 'AGTTATGCATCCATACAGTACACAATCTCTTCTCTCTACAGATGACTGCCATGGAGGAGTCACAGTCGGATATCAGCCTCGAGCTCCCTCTGAGCCAGGAGA'
    trgt_seq = 'TGCCATGGAGGAGTCACAGT'
    result_list = []

    for file_path in sources:
        opt = webdriver.ChromeOptions()
        opt.add_argument("start-maximized")
        web_drv = webdriver.Chrome(chrome_options=opt, executable_path=WEB_DRV_PATH)

        logic_prep = LogicPrep.LogicPreps(web_drv, TARGET_URL)

        logic_prep.go_to_url(TARGET_URL)
        # # Analysis Parameters
        # # Comparison range (R) [?]
        logic_prep.click_by_id('chklr')
        # # (Optional) WT marker (r) [?]
        logic_prep.click_by_id('chkr')  # uncheck

        # # Sequencing Data
        # # Single-end read or fastq-joined file
        logic_prep.get_by_xpath("//select[@id='optfile']/option[@value='1']", False).click()
        logic_prep.input_data_by_id('file3', file_path)

        # # Basic Information
        # # Full reference sequence (5' to 3'):
        logic_prep.input_data_by_id('fullseq', ref_seq)
        # # Nuclease Type:
        # logic_prep.get_by_xpath("//select[@id='nuctype']/option[@value='1']", False).click()
        # # Select Nuclease:
        # logic_prep.get_by_xpath("//select[@id='nucleases']/option[@value='11']", False).click()
        # # Target DNA sequence (5' to 3', without PAM sequence):
        logic_prep.input_data_by_id('rgenseq', trgt_seq)
        # # (Optional) Donor DNA sequence for homology directed repair (HDR) (5' to 3')
        # logic_prep.input_data_by_id('hdrseq', '(Optional) Donor DNA sequence for homology directed repair')

        # # check opt
        # time.sleep(3.0)
        logic_prep.click_by_id('submit')

        # # Result Summary
        logic_prep.scroll_down()
        try:
            os.remove('F:/Downloads/result.txt')
        except Exception as err:
            print(str(err))
        time.sleep(1.0)
        try:
            # # F:/Downloads/result.txt
            logic_prep.click_by_id('btndownload')
            # # check whether download is done or not
            every_downloads_chrome(web_drv)
        except Exception as err:
            print('[ERROR] after submitting \n', file_path + '\n', str(err))
            web_drv.quit()
            continue
        fl_nm_arr = file_path.split('\\')[-1].split('_')
        brcd_paired_key = fl_nm_arr[0] + '_' + fl_nm_arr[1]
        tmp_list = util.read_tsv_ignore_N_line('F:/Downloads/result.txt')

        result_list.extend([[brcd_paired_key] + tmp_arr[1:] for tmp_arr in tmp_list])
        web_drv.quit()

    # make result file
    header = ['brcd_pair', 'WT Sequence', 'RGEN Treated Sequence', 'Length', 'Count', 'Type', 'HDR']
    util.make_tsv(WORK_DIR + OU + trgt_fastq_dir[:-1] + ".txt", header, result_list)


def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)


if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [ " + PROJECT_NAME + " ]>>>>>>>>>>>>>>>>>>")
    main()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))