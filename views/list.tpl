<div id="documents" class="card">
    <div class="card-body">
        % for i,r in enumerate(data['content']):
        <div class="row">
            <header>
                <a href="/catalog/{{ r['id'] }}">
                    <h5 class="bg-info">{{ i+1 }}. {{ r[TITLE_FIELD] }}</h5>
                </a>
            </header>
            % if data['image_field'] in r:
                <div class="col-sm-7">
            % else:
                <div class="col-sm-12">
            % end
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
            % include('images.tpl')
        </div>
        % end
    </div>
</div>
