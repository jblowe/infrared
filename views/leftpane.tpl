% if data['results']['results'] != []:
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
                        aria-expanded="{{ 'true' if facet[1] in data['terms'] else 'false' }}"
                        aria-controls="facet-{{ facet[1] }}"
                >
                    {{ facet[0] }}
                </button>
            </h3>
            <ul id="facet-{{ facet[1] }}" class="card-body collapse{{ ' show' if facet[1] in data['terms'] else '' }}">
              % for f in data['results']['facets'][facet[1]]:
                <li class="d-flex justify-content-between align-items-start">
                  % if data['terms'].get(facet[1]) == f:
                    % qstr = data['query_string'].replace(f"{facet[1]}={f}", "")
                    % qstr = qstr.lstrip('&').lstrip('?')
                    <span class="facet-label d-flex align-items-center">
                      <span class="me-1 text-primary">{{ f }}</span>
                      <a class="remove text-primary ms-1" href="/facet/?{{ qstr }}">
                        <span class="fas fa-times" aria-hidden="true"></span>
                        <span class="visually-hidden">[remove]</span>
                      </a>
                    </span>
                  % else:
                    <a class="text-decoration-none" href="/facet/?{{ data['query_string'] }}&{{ facet[1] }}={{ f }}">
                      {{ f }}
                    </a>
                  % end
                    % cell = int(data['results']['facets'][facet[1]][f])
                    % cell = f'{cell:,}'
                  <span>{{ cell }}</span>
                </li>
              % end
            </ul>
        </div>
        % end
    % end
</div>
% end