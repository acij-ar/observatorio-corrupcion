<template>
  <footer class="footer">
    <div class="container">
      <div class="content has-text-centered">
        <p>
          El código fuente esta licenciado bajo <a href="https://www.gnu.org/licenses/gpl.html" target="_blank">
          GPLv3</a>. El contenido del sitio esta con
          <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">CC BY SA 4.0</a>.
        </p>
      </div>

      <div class="columns">
        <div class="column is-2 is-offset-4 horizontal-center">
          <a href="https://acij.org.ar/" target="_blank">
            <img src="@/assets/img/logo_acij.png" class="b" />
          </a>
        </div><!--/column -->

        <div class="column is-3 horizontal-center">
          <a href="http://conocimientoabierto.org/" target="_blank">
            <img src="@/assets/img/logo_fca.png" class="a" />
          </a>
        </div><!--/column -->
      </div><!--/columns -->

    </div><!--/container -->
  </footer>
</template>

<style scoped>
p {
  color: white !important;
}

.footer {
  background-color: #292935;
  padding-top: 50px;
  padding-bottom: 30px;
}

.red {
  color: red;
}

.footer a,
.footer a:hover {
  color: #018ed3;
}

.a {
  max-width: 222px;
  max-height: 80px;
}

.b {
  max-width: 140px;
  max-height: 80px;
}
</style>
