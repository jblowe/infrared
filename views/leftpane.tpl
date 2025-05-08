<h6 class="">Facets</h6>
<div id="facets">
    % for facet in FACETS:
        % if facet[1] in data['results']['facets']:
        <div class="card facet-limit">
            <h3 class="card-header">
            <button
                class="btn text-left"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#facet-{{ facet[1] }}"
                aria-expanded="false"
                aria-controls="facet-{{ facet[1] }}"
            >
                {{ facet[0] }}
            </button>
            </h3>
            <ul id="facet-{{ facet[1] }}" class="card-body collapse">
                % for f in data['results']['facets'][facet[1]]:
                <li class="d-flex justify-content-between align-items-top">
                    <a class="text-decoration-none" href="/facet/?{{ data['query_string'] }}&{{ facet[1] }}={{ f }}">
                        {{ f }}
                    </a>
                    <span>
                        {{ data['results']['facets'][facet[1]][f] }}
                    </span>
                </li>
                % end
            </ul>
        </div>
        % end
    % end
</div>
