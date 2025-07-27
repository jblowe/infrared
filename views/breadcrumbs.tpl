<form class="breadcrumbs-form" action="/" accept-charset="UTF-8" method="get">
    <div class="row p-2">
        <div id="startover" class="col-sm-2">
            <a href="/" class="btn btn-primary">
                Start over
            </a>
        </div>
        <div id="breadcrumbs" class="col-sm-10">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    % for b in data['terms']:
                        <li class="breadcrumb-item">
                        % from copy import deepcopy
                        % this_crumb = []
                        % for t in data['terms']:
                            % if t[0] == b[0] and t[1] == b[1]:
                                % current = t
                            % else:
                                % this_crumb.append(t)
                            % end
                        % end
                        % from urllib.parse import urlencode
                        % query_string = urlencode(this_crumb) + '&' +  urlencode(data['controls'])
                        <a class="btn btn-outline-secondary" href="/facet/?{{query_string}}">
                           % if any(k == b[0] and v == b[1] for k, v in data['terms']):
                               {{ FACET_LABELS[b[0]] }} > {{ b[1] }}
                               <span class="remove-icon" aria-hidden="true">✖</span>
                               <span class="sr-only visually-hidden">
                                   Remove constraint {{ FACET_LABELS[b[0]] }} {{ b[1] }}
                               </span>
                            % end
                        </a>
                        </li>
                    % end
                </ol>
            </nav>
        </div>
    </div>
</form>