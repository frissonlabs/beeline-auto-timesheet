from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

LOGIN_NAME = "email"
PASSWORD_NAME = "password"
LOGIN_BUTTON_NAME = "submit"
MAIN_PAGE_HEADER_ID = "NewHeaderCurrentLoginName"
MONDAY_FIELD_UNBOX_ID = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_0_Task_0_EntryTextBox_1"
	
def handle_login_page(webdriver, url, email, password) -> None:
	webdriver.get(url)

	WebDriverWait(webdriver, 10).until(
		lambda x: x.find_element_by_name(LOGIN_NAME).is_displayed()
	)

	login_field = webdriver.find_element_by_name(LOGIN_NAME)
	password_field = webdriver.find_element_by_name(PASSWORD_NAME)

	if not login_field.text:
		login_field.send_keys(email)
		password_field.send_keys(password)
	
	try:
		login_button = webdriver.find_element_by_name(LOGIN_BUTTON_NAME)
		login_button.click()
	except NoSuchElementException:
		print("Error logging in!")
		exit()

	return WebDriverWait(webdriver, 10).until(
		lambda x: x.find_element_by_id(MAIN_PAGE_HEADER_ID) and x.find_element_by_id(MONDAY_FIELD_UNBOX_ID)
	)
