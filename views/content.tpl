<div class="row">
    % include('widgets.tpl')
</div>
% current_view = data['controls']['view']
% if data['results']['results'] == []:
<h2>No results found for your search</h2>
    Try modifying your search
    <li> Use fewer keywords to start, then refine your search using the links on the left.
% elif current_view == 'TABLE':
    % include('table.tpl')
% elif current_view == 'LIST':
    % include('list.tpl')
% elif current_view == 'GALLERY':
    % include('gallery.tpl')
% elif current_view == 'FULL':
    % include('full.tpl')
% else:
    % include('full.tpl')
% end