from interface_class import Interface
import logging

logging.basicConfig(level=logging.INFO, filename='scraper.log', format='%(asctime)s -  %(levelname)s - %(message)s', datefmt='%H:%M:%S')


def main():
    root = Interface()
    root.mainloop()


if __name__ == '__main__':
    main()