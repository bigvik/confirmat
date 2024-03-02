<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>Конфирмат</title>
        <!-- Bootstrap icons-->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-table@1.22.2/dist/bootstrap-table.min.css" rel="stylesheet">
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="../css/bootstrap.min.css" rel="stylesheet">
        <link href="../css/custom.css" rel="stylesheet" />
    </head>
    <body>
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container justify-content-center px-4 px-lg-5">
                <a class="navbar-brand" href="/"><img src="../logo.jpg"/></a>
            </div>
        </nav>

        <!-- Product section-->
        <section class="py-5">
            <div class="container justify-content-center">
                <div class="input-group mb-3">
                    <input id="filter" type="text" class="form-control" onkeyup="filterTable()" placeholder="<?=$uisearch?>" aria-describedby="button-addon1"/>
                </div>

                <table id="table" data-url="/json" data-filter-control="true" data-show-search-clear-button="true" data-search="true" class="table table-bordered table-striped table-hover">
                      <thead>
                          <tr>
                                <th data-field="id">ID</th>
                                <th data-field="name" data-sortable="true" data-sort-name="id" data-sort-order="desc" data-filter-control="input"><?=$uiname?></th>
                                <th data-field="price"><?=$uiprice?></th>
                          </tr>
                      </thead>
                    <?=$content?>
                </table>
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
        <script>
function filterTable() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("filter");
  filter = input.value.toUpperCase();
  table = document.getElementById("table");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
</script>
        
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