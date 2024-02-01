<?php
// Параметры подключения к базе данных MySQL
$host = 'mysql-bigvik.alwaysdata.net';
$user = 'bigvik';
$password = '3212745';
$database = 'bigvik_confirmat';

// Подключение к базе данных MySQL
$mysqli = new mysqli($host, $user, $password, $database);

// Проверка наличия ошибок подключения
if ($mysqli->connect_error) {
    die('Ошибка подключения (' . $mysqli->connect_errno . ') ' . $mysqli->connect_error);
}

// Получение значения из URL
$id = isset($_GET['id']) ? intval($_GET['id']) : 0;

if ($id == 0) {
    header('Location: https://www.boyard.biz', true, 303);
    exit();
}

// Подготовленный запрос к базе данных
$query = $mysqli->prepare("SELECT * FROM product_data WHERE id = ?");
$query->bind_param('i', $id);
$query->execute();

// Извлечение данных
$query->bind_result($id, $url, $name, $art, $price, $ours_price, $imgs, $prop, $des, $docs);
$query->fetch();
// Закрытие запроса
$query->close();
// Закрытие соединения с базой данных


if (str_contains($art, 'RT')){
    $query = $mysqli->prepare("SELECT * FROM product_data WHERE art LIKE ?");
    $param = "%".explode('/', $art)[0]."%";
    $query->bind_param('s', $param);
    $query->execute();
    $result = $query->get_result();

    // Check if there are any rows returned
    if ($result->num_rows > 0) {
        $linklist = "<div><p>Размеры: ";
        while ($row = $result->fetch_assoc()) {
            // Process each row as needed
            $exp = explode("/", $row['art']);
            $key = array_key_last($exp);
            $temp = '<a href="index.php?id='.$row['id'].'">'.$exp[$key].'  </a>';
            $linklist .= $temp;
        }
        $linklist .= "</p></div>";
    } else {
        $linklist = "";
    }

    // Close the result set and the prepared statement
    $result->close();
    $query->close();
}

$mysqli->close();

$jprop = json_decode($prop);

include('template.php');
?>