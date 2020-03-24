import logging

#CK - 2020/01/13
#added 'logfilename' and 'uselogfile' inputs. Setup so that by default, nothing
#changes from the original way the function behaved. But, if the 'logfilename'
#is provided, and the 'uselogfile' indicator is True, then it will create a
#logger that prints to the specified file


def get_think_logger(name='think',
                     logfilename='outfile.txt',
                     uselogfile=False,
                     formats='%(time)12.3f      %(source)-18s      %(message)s',
                     level=logging.DEBUG):
        '''Returns a new logger.'''
        if uselogfile:
            logging.basicConfig(filename=logfilename,
                                format=formats, level=level)
        else:
            logging.basicConfig(format=formats, level=level)
        return logging.getLogger(name)
