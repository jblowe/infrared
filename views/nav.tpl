<!-- Static navbar -->
<nav class="navbar navbar-expand-md navbar-dark" style="background-color: {{ BANNER_COLOR }};">
  <div class="container">
    <div class="row">
        <div class="col-md-9">
          <a class="navbar-brand" href="/">{{ BANNER }}</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
        </div>
      <div class="collapse navbar-collapse col-sm-3" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <a class="nav-item nav-link active" href="/"><span class="fas fa-home" /></a>
          <a class="nav-item nav-link" href="/about"><span class="fas fa-info-circle" /></a>
        </div>
      </div>
    </div>
        % include('buttons.tpl')
  </div>
</nav>
