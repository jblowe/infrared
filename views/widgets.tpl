<div id="widgets" class="col-sm-8">
    % base_string = data['base_string']
    % current_view = data['controls']['view']
    <section class="paginate-section">
        <div class="page-links">
            <a rel="next" href="/facet/?{{!base_string}}&page=2">« Previous »</a>
            <span class="page-entries">
                    <strong>1</strong> - <strong>10</strong> of <strong>{{ data['results']['numfound'] }}</strong>
                </span> |
            <a rel="next" href="/facet/?{{!base_string}}&page=2">Next »</a>
        </div>
    </section>
</div>
<div id="displays" class="col-sm-4" style="float: right;">
    <nav class="nav">
        <a class="nav-link {{'active' if current_view == 'TABLE' else ''}}" href="/facet/?{{!base_string}}&view=TABLE">
            <span class="fas fa-table fa-2x"></span>
        </a>
        <a class="nav-link {{'active' if current_view == 'LIST' else ''}}" href="/facet/?{{!base_string}}&view=LIST">
            <span class="fas fa-list fa-2x"></span>
        </a>
        <a class="nav-link {{'active' if current_view == 'GALLERY' else ''}}" href="/facet/?{{!base_string}}&view=GALLERY">
            <span class="fas fa-th fa-2x"></span>
        </a>
        <a class="nav-link {{'active' if current_view == 'FULL' else ''}}" href="/facet/?{{!base_string}}&view=FULL">
            <span class="fas fa-file fa-2x"></span>
        </a>
    </nav>
</div>
