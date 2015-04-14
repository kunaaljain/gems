/*

A simple dynamic script to send emails from google spreadsheet
FORMAT:
X A                       B
1 Number of Users	      5
2 	
3 Username	              Password
4 kunaalus@gmail.com	  kunaal
5 j.kunal@iitg.ernet.in	  jain


Made with love by : Kunaal Jain (kunaalus@gmail.com)
*/


var confirmation = "Sent";

function sendEmails2() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var startRow = 4;
  var numrange = sheet.getRange(1,2);
  var numRows = numrange.getValue(); 
  var dataRange = sheet.getRange(startRow, 1, numRows, 3) //(row,col,row,col)
  // Fetch values for each row in the Range.
  var data = dataRange.getValues();
  for (var i = 0; i < data.length; ++i) {
    var row = data[i];
    var emailAddress = row[0]; 
    var message = "your password is " + row[1];     
    var emailSent = row[2];     
    if (emailSent != confirmation) {  // Prevents sending duplicates
      var subject = "Your username and password";
      MailApp.sendEmail(emailAddress, subject, message);
      sheet.getRange(startRow + i, 3).setValue(confirmation);
      // Make sure the cell is updated right away in case the script is interrupted
      SpreadsheetApp.flush();
    }
  }
}