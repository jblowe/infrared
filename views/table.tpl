<table class="table table-striped table-responsive-sm">
    <thead class="bg-info">
        <th>Row</th>
        % for x in data['result_fields']:
        <th data-field="{{ x[1] }}"
            data-sortable="true"
        >
            {{ x[0] }}
        </th>
        % end
        <th data-field="has_image"
            data-sortable="true"><span class="fas fa-image fa-2x"></span>
        </th>
    </thead>
    <tbody>
    % for i,r in enumerate(data['content']):
    <tr>
        <td>{{ i+1 }}</td>
        % for x in data['result_fields']:
            % if x[1] in r:
                <td style="white-space: nowrap;">{{ r[x[1]] }}</td>
            % else:
                <td/>
            % end
        % end
        % if data['image_field'] in r:
            <td>
                <a target="_blank" href="{{r[data['image_field']][0]}}"><span class="fas fa-image fa-2x"></span></a>
            </td>
        % else:
          <td/>
        % end
    </tr>
    % end
    </tbody>
</table>
