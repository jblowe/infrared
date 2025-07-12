<div id="images" class="row row-cols-1 row-cols-md-5 g-2">
  % if data['image_field'] in r:
    % for image in r[data['image_field']]:
      <div class="col">
        <div class="card h-100">
          <img class="card-img-top" src="{{image}}" style="margin: 0; padding: 0; border: none;" />
          <div class="card-body">
            % card_title = image.replace('.thumb.jpg','').replace('/images/','')
            <h6 class="card-title">{{card_title}}</h6>
          </div>
        </div>
      </div>
    % end
  % end
</div>
