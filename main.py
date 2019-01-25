from request_management.main import main as _req
from migrations.migrate import migrate
from seeds.seedUsers import seed



def main():
    migrate()
    # add admin
    seed('admin_hard_password')
    # _req()


if __name__ == '__main__':
    main()
