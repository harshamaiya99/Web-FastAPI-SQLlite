@ignore
Feature: Authentication Helper

  Scenario: Get Manager Token
    Given url baseUrl
    And path 'token'
    # Use variables passed from karate-config.js (No quotes!)
    And form field username = managerUsername
    And form field password = managerPassword
    When method post
    Then status 200
    * def accessToken = response.access_token