from request_management.main import main as _req
from migrations.migrate import migrate

def main():
    # you should run only one of these functions at a time
    
    # migrate()
    _req()


if __name__ == '__main__':
    main()
