<!DOCTYPE html>
<html lang="en">
% include('head.tpl')
<body>
% include ('nav.tpl')
% include('input_field.tpl')
<div role="main" class="container-fluid w-100 px-5">
    <div class="row">
        % include('breadcrumbs.tpl')
    </div>
    <div class="row">
        <div id="leftpane" class="col-sm-2">
            % include('leftpane.tpl')
        </div>
        <div id="content" class="col-sm-10" class="container-fluid">
        % if 'home' in data:
            % include('home.tpl')
        % elif 'about' in data:
            % include('about.tpl')
        % elif 'content' in data:
            % include('content.tpl')
        % elif 'single' in data:
            % include('single.tpl')
        % else:
            % include('alerts.tpl')
            % if command in data:
                % include(f'{data[command]}.tpl')
            % end
        % end
        </div>
    </div>
</div>
% include('footer.tpl')
</body>
</html>
