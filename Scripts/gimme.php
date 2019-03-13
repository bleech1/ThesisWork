<?php
$uploaddir = "/home/bleech/ThesisData/";
$uploadfile = $uploaddir.$_FILES['data']['name'];
if(move_uploaded_file($_FILES['data']['tmp_name'], $uploadfile))
{
  echo "The file has been uploaded successfully";
}
else
{
  echo "There was an error uploading the file";
}
?>