<?php

$routes = [
    // срабатывает при вызове корня или /index.php
    '/' => 'hello',
    // срабатывает при вызове /about или /index.php/about
    '/about' => 'about',
    // динамические страницы
    '/page' => 'page',
    '/all' => 'all'
];

$request = $_SERVER['REQUEST_URI'];

// Параметры подключения к базе данных MySQL
$host = 'mysql-bigvik.alwaysdata.net';
$user = 'bigvik';
$password = '3212745';
$database = 'bigvik_confirmat';


// Site UI language settings
$lang = substr($_SERVER['HTTP_ACCEPT_LANGUAGE'], 0, 2);
if ($lang !== 'kk' && $lang !== 'ru'){$lang = 'ru';}
include('lang/'.$lang.'.php');



// Connecting MySQL
$mysqli = new mysqli($host, $user, $password, $database);
// Errors?
if ($mysqli->connect_error) {
    die('Ошибка подключения (' . $mysqli->connect_errno . ') ' . $mysqli->connect_error);
}

if ($request == '/all'){
    $query = $mysqli->prepare("SELECT id, name, ours_price FROM product_data");
    $query->execute();
    $result = $query->get_result();
    if ($result->num_rows > 0) {
        $content = '';
        while ($row = $result->fetch_assoc()) {
            $content = $content.'<tr>';
            $content = $content.'<td><a href="index.php/?id='.$row['id'].'">'.$row['id'].'</a></td>';
            $content = $content.'<td>'.$row['name'].'</td>';
            $content = $content.'<td>'.$row['ours_price'].' ₸</td>';
            $content = $content.'</tr>';
        }
        include('views/all.php');
    }
    exit;
}

if ($request == '/json'){
    $query = $mysqli->prepare("SELECT id, name, ours_price FROM product_data");
    $query->execute();
    $result = $query->get_result();
    $rows = mysqli_fetch_all($result);
    echo json_encode($rows, JSON_UNESCAPED_UNICODE);
    exit;
}

// Get ID from URL
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

if ($url == ''){include('views/404.php');exit;}

// Закрытие запроса
$query->close();
// Закрытие соединения с базой данных
$linklist = "";

$filter = array('RT', 'RS', 'SU', 'SB', 'DB', 'KR');

if (in_array(substr($art, 0, 2), $filter)){
    $query = $mysqli->prepare("SELECT * FROM product_data WHERE art LIKE ?");
    $param = explode('/', $art)[0]."%";
    $query->bind_param('s', $param);
    $query->execute();
    $result = $query->get_result();

    // Check if there are any rows returned
    if ($result->num_rows > 0) {
        $linklist = "<div>".$uidim.": ";
        while ($row = $result->fetch_assoc()) {
            // Process each row as needed
            $exp = explode("/", $row['art']);
            $key = end($exp);

            if ($key == 'R' || $key == 'L'){$key = prev($exp)."/".$key;}
            if ($key == 'GRPH'){
                $key2 = prev($exp);
                if ($key2 == 'R' || $key2 == 'L'){$key = prev($exp)."/".$key2."/".$key;}
                else{$key = prev($exp)."/".$key;}  
            }
            if ($row['id'] == $id){
                $temp = '<a class="badge bg-primary" href="index.php?id='.$row['id'].'">'.$key.'</a>  ';
            }else{
                $temp = '<a class="badge bg-light text-dark" href="index.php?id='.$row['id'].'">'.$key.'</a>  ';
            }
            
            $linklist .= $temp;
        }
        $linklist .= "</div>";
    } else {
        $linklist = "";
    }

    // Close the result set and the prepared statement
    $result->close();
    $query->close();
}

$mysqli->close();

$jprop = json_decode($prop);

include('views/template.php');
?>