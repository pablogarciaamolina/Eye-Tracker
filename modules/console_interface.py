from termcolor import colored

class Console_Interface:

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