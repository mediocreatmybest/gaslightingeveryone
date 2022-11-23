#Tested on flickr extractor, seems to be ok. 
#No doubt a better way exists on how to clean this up.
#Only pulls title, description, cleans up symbols, and forces single line, tags currently not being appended commas. 
#$imgextension = @('.png','.jpg','.jpeg')
$textextension = @('.json')
$caption_dir = "C:\example-images\"


Get-ChildItem -Path $caption_dir -File  | foreach-object {
    if ($textextension -eq $_.Extension ) { 
      
    #shorten name and remove final extension, this assumes all json files match an image file (no error checking on this or anywhere really) 
    $simplename = $_.BaseName|Out-String -Stream
    #Remove square brackets as they cause issues with powershell
    $path = $_.FullName -replace "(\[|\])","*"
    $jsonfile = (Get-Content -Raw -Path $path |ConvertFrom-Json |Select-Object title, description | ConvertTo-Csv -NoTypeInformation | Select-Object -skip 1)
    $results = $jsonfile|Out-String
    $tags = (Get-Content -Raw -Path $path |ConvertFrom-Json |Select-Object -expand tags)
    $tagresults = $tags

    
    #Regular text filtering

    # Remove new lines
    $results = $results -replace "`t|`n|`r",""
    $results = $results -replace " ;|; ",";"
   
     # Remove " double quote marks
    $results = $results -replace '"',''

    # Catch any new double spaces - Not working. 
    #$results = $results -replace "\s+", " "
    #$results = [regex]::Replace($results, "\s+", " ")
    #This might work for the moment
    $results = $results -replace ' - ',' '
    $results = $results -replace ' = ',' '

    #remove wiki references
    $results = $results -replace ':wiki:'
   
    #remove additional Info flickr
    $results = $results -replace "PROCESS INFO|SOURCE INFO|IMAGE INFO",","

    #Catch any new double commas,
    $results = $results -replace ",,",","
    
    #leave web address only
    #$results = $results -Replace ".*//|(.*?)/.*",'$1'
    
    #remove HREF Info
    $results = $results -replace "<a.*</a>"
    
    #remove additional symbols
    $results = $results -replace '[\=\(\)*.:-]'
    
    #remove white space from start and end, and final character , before output, uncomment if needed
    $results = $results.Trim()
    $len = $results.Length
    $len = $len - 1
    #$results = $results.Remove($len,1)
    
    #TAGs text filtering

    #$tagresults = $tagresults -replace "`t|`n|`r"
    #$tagresults = $tagresults -replace " ;|; "
    #Can't seem to put commas after each tag. Broken. 
    #$tagresults = $tagresults -replace '/s',', '
    
    #Final Output     
    Write-Output $simplename", "$results", "$tagresults |Out-File -FilePath $caption_dir$simplename".txt"
    Write-Output $simplename", "$results", "$tagresults |Out-File -Append -FilePath $caption_dir"captions.txt"
    
    #write to screen, Uncomment it out if you want to see output. 
    #Write-Host $simplename", "$results", "$tagresults

     }
       
        
}