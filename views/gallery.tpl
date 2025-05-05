<div id="documents" class="card-group">
    % for i,r in enumerate(data['content']):
    <div class="card">
        % if data['image_field'] in r:
        <img class="card-img-top" style="max-width: 300px" src="{{r[data['image_field']]}}">
        % end
        <div class="card-body">
            <h5 class="card-title">{{ i+1 }}</h5>
            <div class="card-body">
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
        </div>
    </div>
    % end
</div>
