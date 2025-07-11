<div id="documents" class="card">
    <div class="card-body">
        % for i,r in enumerate(data['content']):
        <div class="row">
            <header>
                <h5 class="bg-info">{{ i+1 }}. {{ r[TITLE_FIELD] }}</h5>
            </header>
            <div class="col-sm-7">
                <dl class="row lh-sm">
                    % for x in data['result_fields']:
                        % if x[1] in r and x[1] != TITLE_FIELD:
                            <dt class="col-sm-3 lh-sm">
                                {{ x[0] }}
                            </dt>
                            <dd class="col-sm-9 lh-sm">
                                % cell = r[x[1]]
                                % if type(cell) == type([]):
                                %     cell = ', '.join(cell)
                                % end
                                {{ cell }}
                            </dd>
                        % end
                    % end
                </dl>
            </div>
            % if data['image_field'] in r:
                <div class="col-sm-5">
                    % for image in r[data['image_field']]:
                        <img class="thumbnail-small" src="{{image}}">
                    % end
                </div>
            % else:
                <div class="col-sm-5">
                    <img class="thumbnail" src="/static/unavailable.png">
                </div>
            % end
        </div>
        % end
    </div>
</div>
