from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from time import sleep

PROJECT_TASK_ID = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_0_Task_0_ProjectComboSelector_Input"
BILLABLE_NONBILLABLE_ID = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_0_Task_0_TaskComboSelector_Input"
BILLABLE_NONBILLABLE_LOADING_ID = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_0_Task_0_TaskComboSelector_LoadingDiv"
BILLABLE_NONBILLABLE_RESULTS_ID = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_0_Task_0_TaskComboSelector_ResultsDiv"
BILLABLE_ID = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_0_Task_0_TaskComboSelector_beelineComboSelectorItem_Billable"
NONBILLABLE_ID = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_0_Task_0_TaskComboSelector_beelineComboSelectorItem_NonBillable"
FIELD_UNBOX_ID_PREFIX = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_0_Task_0_EntryTextBox_"
TIMESHEET_BLOCK_ID = "TimesheetTimeBlockScreen_0_TimesheetTimeBlockRow_1"
START_TIME_CLASS = "startTimeComboSelector"
END_TIME_CLASS = "endTimeComboSelector"
TIME_BLOCK_SAVE_ID = "timesheetTimeBlockSave"
MASTER_DIALOG_IFRAME_ID = "Master_Dialog_IFrame"

SUBMIT_TIMESHEET_BUTTON_ID = "submitTimesheetButton"

MONDAY_TEXT_ID = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_2_DateHeading_0"
FRIDAY_TEXT_ID = "Assignment_0_AssignmentDetail_0_TimesheetRowGroup_2_DateHeading_4"

def fill_timesheet(webdriver, project_task, is_billable = True) -> None:
	wait = WebDriverWait(webdriver, 10)

	projectTaskInput = webdriver.find_element_by_id(PROJECT_TASK_ID)
	projectTaskInput.clear()
	projectTaskInput.send_keys(project_task)
	sleep(3)
	billableNonbillableInput: WebElement = webdriver.find_element_by_id(BILLABLE_NONBILLABLE_ID)
	billableNonbillableInput.click()
	
	sleep(3)
	billableOption: WebElement = wait.until(lambda x: x.find_element_by_id(BILLABLE_ID))
	billableOption.click()
	
	for day_idx in range(0, 5):
		try:
			field_unbox_input: WebElement = webdriver.find_element_by_id(FIELD_UNBOX_ID_PREFIX + str(day_idx))
			if field_unbox_input.is_enabled:
				field_unbox_input.click()
	
				wait.until(
					lambda x: x.find_element_by_class_name("modal-open")
				)

				wait.until(
					lambda x: not x.find_element_by_id("Master_Dialog_LoadingPanel").is_displayed()
				)
	
				webdriver.switch_to.frame(MASTER_DIALOG_IFRAME_ID)
	
				startTimeInput: WebElement = webdriver.find_element_by_class_name(START_TIME_CLASS)
				startTimeInput.clear()
				startTimeInput.send_keys("9:00 AM")
	
				endTimeInput: WebElement = webdriver.find_element_by_class_name(END_TIME_CLASS)
				endTimeInput.clear()
				endTimeInput.send_keys("5:00 PM")
	
				saveButton: WebElement = webdriver.find_element_by_id(TIME_BLOCK_SAVE_ID)
				saveButton.click()
	
				webdriver.switch_to.default_content()
				wait.until(
					lambda x: not x.find_element_by_class_name("ui-dialog").is_displayed()
				)
		except NoSuchElementException:
			continue

def can_submit_timesheet(webdriver) -> bool:
	return True if webdriver.find_element_by_id(SUBMIT_TIMESHEET_BUTTON_ID).is_displayed() else False
 
def submit_timesheet(webdriver) -> None:
	submitButton: WebElement = webdriver.find_element_by_id(SUBMIT_TIMESHEET_BUTTON_ID)
	submitButton.click()
 
	dialogButtonset: WebElement = webdriver.find_element_by_class_name("ui-dialog-buttonset")
	dialogButtons = dialogButtonset.find_elements_by_class_name("ui-button")
	
	confirmationButton = next(x for x in dialogButtons if "Submit" in x.text)
	confirmationButton.click()

	WebDriverWait(webdriver, 10).until(
		lambda x: not x.find_element_by_class_name("controllerOverlay").is_displayed()
	)
 
def get_timesheet_date_range(webdriver) -> str:
	try:
		timesheet_selector: WebElement = webdriver.find_element_by_id("timesheetSelectorUl")
		current_timesheet: WebElement = timesheet_selector.find_element_by_class_name("active")
		date_range: WebElement = current_timesheet.find_element_by_class_name("title")
		return date_range.text
	except Exception:
		return "?"
