from interface_class import Interface
import logging; logging.basicConfig(level=logging.INFO, filename='scraper.log', format='%(asctime)s -  %(levelname)s - %(message)s', datefmt='%H:%M:%S')

data = {
    'sample': {'question': 'hello world',
                'answers': ['what', 'is', 'up', 'my', 'dudes'],
                'is_selected': [False, False, True, False, True]},
    'question_order': ['sample']
}


def main():
    root = Interface()
    root.mainloop()


if __name__ == '__main__':
    main()