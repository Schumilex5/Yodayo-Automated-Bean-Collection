import utyl


def claim_process(driver, index):
    # Go to login page
    utyl.go_to_login_page(driver)

    # Find the email field by placeholder and type the email
    utyl.fill_email_field(driver, index)
    # Find the password field by placeholder and type the password
    utyl.fill_password_field(driver, index)
    # Find the login button by inner text and click it
    utyl.click_login_button(driver)

    # Tick all checkboxes if new to site
    utyl.find_and_tick_checkboxes(driver)

    # Find any click profile picture
    utyl.wait(3)
    utyl.find_and_click_profile_picture(driver)

    # Go to beans page by clicking the option
    utyl.find_and_click_claim_yobeans(driver)
    utyl.wait(3)

    # Claim beans
    utyl.claim_yo_beans(driver)

    # Logout
    utyl.find_and_click_profile_picture(driver)
    utyl.click_logout_button(driver)
