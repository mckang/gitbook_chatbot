from app.gitbook import __main__ as gitbook_main
from app.blog import __main__ as blog_main

def main():
    gitbook_main.main()
    blog_main.main()

if __name__ == "__main__":
    main()