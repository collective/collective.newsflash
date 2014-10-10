*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${NEWSFLASH} =  Extra! Extra! Read all about it The Pinball Wizard in a miracle cure!

*** Test cases ***

Test News Flash Manager
    Enable Autologin as  Manager
    Go to  ${PLONE_URL}

    Page Should Contain  You have no news flashes registered

    # Test Add News Flash
    Click Manage News Flashes
    Add News Flash
    Page Should Contain  ${NEWSFLASH}

    # Test Remove News Flash
    Click Manage News Flashes
    Remove News Flash
    Page Should Not Contain  ${NEWSFLASH}

*** Keywords ***

Click Manage News Flashes
    Click Element  css=#edit-newsflashes.link-overlay
    Wait Until Page Contains Element  css=div.pb-ajax div#content-core

Add News Flash
    Click Button  Add
    Wait Until Page Contains Element  css=div#formfield-form-widgets-newsflash-0
    Input Text  css=textarea#form-widgets-newsflash-0  ${NEWSFLASH}
    Click Button  Save

Remove News Flash
    Select Checkbox  css=input#form-widgets-newsflash-0-remove
    Click Button  Remove selected
    Wait Until Keyword Succeeds  1  5  Page Should Not Contain Button  Remove selected
    Click Button  Save
