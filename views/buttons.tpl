% if not ('about' in data or 'home' in data):
<div class="navbar-nav" style="float: right;">
    <a class="nav-item nav-link" href="{{ data['back'] }}">&lt;&lt; back</a>
    <span style="padding-right: 10px;"> </span>
    <a class="nav-item nav-link" href="#" id="toggle_sidebar">toggle sidebar</a>
</div>
%end
