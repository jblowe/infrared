<div id="documents" class="row row-cols-1 row-cols-md-5 g-4">
    <!-- div id="documents" class="card-group" -->
    % for i,r in enumerate(data['content']):
    <div class="col">
        <!-- div class="card" style="width: 10rem;" -->
        <div class="card">
            % if data['image_field'] in r:
                % for image in r[data['image_field']]:
                    <img src="{{image}}" class="card-img-top" alt="{{ r[TITLE_FIELD] }}">
                % end
            % else:
                <img src="https://placehold.co/200x200/orange/white" class="card-img-top" alt="placeholder image">
            % end
            <div class="card-body" style="padding: 3px;">
                <!-- h5 class="bg-info">{{ i+1 }}. {{ r[TITLE_FIELD] }}</h5 -->
                <h6 class="">{{ r[TITLE_FIELD] }}</h6>
                <!-- h5 class="card-title">{{ i+1 }}</h5 -->
                <ul class="list-unstyled">
                    % for x in data['result_fields']:
                    % if x[1] in r and x[1] != TITLE_FIELD:
                    <li>
                        % cell = r[x[1]]
                        % if type(cell) == type([]):
                        %     cell = ', '.join(cell)
                        % end
                        {{ cell }}
                    </li>
                    % end
                    % end
                </ul>
            </div>
        </div>
    </div>
    % end
</div>
