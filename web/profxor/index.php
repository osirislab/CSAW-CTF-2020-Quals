<?php

header("Cache-Control: no-cache, must-revalidate");

$test = $_GET['comfortable'];

$value = $_GET['value'];

function xor_this($string) {

    // Let's define our key here
    $key = ('12');

    // Our plaintext/ciphertext
    $text = $string;

    // Our output text
    $outText = '';

    // Iterate through each character
    for($i=0; $i<strlen($text); )
    {
        for($j=0; ($j<strlen($key) && $i<strlen($text)); $j++,$i++)
        {
            $outText .= $text{$i} ^ $key{$j};
            //echo 'i=' . $i . ', ' . 'j=' . $j . ', ' . $outText{$i} . '<br />'; // For debugging
        }
    }
    return $outText;
}

// THESE DATABSE DEFINITIONS ARE IMPORTANT FOR PROPER QUERY EXECUTION
$table_name = "mytable";
$col_name = "Message";


$user = xor_this($value);
$query = "SELECT * from ";
$query .= $table_name;
$query .= " where ";
$query .= $col_name;
$query .= "='";
$query .= $user;
$query.= "'";

if ($query != null){
  $login = runQuery($query);
}
// MySQL database connection


function runQuery($query){
  $servername = "127.0.0.1";
  $username = "root";
  $password = "password";
  $database = "mydb";

  // Create connection
  $conn = new mysqli($servername, $username, $password, $database);

  // Check connection
  if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }
    //echo "Connected successfully";

    //$test_q = "SELECT * FROM mytable";


    $result = $conn->query($query);

    //echo $result;
    //Query Check
    if ($result->num_rows > 0) {
      return true;
    }
}

?>


<html>
<head>
  <link rel="stylesheet" type="text/css" href="style.css" />
  <meta charset="utf-8">
  <title>A Blind Scramble</title>
</head>
  <body>
    <?php if($test=="yes"): //echo md5("secretstr"."What Can I do for you")?>
      <div class="vert_pad">
        <h2>fZPFQP\{ZT^AH]DF[EZ  -->  What Can I help you with</h2><br>
        <h3>P.S. - I'm not sure we're safe. Send me your login encoded. </h3>
        <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="get">
          <input class="box" type="text" name="value"><br>
          <input type = "hidden" method="get" name="comfortable" value="yes">
          <input class = "button" type="submit"><br>
        </form>
      </div>

    <?php else: ?>

      <div class="vert_pad">
        <h2>Decode this to make me comfortable. <br> Otherwise, please get out of here</h2>
        <h2 id="scary">fZPFQP\{ZT^AH]DF[EZ</h2>
          <form id = 'ini' action="<?php echo $_SERVER['PHP_SELF']; ?>" method="get">
            <input class="box" type = "text" method="post" name="">
            <input type = "hidden" method="get" name="comfortable" value="no"><br>
            <input class = "button" type="submit"><br>
          </form>
      </div>

    <?php endif ?>

    <?php if($login): ?>
      <div class="vet_pad">
        <h2> Whoa dude! Nothing Here! </h2>
      </div>
    <?php endif ?>
  </body>

</html>
