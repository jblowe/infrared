<div id="facets">
    <h6 class="">Facets</h6>
        % for facet in FACETS:
        <div class="dropdown facet-values pb-1">
            <button type="button" class="btn w-100 btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
             {{ facet[0] }}
            </button>
            <ul class="dropdown-menu  w-100">
                % for f in data['results']['facets'][facet[1]]:
                <li>
                    <span class="facet-label">
                        <a class="dropdown-item" href="{{ data['query_string'] }}{{ facet[1] }}={{ f }}">{{ f }}</a>
                    </span>
                    <span class="facet-count">
                        {{ data['results']['facets'][facet[1]][f] }}
                    </span>
                </li>
                % end
            </ul>
        </div>
        % end
</div>
