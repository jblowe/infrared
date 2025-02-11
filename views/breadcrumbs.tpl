<form class="breadcrumbs-form" action="/" accept-charset="UTF-8" method="get">
    <div class="row p-2">
        <div id="startover" class="col-sm-2">
            <button class="btn btn-primary">
                Start over
            </button>
        </div>
        <div id="breadcrumbs" class="col-sm-10">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    % for b in data['results']['terms']:
                        <li class="breadcrumb-item">
                        % from bottle import request
                        <a class="btn btn-outline-secondary" href="{{ request.url }}&remove={{b}}">
                              {{ FACET_LABELS[b] }} > {{ data['results']['terms'][b] }}
                              <span class="remove-icon" aria-hidden="true">✖</span>
                              <span class="sr-only visually-hidden">
                                Remove constraint {{ FACET_LABELS[b] }} {{ data['results']['terms'][b] }}
                              </span>
                        </a>
                        </li>
                    % end
                </ol>
            </nav>
        </div>
    </div>
</form>