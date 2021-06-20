from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

LOGIN_ID = "beelineForm_UserLoginForm_userNameText"
PASSWORD_ID = "beelineForm_UserLoginForm_passwordText"
LOGIN_BUTTON_ID = "beelineForm_loginButtonLink"
MAIN_PAGE_HEADER_ID = "NewHeaderCurrentLoginName"
MONDAY_FIELD_UNBOX_ID = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_0_Task_0_EntryTextBox_1"
	
def handle_login_page(webdriver, url, username, password) -> None:
	webdriver.get(url)

	login_field = webdriver.find_element_by_id(LOGIN_ID)
	password_field = webdriver.find_element_by_id(PASSWORD_ID)
  
	if not login_field.text:
		login_field.send_keys(username)
		password_field.send_keys(password)
	
	try:
		login_button = webdriver.find_element_by_id(LOGIN_BUTTON_ID)
		login_button.click()
	except NoSuchElementException:
		print("Error logging in!")
		exit()

	return WebDriverWait(webdriver, 10).until(
		lambda x: x.find_element_by_id(MAIN_PAGE_HEADER_ID) and x.find_element_by_id(MONDAY_FIELD_UNBOX_ID)
	)
