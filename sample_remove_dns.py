from access_router import router_session
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('password', default=None, nargs='?')
    # ns = parser.parse_args()
    # print(parser.parse_args().password)
    my_router = router_session(password=parser.parse_args().password)
    print(my_router.remove_backup_dns())
