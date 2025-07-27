<div class="navbar bg-secondary-subtle">
    <form class="container-fluid" action="/search/?{{ data['query_string']}}" accept-charset="UTF-8" method="get">
        <div class="form-group row w-100 px-5">
            <div class="col-2">
                <select name="search_field" class="form-select">
                    <option value="text">Select...</option>
                    % for c in SEARCH:
                    <option value="{{c[1]}}"
                        % if c[0]== data['selected_field']:
                            selected
                        % end
                    >{{c[0]}}
                    </option>
                    % end
                </select>
            </div>
            <div class="col-5">
                <input name="search_value" type="text" class="form-control"
                       placeholder="Enter a few keywords..."
                       aria-label="search">
                <input name="query_string" type="hidden" value="{{ data['query_string'] }}">
            </div>
            <div class="col-1">
                <button class="btn btn-sm btn-primary form-control" name="search">
                    <span class="fas fa-search fa-lg"></span>
                </button>
            </div>
        </div>
    </form>
</div>