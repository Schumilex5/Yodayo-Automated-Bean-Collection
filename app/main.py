from claim_process import claim_process
from credentials import credential_list
from utyl import setup_browser


def main_loop():
    driver = setup_browser()

    for user in credential_list:
        claim_process(driver, credential_list.index(user))


if __name__ == "__main__":
    main_loop()
