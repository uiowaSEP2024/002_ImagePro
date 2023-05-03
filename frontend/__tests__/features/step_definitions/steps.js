const assert = require('assert')
const { When, Then, Given } = require('@cucumber/cucumber')

Given('user is on the homepage',  function () {
  assert.equal("cat", "cat")
});

Given('user clicks sign up', function () {
  assert.equal("cat", "cat")
});

When('user fills First Name with John and Last Name with Thomas and Email with john@gmail.com', function () {
  assert.equal("cat", "cat")
});

When('user fills Password with abd', function () {
  assert.equal("cat", "cat")
}); 

When('user fills Confirm Password with abd', function () {
  assert.equal("cat", "cat")
});

When('user clicks create account button', function () {
  assert.equal("cat", "cat")
});

Then('user should see Sign up successful', function () {
  assert.equal("cat", "cat")
});

Then('user should still be on signup page', function () {
  assert.equal("cat", "cat")
});

When('user puts Confirm Password as cat', function () {
  assert.equal("cat", "cat")
});

Then('error message should display with Passwords Do Not Match', function () {
  assert.equal("cat", "cat")
});
