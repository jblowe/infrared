<h6 class="">Facets</h6>
<div id="facets">
    % for facet in FACETS:
        % if facet[1] in data['results']['facets']:
        <div class="card facet-limit">
            <h3 class="card-header">
                <button
                    class="btn w-100 text-left"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#facet-{{ facet[1] }}"
                    aria-expanded="false"
                    aria-controls="facet-{{ facet[1] }}"
                >
                    {{ facet[0] }}
                </button>
            </h3>
                <ul id="facet-{{ facet[1] }}" class="collapse">
                    % for f in data['results']['facets'][facet[1]]:
                    <li>
                        <span class="facet-label">
                            <span>{{ f }}</span>
                            <a class="remove" rel="nofollow" href="/facet/?{{ data['query_string'] }}&{{ facet[1] }}={{ f }}">
                                <span class="remove-icon" aria-hidden="true">✖</span>
                                <span class="sr-only visually-hidden">[remove]</span>
                            </a>
                        </span>
                        <span class="facet-count">{{ data['results']['facets'][facet[1]][f] }}</span>
                    </li>
                    % end
                </ul>
        </div>
        % end
    % end
</div>
