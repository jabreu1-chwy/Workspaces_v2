# File path of the CSV file containing the usernames
$filePath = "C:\Users\AA-JAbreu1\Downloads\10_2_23.csv"

# Get the contents of the CSV file
$contents = Import-Csv $filePath

# Iterate through each row in the contents
foreach ($row in $contents) {
    try {
        # Get the user object from Active Directory
        $user = Get-ADUser -Identity $row.UserName -Properties Enabled, DistinguishedName, Department, Title

        if ($user.Enabled -eq $true) {
            $status = "Enabled"
        } else {
            $status = "Disabled"
        }

        # Add the status, department, and title to the current row
        $row | Add-Member -NotePropertyName "Status" -NotePropertyValue $status
        $row | Add-Member -NotePropertyName "Department" -NotePropertyValue $user.Department
        $row | Add-Member -NotePropertyName "Title" -NotePropertyValue $user.Title
    } catch {
        # Add the status to the current row
        $row | Add-Member -NotePropertyName "Status" -NotePropertyValue "Not in AD"
    }
}

# Export the contents back to the CSV file
$contents | Export-Csv -Path $filePath -NoTypeInformation
