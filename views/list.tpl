<div id="documents" class="card">
    <div class="card-body">
        % for i,r in enumerate(data['content']):
        <div class="row">
            <div class="col-sm-8">
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
            <div class="col-sm-4">
                <img class="thumbnail" src="{{r[data['image_field']]}}">
            </div>
        </div>
        % end
    </div>
</div>
