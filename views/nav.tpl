<!-- Static navbar -->
<nav class="navbar navbar-expand-sm navbar-dark" style="background-color: {{ BANNER_COLOR }};">
  <div class="container-fluid">
        <div class="navbar-nav">
          <a style="padding-left: 30px;" class="navbar-brand" href="/">
            <img style="max-height: 40px; padding-left: 30px;" src="/static/{{ LOGO }}">
          </a>
          <a style="padding-left: 30px;" class="navbar-brand" href="/">{{ BANNER }}</a>
        </div>
      <div class="navbar-nav">
          <a class="nav-item nav-link" href="/"><span class="fas fa-home special" /></a>
          <a class="nav-item nav-link" href="/about"><span class="fas fa-info-circle special" /></a>
      </div>
      % include('buttons.tpl')
    </div>
</nav>
