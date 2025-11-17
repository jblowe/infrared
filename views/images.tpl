<div id="images" class="row row-cols-1 row-cols-md-5 g-2">
  % if data['image_field'] in r:
    % for image in r[data['image_field']]:
      % image_prefix = data['image_prefix']
      <div class="col">
        <div class="card h-100">
          <a href="{{image_prefix}}/{{image}}" target="image">
            <img class="card-img-top" src="{{image_prefix}}/{{image}}" style="margin: 0; padding: 0; border: none;" />
          </a>
          <div class="card-body">
            % card_title = image.replace('.thumb.jpg','')
            <h6 class="card-title">{{card_title}}</h6>
          </div>
        </div>
      </div>
    % end
  % end
</div>
