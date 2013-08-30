# encoding: utf-8

import sys
import getopt
import os
import subprocess
import logging
import traceback
import ConfigParser

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)   

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter1 = logging.Formatter("%(levelname)s - %(message)s")
ch.setFormatter(formatter1)
debug_log_path = "debug.log"
if os.path.isfile(debug_log_path):os.unlink(debug_log_path)
fh = logging.FileHandler(debug_log_path)
fh.setLevel(logging.DEBUG)
formatter2 = logging.Formatter("%(asctime)s %(filename)s %(levelname)s - %(message)s")
fh.setFormatter(formatter2)
logger.addHandler(ch)
logger.addHandler(fh)

def run_cmd(cmd, is_wait=True, is_log_stdouterr=True, is_log_cmd=True):

    global logger

    if (is_log_cmd):
        logger.info(cmd)   
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if (is_wait):
        stdout, stderr = p.communicate()
        if is_log_stdouterr:
            logger.debug("stdout is\n %s" % stdout)    
        if (stderr != None and len(stderr) != 0):
            if is_log_stdouterr:
                logger.error("stderr is\n %s" % stderr)  
        return (stdout, stderr)
    else:
        return p

def show_help():
    print 'sample usage : python python_main_template.py -m BB'
    print 'sample usage : python python_main_template.py --mode BB'
    print 'sample usage : python python_main_template.py -m BB -d'

def main(argv): 

    logger.info("program start......")
            
    try:
        opts, args = getopt.getopt(argv, "hdm:", ["help", "debug", "mode="])

        mode = "AA"
        is_debug_mode = False
        jenkins_parameter_a = 'aaa'
        jenkins_parameter_b = 'bbb'
        build_number = '0000'

        # logger.info("-------------Environment Variables-------------")
        # for (k,v) in os.environ.items():
        #     logger.info("%-20s : %s" % (k, v))
        # logger.info("-----------------------------------------------") 
            
        if (os.environ.get("BUILD_NUMBER", None) != None):
            build_number = os.environ["BUILD_NUMBER"]
        if (os.environ.get("JENKINS_PARAMETER_A", None) != None):
            jenkins_parameter_a = os.environ["JENKINS_PARAMETER_A"]            
        if (os.environ.get("JENKINS_PARAMETER_B", None) != None):
            jenkins_parameter_b = os.environ["JENKINS_PARAMETER_B"]      
        
        #replace default value by command line args
        for option, value in opts:
            if option in ("-d", "--debug"):
                is_debug_mode = True
            if option in ("-h", "--help"):
                show_help()
                return 1
            if option in ("-m", "--mode"):
                mode = value
                
        logger.debug("-------------All Variables After Replace-------------")
        logger.debug("%-20s : %s" % ("is_debug_mode", str(is_debug_mode)))
        logger.debug("%-20s : %s" % ("mode", mode))
            
        logger.debug("%-20s : %s" % ("build_number", build_number))
        logger.debug("%-20s : %s" % ("jenkins_parameter_a", jenkins_parameter_a))
        logger.debug("%-20s : %s" % ("jenkins_parameter_b", jenkins_parameter_b))
                                             
        logger.debug("-------------Start Processing-------------")      
        
        #bool
        logger.info("-------------bool-------------")
        a = True
        b = False
        if a:   #or if a == True:
            logger.info('a is True')
        else:
            logger.info('a is False')             

        if not b:  #or if b == False:
            logger.info('b is False')
        else:
            logger.info('a is True')      

        #string
        logger.info("-------------string-------------")     
        s1 = 'aaa'
        s2 = "   aAa\"bBb test test  "
        logger.info(type(s2))
        logger.info(s2.lower())
        logger.info(s2.upper())
        logger.info(s2.replace('test', '456'))
        logger.info(s2.replace('test', ''))
        logger.info(len(s2))
        logger.info(s2.strip())  #remove leading and trailing white space
        logger.info(s2.split())
        if s2.find('test') != -1:
            logger.info('find test')
        else:
            logger.info('not find test') 
        logger.info('test' in s2)

        #list
        logger.info("-------------list-------------")   
        sample_list = [1,2,3,4,5]
        logger.info(type(sample_list))
        logger.info(sample_list[0])
        logger.info(sample_list[-1])
        logger.info(sample_list[-2])
        for e in sample_list:
            logger.info(e)
        sample_list.append(6)
        logger.info(sample_list)
        logger.info(len(sample_list))
        for i in range(3):
            logger.info(i)
        logger.info(3 in sample_list)
        logger.info(9 in sample_list)

        #tuple
        logger.info("-------------tuple-------------")   
        sample_tuple = (1,2,3,4,5)
        logger.info(sample_tuple[0])
        logger.info(sample_tuple[-1])
        logger.info(sample_tuple[-2])
        # sample_tuple.append(6)   #will be fail because tuple can't change element

        #dict
        logger.info("-------------dict-------------")   
        sample_dict = {'a':111, 'b':222, 'c':333}
        sample_dict['d'] = 444
        logger.info(sample_dict)
        logger.info(len(sample_dict))
        logger.info(sample_dict['a'])
        logger.info(sample_dict.get('aa', 'fail to find'))
        for (k,v) in sample_dict.items():
            logger.info("k :%s, v:%s" % (k,v))
        logger.info('a' in sample_dict.keys())
        logger.info(5555 in sample_dict.values())

        #file access
        logger.info("-------------file-------------")   
        fw = open('test.txt', 'w')
        fw.write('hello world')
        fw.close()

        fr = open('test.txt', 'r')
        logger.info(fr.read())
        fr.close()

        #read config
        logger.info("-------------config-------------")   
        setting_config = ConfigParser.RawConfigParser()
        setting_config.read('setting.cfg')
        try:
            v1 = setting_config.get("SECTION_A", "k1")
            v2 = setting_config.get("SECTION_A", "k2")

            logger.info("v1:%s, v2:%s" % (v1,v2))

        except:
            logger.error('fail to read from config')

        #use command line get output and process
        logger.info("-------------command line process-------------")   
        cmd = 'ps aux'
        (stdout, stderr) = run_cmd(cmd)
        root_process = 0
        for line in stdout.split('\n'):
            elements = line.split()
            if len(elements) > 0:
                if elements[0].lower() == 'root'.lower():
                    root_process = root_process + 1
                elif elements[0].lower() == 'test'.lower():
                    pass
                else:
                    pass

        logger.info("root_process is %d" % (root_process))      

        #random


        #json handle


    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exception_str = ''.join('!! ' + line for line in lines)           
        logger.error("exception ...\n%s" % (exception_str))    
        return 2


    return 0

if __name__ == "__main__":
    main(sys.argv[1:])

