<div id="documents" class="card">
    <div class="card-body">
        % for i,r in enumerate(data['content']):
        <div class="row">
            <header>
                <h5>{{ i+1 }}</h5>
            </header>
            <dl class="row lh-sm">
                % for x in data['result_fields']:
                    % if x[1] in r:
                        <dt class="col-sm-3 lh-sm">
                            {{ x[0] }}
                        </dt>
                        <dd class="col-sm-9 lh-sm">
                            {{ r[x[1]] }}
                        </dd>
                    % end
                % end
            </dl>
        </div>
        % if data['image_field'] in r:
            <div class="col-sm-4">
                % for image in r[data['image_field']]:
                    <img class="thumbnail" src="{{image}}">
                % end
            </div>
        % end
        % end
    </div>
</div>
