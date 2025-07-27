% if data['results']['results'] != []:
<div id="widgets" class="col-sm-8">
    % base_string = data['base_string']
    % current_view = data['controls']['view']
    <section class="paginate-section">
        <div class="page-links">
            % previous = controls['page'] - 1 if controls['page'] > 0 else 1
            % if controls['page'] > 1:
                <a rel="next" href="/facet/?{{!base_string}}&page={{ controls['page'] - 1 }}">« Previous | </a>
            % end
            <span class="page-entries">
                % numfound = f"{data['results']['numfound']:,}"
                % if data['results']['start_row'] + len(data['results']['results']) < data['results']['numfound']:
                    % cell = data['results']['start_row']+len(data['results']['results'])
                    % cell = f'{cell:,}'
                    <strong>{{ data['results']['start_row']+1 }}</strong> - <strong>{{ cell }}</strong> of <strong>{{ numfound }}</strong>
                % else:
                    <strong>{{ data['results']['start_row']+1 }}</strong> - <strong>{{ numfound }}</strong>
                % end
            </span>
            % if (data['controls']['per_page'] * data['controls']['page']) < data['results']['numfound']:
                <a rel="next" href="/facet/?{{!base_string}}&page={{ controls['page'] + 1}}"> | Next »</a>
            % end
            <small>Page {{ controls['page'] }}</small>
        </div>
    </section>
</div>
<div id="displays" class="col-sm-4" style="float: right;">
    <nav class="nav nav-pills">
        <a title="Table" class="nav-link {{'active' if current_view == 'TABLE' else ''}}" href="/facet/?{{!base_string}}&page={{ controls['page'] }}&view=TABLE">
            <span class="fas fa-table fa-2x"></span>
        </a>
        <a title="List" class="nav-link {{'active' if current_view == 'LIST' else ''}}" href="/facet/?{{!base_string}}&page={{ controls['page'] }}&view=LIST">
            <span class="fas fa-list fa-2x"></span>
        </a>
        <a title="Gallery" class="nav-link {{'active' if current_view == 'GALLERY' else ''}}" href="/facet/?{{!base_string}}&page={{ controls['page'] }}&view=GALLERY">
            <span class="fas fa-th fa-2x"></span>
        </a>
        <a title="Full" class="nav-link {{'active' if current_view == 'FULL' else ''}}" href="/facet/?{{!base_string}}&page={{ controls['page'] }}&view=FULL">
            <span class="fas fa-file fa-2x"></span>
        </a>
    </nav>
</div>
% end
