<div id="documents" class="card">
    <div class="card-body">
        % for i,r in enumerate(data['content']):
            <div class="row">
                <header>
                    <h5 class="bg-info">{{ i+1 }}. {{ r[TITLE_FIELD] }}</h5>
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
            <div id="images" class="row row-cols-1 row-cols-md-4 g-4">
                % if data['image_field'] in r:
                    % for image in r[data['image_field']]:
                    <div class="card">
                        <img class="card-img-top" src="{{image}}"/>
                        <div class="card-body" style="padding: 2px;">
                            % card_title = image.replace('.thumb.jpg','').replace('/images/','')
                            <h6 class="card-title">{{card_title}}</h6>
                        </div>
                    </div>
                    % end
                % else:
                    <div class="col-sm-5">
                        <img class="thumbnail" src="/static/unavailable.png">
                    </div>
                % end
            </div>
        % end
    </div>
</div>
