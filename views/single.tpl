<div id="documents" class="card">
    <div class="card-body">
        % r = data['single']
        <div class="row">
            <header>
                <h5 class="bg-info">{{ r[TITLE_FIELD] }}</h5>
            </header>
            <dl class="row lh-sm">
                % for x in data['result_fields']:
                    % if x[1] in r:
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
</div>
