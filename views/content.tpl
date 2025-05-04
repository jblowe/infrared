<div class="row">
    % include('widgets.tpl')
</div>
% current_view = data['controls']['view']
% if current_view == 'TABLE':
    % include('table.tpl')
% elif current_view == 'LIST':
    % include('list.tpl')
% elif current_view == 'GALLERY':
    % include('gallery.tpl')
% elif current_view == 'FULL':
    % include('full.tpl')
% else:
    % include('full.tpl')