<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>Конфирмат: <?=$name?></title>
        <!-- Favicon-->
        <link rel="icon" type="image/x-icon" href="favicon.ico" />
        <!-- Bootstrap icons-->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css" rel="stylesheet" />
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="css/bootstrap.min.css" rel="stylesheet">
        <link href="css/custom.css" rel="stylesheet" />
    </head>
    <body>
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container justify-content-center px-4 px-lg-5">
                <a class="navbar-brand" href="/"><img src="logo.svg"/></a>
            </div>
        </nav>

        <!-- Product section-->
        <section class="py-5">
            <div class="container px-4 px-lg-5 my-5">
                <div class="row gx-4 gx-lg-5 align-items-center">
                    <div class="col-md-6">
                        <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
                            <div id="crsl" class="carousel-inner">
                                <?
                                foreach(explode(",", $imgs) as $img) {
                                  if (str_contains($img, 'slider_big')){
                                    echo '<div class="carousel-item"><img  class="card-img-top mb-5 mb-md-0" width="600px" src="'.$img.'"/></div>';
                                  }
                                }
                                ?>
                            </div>
                            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls"  data-bs-slide="prev">
                                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                <span class="visually-hidden">Предыдущий</span>
                            </button>
                            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls"  data-bs-slide="next">
                                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                <span class="visually-hidden">Следующий</span>
                            </button>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="small mb-1">Артикул: <?=$art?></div>
                            <h3 class="display-5 fw-bolder"><?=$name?></h3>
                            <div class="fs-5 mb-5">
                                <span id="price"><?if($ours_price == 0){echo 'наличие и цену уточняйте у менеджеров';}else{echo $ours_price.' ₸';}?></span>
                            </div>
                            <?
                              if($linklist != ""){echo $linklist;}
                            ?>
                            &nbsp
                            <div class="gy-5"><ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
                              <li class="nav-item" role="presentation">
                                <button class="nav-link active btn-sm" id="pills-home-tab" data-bs-toggle="pill" data-bs-target="#pills-home" type="button" role="tab" aria-controls="pills-home" aria-selected="true">Описание</button>
                              </li>
                              <li class="nav-item" role="presentation">
                                <button class="nav-link btn-sm" id="pills-profile-tab" data-bs-toggle="pill" data-bs-target="#pills-profile" type="button" role="tab" aria-controls="pills-profile" aria-selected="false">Характеристики</button>
                              </li>
                                </ul>
                                <div class="tab-content" id="pills-tabContent">
                                  <div class="tab-pane fade show active" id="pills-home" role="tabpanel" aria-labelledby="pills-home-tab"><?=$des?></div>
                                  <div class="tab-pane fade" id="pills-profile" role="tabpanel" aria-labelledby="pills-profile-tab">
                                    <ul>
                                    <?
                                        foreach (json_decode($prop, true) as $key => $value) {
                                            echo "<li><strong>$key:</strong>    $value</li>";
                                        }
                                        
                                    ?>
                                      </ul>  
                                </div>
                                </div>
                            </div>

                        
                    </div>
                </div>
            </div>
        </section>

        <!-- Tabs-->


        <!-- Footer-->
        <footer class="py-5 bg-dark">
            <div class="container"><p class="m-0 text-center text-white">Copyright &copy; BIgVik by Confirmat 2024</p></div>
        </footer>
        <!-- Bootstrap core JS-->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
        <!-- Core theme JS-->
        <script src="js/scripts.js"></script>
        
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-64SW410Z3L"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-64SW410Z3L');
        </script>

    </body>
</html>