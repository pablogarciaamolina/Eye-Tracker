import os
from termcolor import colored

class Console_Interface:

    def clear_interface(self):

        os.system('cls')

    def title(self, text: str):
        print(colored(text.upper(), attrs=['bold']))

    def start_load(self, text: str):
        print(text + ' ...', end='', flush=True)

    def finish_load(self, text: str = 'DONE'):
        print(text)

    def message(self, m: str, underlined: bool = False):
        if underlined:
            m = colored(m, attrs=['underline'])

        print(m)

    def colored_message(self, m: str, color: str, underlined: bool = False):
        if underlined:
            m = colored(m, attrs=['underline'])

        m = colored(m, color)
        print(m)

    def bool_input(self, text: str, next_line: bool = False) -> bool:

        if next_line: 
            text = text + '\n'

        return bool(input(text))

    def special_intro(self):
        '''
          EYE TRACKER              
        '''

        self.clear_interface()

        print("\
                 ______             _______             _              \n\
                |  ____|           |__   __|           | |             \n\
                | |__  _   _  ___     | |_ __ __ _  ___| | _____ _ __  \n\
                |  __|| | | |/ _ \    | | '__/ _` |/ __| |/ / _ \ '__| \n\
                | |___| |_| |  __/    | | | | (_| | (__|   <  __/ |    \n\
                |______\__, |\___|    |_|_|  \__,_|\___|_|\_\___|_|    \n\
                        __/ |                                          \n\
                        |___/                \n\
            ")
        
        print('\n\n')


