<div id="documents" class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table-sm table-striped">
                <thead>
                <th>id</th>
                % for x in data['result_fields']:
                <th>
                    {{ x[0] }}
                </th>
                % end
                </thead>
                <tbody>
                % for i,r in enumerate(data['content']):
                <tr class="">
                    <td>{{ i+1 }}</td>
                    % for x in data['result_fields']:
                        <td>{{ r[x[1]] }}</td>
                    % end
                </tr>
                % end
                </tbody>
            </table>
        </div>
    </div>
</div>
